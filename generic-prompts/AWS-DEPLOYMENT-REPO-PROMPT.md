# Prompt: Building an AWS Terraform/Helm/Scripts Deployment Repository

> **Purpose**: This prompt guides an AI assistant through building a production-grade AWS deployment repository from scratch. It captures lessons learned from real-world deployments and enforces patterns that prevent common mistakes.

---

## CRITICAL RULES (Apply to Every Response)

### Communication Rules
1. **DO NOT ASSUME, DO NOT FILL IN THE BLANKS** - Ask clarifying questions using your question tool
2. **ONE QUESTION AT A TIME** - Use multi-select when options are not mutually exclusive
3. **NO TIME ESTIMATES** - Never say "this will take 2-3 hours". Describe steps, not durations
4. **READ BEFORE EDITING** - Always read a file before modifying it
5. **FIX THE AUTOMATION, NOT THE SYMPTOM** - Never apply manual workarounds; fix the code

### Code Rules
1. **NO AI/ASSISTANT MENTIONS** - Never add comments like "AI-generated", "Claude", etc.
2. **KISS PRINCIPLE** - Simplest solution first. No features "just in case"
3. **SECURITY FIRST** - Never commit secrets, API keys, or credentials
4. **IDEMPOTENT SCRIPTS** - All setup/install scripts MUST be safely re-runnable

---

## Phase 1: Initial Questions

Before writing any code, gather these requirements:

### Project Identity
```
- What is the project name/prefix? (e.g., "tgp" for teams-gitlab-prod)
- What AWS region will this deploy to?
- What domain will be used?
- What application is being deployed? (GitLab, Keycloak, custom app, etc.)
```

### Infrastructure Scope (Discover, Don't Ask)

**DO NOT ask the user about infrastructure services upfront.**

Instead:
1. Use an **exploratory agent** to analyze the application requirements
2. Use a **security expert agent** to recommend services based on the app
3. Only ask the user if there are **conflicting recommendations**

The agent should determine which services are needed by:
- Reading the application's documentation/requirements
- Analyzing similar reference architectures
- Reviewing the Helm chart dependencies (database, cache, storage)

Common patterns to detect:
| If the app needs... | Then include... |
|---------------------|-----------------|
| PostgreSQL database | RDS PostgreSQL in Layer 02 |
| Redis/caching | ElastiCache Redis in Layer 02 |
| Object storage | S3 buckets in Layer 01 |
| Container orchestration | EKS in Layer 03 |
| Private API access | VPN (WireGuard or AWS Client VPN) in Layer 03 |
| CDN/caching | CloudFront in Layer 05 |
| Web application firewall | WAF in Layer 05 |

### Environment Strategy
```
- How many environments? (dev, staging, prod)
- Same account or separate accounts per environment?
- State isolation requirements?
```

---

## Phase 2: Repository Structure

Create this directory structure:

```
project-name/
├── .gitignore
├── Makefile                   # Main workflow orchestration
├── README.md                  # Quick start guide
├── docs/
│   ├── ARCHITECTURE.md        # System design documentation
│   ├── TROUBLESHOOTING.md     # Common issues and solutions
│   └── WIREGUARD.md           # VPN setup (if applicable)
├── helm/
│   ├── values-base.yaml       # Base Helm values (shared)
│   ├── values-prod.yaml       # Production overrides
│   ├── values-dev.yaml        # Development overrides
│   └── [app]-values.yaml      # App-specific values
├── scripts/
│   ├── bootstrap-terraform.sh # One-time: Create S3 backend
│   ├── create-secrets.sh      # Sync AWS Secrets Manager → K8s
│   ├── wait-for-*.sh          # Health check scripts
│   └── validate-destroy.sh    # Pre-destroy validation
└── terraform/
    ├── 01-foundation/         # VPC, S3, KMS, ACM
    ├── 02-data/               # RDS, ElastiCache
    ├── 03-eks/                # EKS, IAM, Node Groups, VPN
    ├── 04-k8s-platform/       # EKS addons, Autoscaler, Observability
    └── 05-edge/               # CloudFront, WAF
```

---

## Phase 3: Terraform Split-State Architecture

### Layer Design Principles

Each layer has:
- **Separate S3 state file** - Blast radius isolation
- **Own backend.tf** - Independent state management
- **remote-state.tf** - Read outputs from upstream layers
- **outputs.tf** - Expose values for downstream layers

### Layer Dependencies

```
01-foundation ──┬──> 02-data ────> 03-eks ──┬──> [kubeconfig]
      │         │                           │
      │         └───────────────────────────┼──> [cilium]
      │                                     │
      └─────────────────────────────────────┴──> 04-k8s-platform
                                                       │
                                                       v
                                               [lb-controller]
                                                       │
                                                       v
                                                [helm-install]
                                                       │
                                                       v
                                                   05-edge
```

### Layer Contents

| Layer | Path | Contents | Dependencies |
|-------|------|----------|--------------|
| 01-foundation | `terraform/01-foundation/` | VPC, S3, KMS, ACM | None |
| 02-data | `terraform/02-data/` | RDS, ElastiCache | 01 |
| 03-eks | `terraform/03-eks/` | EKS, IAM, NLB, VPN | 01, 02 |
| 04-k8s-platform | `terraform/04-k8s-platform/` | Addons, Autoscaler | 03 + Cilium |
| 05-edge | `terraform/05-edge/` | CloudFront, WAF | 03 |

### Remote State Pattern

```hcl
# terraform/02-data/remote-state.tf
data "terraform_remote_state" "foundation" {
  backend = "s3"
  config = {
    bucket = "${var.prefix}-terraform-state"
    key    = "foundation/terraform.tfstate"
    region = var.region
  }
}

# Usage in resources
locals {
  vpc_id             = data.terraform_remote_state.foundation.outputs.vpc_id
  private_subnet_ids = data.terraform_remote_state.foundation.outputs.private_subnet_ids
  kms_key_arn        = data.terraform_remote_state.foundation.outputs.kms_key_arn
}
```

### Output Naming Convention

Use consistent prefixes for outputs:
```hcl
# Good - Consistent naming
output "vpc_id" { value = aws_vpc.main.id }
output "vpc_cidr" { value = aws_vpc.main.cidr_block }
output "private_subnet_ids" { value = aws_subnet.private[*].id }
output "public_subnet_ids" { value = aws_subnet.public[*].id }

# Bad - Inconsistent
output "the_vpc" { ... }
output "subnet_private" { ... }
```

---

## Phase 4: Makefile Orchestration

### Core Structure

```makefile
.PHONY: help apply destroy plan status

# Configuration
NAMESPACE := your-app
TERRAFORM_DIR := terraform
HELM_DIR := helm
REGION := us-east-2
PREFIX := your-prefix
LOGS_DIR := logs

# Terraform layer directories (numbered for explicit ordering)
TF_FOUNDATION := $(TERRAFORM_DIR)/01-foundation
TF_DATA := $(TERRAFORM_DIR)/02-data
TF_EKS := $(TERRAFORM_DIR)/03-eks
TF_K8S_PLATFORM := $(TERRAFORM_DIR)/04-k8s-platform
TF_EDGE := $(TERRAFORM_DIR)/05-edge

# =============================================================================
# Help (First target = default)
# =============================================================================
help:
	@echo "Deployment Workflow"
	@echo ""
	@echo "=== MAIN COMMANDS ==="
	@echo "  make apply     - Full deployment (all steps)"
	@echo "  make destroy   - Full teardown (reverse order)"
	@echo "  make status    - Show deployment status"
	@echo ""
	@echo "=== TERRAFORM LAYERS ==="
	@echo "  tf-foundation  - Layer 01: VPC, S3, KMS"
	@echo "  tf-data        - Layer 02: RDS, Redis (requires: 01)"
	@echo "  tf-eks         - Layer 03: EKS cluster (requires: 01, 02)"
	@echo "  tf-k8s-platform - Layer 04: Addons (requires: 01-03 + cilium)"
```

### Dependency Validation Pattern

```makefile
tf-data: tf-init-data
	@echo "=== Applying Layer 02: Data ==="
	@# Validate Layer 01 outputs exist before proceeding
	@if ! cd $(TF_FOUNDATION) && terraform output vpc_id >/dev/null 2>&1; then \
		echo "ERROR: Layer 01 (Foundation) must be applied first!"; \
		echo "Run: make tf-foundation"; \
		exit 1; \
	fi
	cd $(TF_DATA) && terraform apply -auto-approve

tf-k8s-platform: tf-init-k8s-platform
	@echo "=== Applying Layer 04: K8s Platform ==="
	@# Validate EKS exists
	@if ! cd $(TF_EKS) && terraform output cluster_endpoint >/dev/null 2>&1; then \
		echo "ERROR: Layer 03 (EKS) must be applied first!"; \
		exit 1; \
	fi
	@# Validate Cilium is running (K8s prerequisite)
	@if ! kubectl get deployment cilium-operator -n kube-system >/dev/null 2>&1; then \
		echo "ERROR: Cilium must be installed first!"; \
		echo "Run: make cilium"; \
		exit 1; \
	fi
	cd $(TF_K8S_PLATFORM) && terraform apply -auto-approve
```

### Health Check Pattern

```makefile
# Internal health check targets (prefix with _)
_wait_lb_controller:
	@echo "Waiting for LB Controller CRD..."
	@timeout 300 bash -c 'until kubectl get crd targetgroupbindings.elbv2.k8s.aws >/dev/null 2>&1; do sleep 5; done'

_wait_pods_ready:
	@echo "Waiting for pods..."
	@timeout 600 bash -c 'until [ $$(kubectl get pods -n $(NAMESPACE) --field-selector=status.phase=Running --no-headers | wc -l) -gt 0 ]; do sleep 10; done'

# Usage in apply
lb-controller: _check_kubeconfig
	./scripts/setup-lb-controller.sh
	$(MAKE) _wait_lb_controller
```

### Logging Pattern

```makefile
apply:
	@mkdir -p $(LOGS_DIR)
	@LOG=$(LOGS_DIR)/apply_$$(date +%Y%m%d_%H%M%S).log && \
	echo "[STEP 1/10 STARTED] Layer 01 Foundation" | tee -a $$LOG && \
	( $(MAKE) tf-foundation ) >> $$LOG 2>&1 && \
	echo "[STEP 1/10 COMPLETED] Layer 01 Foundation" | tee -a $$LOG && \
	# ... continue with other steps
	echo "Deployment complete! Log: $$LOG"

# Monitor progress
log-status:
	@LATEST=$$(ls -t $(LOGS_DIR)/*.log 2>/dev/null | head -1); \
	COMPLETED=$$(grep -c '\[STEP.*COMPLETED\]' "$$LATEST" 2>/dev/null || echo 0); \
	echo "Progress: $$COMPLETED/10 steps completed"; \
	tail -5 "$$LATEST"
```

---

## Phase 5: Scripts Standards

### Script Template

Every script should follow this pattern:

```bash
#!/bin/bash
set -euo pipefail

# Description: What this script does
# Usage: ./script.sh [args]
# Prerequisites: What must exist before running

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration (with defaults)
PREFIX="${PREFIX:-tgp}"
REGION="${REGION:-us-east-2}"

# Functions
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
error() { log "ERROR: $*" >&2; exit 1; }

# Idempotency check
check_already_done() {
    # Return 0 if work already complete, 1 if needs to run
    # Example: Check if secret exists
    aws secretsmanager describe-secret --secret-id "$1" >/dev/null 2>&1
}

# Main logic
main() {
    log "Starting..."

    if check_already_done "$PREFIX-some-resource"; then
        log "Already exists, skipping"
        exit 0
    fi

    # Do the work
    log "Creating resource..."

    log "Complete"
}

main "$@"
```

### Wait/Health Check Script Pattern

```bash
#!/bin/bash
# scripts/wait-for-lb-controller.sh
set -euo pipefail

TIMEOUT=${TIMEOUT:-300}
INTERVAL=${INTERVAL:-5}

log() { echo "[$(date '+%H:%M:%S')] $*"; }

wait_for_crd() {
    local elapsed=0
    while ! kubectl get crd targetgroupbindings.elbv2.k8s.aws >/dev/null 2>&1; do
        if [ $elapsed -ge $TIMEOUT ]; then
            log "ERROR: Timeout waiting for CRD"
            exit 1
        fi
        log "Waiting for LB Controller CRD... (${elapsed}s/${TIMEOUT}s)"
        sleep $INTERVAL
        elapsed=$((elapsed + INTERVAL))
    done
    log "CRD ready"
}

wait_for_webhook() {
    local elapsed=0
    while ! kubectl get endpoints -n kube-system aws-load-balancer-webhook-service -o jsonpath='{.subsets[0].addresses[0].ip}' 2>/dev/null | grep -q .; do
        if [ $elapsed -ge $TIMEOUT ]; then
            log "ERROR: Timeout waiting for webhook"
            exit 1
        fi
        log "Waiting for webhook endpoint... (${elapsed}s/${TIMEOUT}s)"
        sleep $INTERVAL
        elapsed=$((elapsed + INTERVAL))
    done
    log "Webhook ready"
}

main() {
    log "Checking LB Controller health..."
    wait_for_crd
    wait_for_webhook
    log "LB Controller fully ready"
}

main
```

---

## Phase 6: Secrets Management

### Pattern: AWS Secrets Manager → Kubernetes

```bash
#!/bin/bash
# scripts/create-secrets.sh
set -euo pipefail

NAMESPACE="${NAMESPACE:-gitlab}"
PREFIX="${PREFIX:-tgp}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }

create_secret() {
    local name=$1
    local aws_secret=$2
    local key=${3:-password}

    log "Creating K8s secret: $name from AWS secret: $aws_secret"

    # Fetch from AWS Secrets Manager
    VALUE=$(aws secretsmanager get-secret-value \
        --secret-id "$aws_secret" \
        --query SecretString --output text)

    # Handle JSON secrets
    if echo "$VALUE" | jq -e . >/dev/null 2>&1; then
        VALUE=$(echo "$VALUE" | jq -r ".$key")
    fi

    # Create/update K8s secret (idempotent)
    kubectl create secret generic "$name" \
        --from-literal="$key=$VALUE" \
        --namespace "$NAMESPACE" \
        --dry-run=client -o yaml | kubectl apply -f -
}

main() {
    log "Creating Kubernetes secrets from AWS Secrets Manager..."

    # Ensure namespace exists
    kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

    # Create each secret
    create_secret "postgres-secret" "${PREFIX}-db-password" "password"
    create_secret "redis-secret" "${PREFIX}-redis-password" "password"
    create_secret "smtp-secret" "${PREFIX}-ses-smtp-credentials" "password"

    log "All secrets created"
}

main
```

---

## Phase 7: Common Issues & Solutions

### Issue: Windows Git Bash Path Conversion

**Symptom**: `terraform import` fails with paths like `C:/Program Files/Git/aws/...`

**Cause**: Git Bash converts `/aws/...` paths to Windows paths

**Solution**: Always prefix with `MSYS_NO_PATHCONV=1`
```bash
MSYS_NO_PATHCONV=1 terraform import aws_cloudwatch_log_group.example /aws/vpc/flow-logs
```

### Issue: Secrets Manager Deletion Recovery Window

**Symptom**: "Secret already scheduled for deletion" error

**Cause**: Secrets have 7-day recovery window

**Solution**: Restore before recreating
```bash
aws secretsmanager restore-secret --secret-id tgp-db-password
```

### Issue: EKS API Unreachable

**Symptom**: `dial tcp x.x.x.x:443: i/o timeout`

**Cause**: Deployer IP not in EKS public access CIDR list

**Solution**: Add IP to `terraform/03-eks/variables.tf`:
```hcl
eks_public_access_cidrs = [
  { cidr = "YOUR.IP.HERE/32", description = "Deployer machine" },
]
```

### Issue: Helm Stuck in pending-install

**Symptom**: Helm operations fail, release in bad state

**Solution**: Clean up before retry
```bash
helm uninstall RELEASE_NAME -n NAMESPACE --wait 2>/dev/null || true
```

### Issue: Orphaned AWS Resources

**Symptom**: "already exists" errors during apply

**Cause**: Resources exist in AWS but not in Terraform state

**Solution**: Import or delete
```bash
# Check what exists
aws resourcegroupstaggingapi get-resources --tag-filters Key=Project,Values=tgp

# Import into Terraform
terraform import aws_s3_bucket.example bucket-name
```

---

## Phase 8: Project Instructions File

Create an AI instruction file using your assistant's format:

| AI Assistant | File Location | Format |
|--------------|---------------|--------|
| Claude Code | `.claude/CLAUDE.md` | Markdown |
| Cursor | `.cursorrules` | Plain text or Markdown |
| GitHub Copilot | `.github/copilot-instructions.md` | Markdown |
| Aider | `CONVENTIONS.md` or `.aider.conf.yml` | Markdown or YAML |
| Windsurf | `.windsurfrules` | Markdown |
| Generic | `AI_INSTRUCTIONS.md` | Markdown |

### Template (adapt to your format):

```markdown
# [Project Name] - Project Instructions

## Project Overview

This project deploys [Application] on AWS EKS using Terraform (split-state) and Helm.

## Terraform Split-State Architecture

| Layer | Path | Contents |
|-------|------|----------|
| 01-foundation | `terraform/01-foundation/` | VPC, S3, KMS, ACM |
| 02-data | `terraform/02-data/` | RDS, ElastiCache |
| 03-eks | `terraform/03-eks/` | EKS, IAM, NLB, VPN |
| 04-k8s-platform | `terraform/04-k8s-platform/` | Addons, Autoscaler |
| 05-edge | `terraform/05-edge/` | CloudFront, WAF |

## Quick Commands

```bash
make help           # Show all commands
make apply          # Full deployment
make destroy        # Full teardown
make tf-status      # Show layer states
make status         # Show K8s status
```

## Key Files

- `Makefile` - Main workflow orchestration
- `helm/values-*.yaml` - Helm configuration
- `scripts/create-secrets.sh` - Secrets sync

## Deployment Workflow

1. Layer 01 (Foundation)
2. Layer 02 (Data)
3. Layer 03 (EKS)
4. Setup VPN (interactive)
5. Install Cilium CNI
6. Layer 04 (K8s Platform)
7. Install LB Controller
8. Create Kubernetes secrets
9. Install Helm chart
10. Layer 05 (Edge)

## Lessons Learned

### Config Fix = Full Codebase Search

When fixing configuration values:
1. Search entire codebase for the pattern
2. Check docs, scripts, AND config files
3. Verify naming matches Terraform source of truth
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | What To Do Instead |
|--------------|--------------|---------------------|
| Manual fixes (terraform import, kubectl apply) | Don't recur, create tribal knowledge | Fix the automation code |
| Running without MSYS_NO_PATHCONV on Windows | Git Bash mangles /aws/* paths | Always set env var |
| Ignoring orphaned AWS resources | "Already exists" errors block deploy | Search and import/delete |
| Destroying and immediately redeploying | Secrets in deletion recovery window | Restore secrets first |
| Assuming office IPs can access EKS | Deployment from new location fails | Add deployer IP to CIDR list |
| Running Helm without prerequisites | Mount errors, auth failures | Verify secrets, CRDs exist |
| Full automation without checkpoints | Can't resume after failures | Use logging, /compact points |

---

## Expert Agent Prompts

Use these prompts to spawn specialized agents at different phases. Replace `[APP_NAME]` and `[PROJECT_PATH]` with actual values.

### Discovery Phase: Application Requirements Agent

```
You are an application requirements analyst. Your task is to discover what
infrastructure an application needs WITHOUT asking the user.

Analyze the following for the application "[APP_NAME]":

1. **Documentation Analysis**
   - Read the official installation docs
   - Identify required services (database, cache, storage, etc.)
   - Note minimum resource requirements

2. **Helm Chart Analysis** (if applicable)
   - Read values.yaml for external service dependencies
   - Identify persistent volume requirements
   - Note any init containers or sidecar patterns

3. **Reference Architecture Research**
   - Search for "[APP_NAME] AWS architecture" or "production deployment"
   - Identify common patterns from official or community sources

4. **Output Format**
   Return a structured list:
   - Required services (with justification)
   - Optional services (with use case)
   - Recommended instance sizes
   - Storage requirements
   - Network requirements (public/private, VPN, etc.)

DO NOT ask the user. Discover and recommend.
```

### Discovery Phase: Security Requirements Agent

```
You are an AWS security architect. Analyze the application and infrastructure
requirements to recommend security controls.

For the application "[APP_NAME]" deploying to AWS EKS:

1. **Network Security**
   - Should the EKS API be public or private?
   - What CIDR restrictions are needed?
   - Is a VPN required? (WireGuard vs AWS Client VPN trade-offs)
   - What security groups are needed?

2. **Secrets Management**
   - What secrets does the application need?
   - Recommend AWS Secrets Manager structure
   - Define rotation requirements
   - Plan K8s secrets sync strategy

3. **IAM Strategy**
   - Define IRSA roles for each component
   - Recommend permission boundaries
   - Identify least-privilege policies

4. **Encryption**
   - KMS key requirements (RDS, S3, EBS, Secrets Manager)
   - In-transit encryption requirements
   - Certificate management (ACM)

5. **Compliance Considerations**
   - Audit logging requirements (CloudTrail, EKS audit logs)
   - Data residency constraints
   - Backup and recovery requirements

Output a security requirements document with specific Terraform resources to create.
```

### Structure Phase: Architecture Review Agent

```
You are a Terraform architecture reviewer. Analyze the proposed repository
structure and layer organization.

Review criteria:

1. **Layer Boundaries**
   - Is each layer focused on a single concern?
   - Are stateful resources (RDS, ElastiCache) isolated from compute?
   - Is the blast radius minimized for each layer?

2. **Dependency Graph**
   - Are dependencies one-directional (no cycles)?
   - Can each layer be destroyed independently (in reverse order)?
   - Are cross-layer references using terraform_remote_state correctly?

3. **Output Design**
   - Are outputs named consistently?
   - Are sensitive outputs marked appropriately?
   - Do downstream layers have access to what they need?

4. **State Isolation**
   - Is each layer's state in a separate S3 key?
   - Can different teams operate on different layers?
   - Is the state bucket properly secured?

5. **Makefile Orchestration**
   - Do targets validate dependencies before running?
   - Are health checks in place between layers?
   - Is the apply/destroy order enforced?

Output: List of issues (blocking vs advisory) with specific fixes.
```

### Structure Phase: Makefile Review Agent

```
You are a DevOps engineer specializing in Makefile-based workflows.

Review the Makefile for:

1. **Idempotency**
   - Can every target be safely re-run?
   - Are there cleanup steps that might fail on first run?
   - Do Helm operations use upgrade --install pattern?

2. **Dependency Validation**
   - Does each layer check prerequisites before applying?
   - Are error messages actionable ("Run: make X first")?
   - Are K8s dependencies (CNI, CRDs) validated?

3. **Error Handling**
   - Do long operations have timeouts?
   - Is there logging to files for debugging?
   - Can failed deployments be resumed?

4. **Usability**
   - Is `make help` comprehensive?
   - Are target names intuitive?
   - Is the deployment order documented?

5. **AI/Pair-Programming Compatibility**
   - Are outputs parseable (step markers, progress)?
   - Is there a status/log-status target?
   - Can progress be monitored during long operations?

Output: Specific improvements with code examples.
```

### Post-Completion: Adversarial Review Agent

```
You are a hostile reviewer. Your job is to FIND PROBLEMS, not validate success.
Assume the deployment will fail and find out why.

Attack vectors to explore:

1. **State Corruption Scenarios**
   - What happens if Terraform state is deleted mid-apply?
   - What if S3 state bucket is inaccessible?
   - Can orphaned resources be recovered?

2. **Partial Failure Modes**
   - What if Layer 02 fails after Layer 01 succeeds?
   - What if Helm install fails after secrets are created?
   - What if the deployer loses network mid-apply?

3. **Security Weaknesses**
   - Are there any hardcoded secrets or credentials?
   - Can the EKS API be accessed from unauthorized IPs?
   - Are IAM roles over-permissioned?
   - Is there sensitive data in Terraform outputs?

4. **Operational Gaps**
   - What happens when secrets need rotation?
   - How is disaster recovery handled?
   - What's the rollback procedure for a bad Helm release?
   - Are there any manual steps hidden in "automated" workflows?

5. **Edge Cases**
   - What if AWS API rate limits are hit?
   - What if the Helm chart version is incompatible?
   - What if node groups scale to zero?
   - What if Cilium agents crash on all nodes?

6. **Documentation Gaps**
   - What knowledge is assumed but not documented?
   - Are troubleshooting steps complete?
   - Would a new team member be able to deploy from scratch?

Output format:
- CRITICAL: Must fix before production
- HIGH: Should fix before production
- MEDIUM: Fix when convenient
- LOW: Nice to have

For each issue, provide:
- Problem description
- How to reproduce/trigger
- Recommended fix
- Files to modify
```

### Post-Completion: Runbook Validation Agent

```
You are a new team member who has never seen this project. Your job is to
validate that the documentation is complete enough for someone to:

1. **Deploy from scratch** - Follow the README and Makefile help
2. **Troubleshoot common issues** - Use TROUBLESHOOTING.md
3. **Recover from failures** - Understand rollback procedures
4. **Onboard new deployers** - Set up VPN access, credentials

Test each runbook by:
- Reading ONLY the documentation (no code spelunking)
- Identifying any steps that say "you should know" or assume knowledge
- Finding missing prerequisites
- Noting unclear or ambiguous instructions

Output:
- List of documentation gaps
- Suggested additions to each doc
- Questions a new user would have
```

### Post-Completion: Cost Review Agent

```
You are a FinOps engineer. Review the Terraform configuration for cost
optimization opportunities.

Analyze:

1. **Right-sizing**
   - Are RDS instance sizes appropriate for the workload?
   - Are EKS node groups using appropriate instance types?
   - Is there over-provisioning "just in case"?

2. **Reserved Capacity**
   - Which resources are candidates for Reserved Instances/Savings Plans?
   - Are there any Spot Instance opportunities (non-critical workloads)?

3. **Storage Costs**
   - Are S3 lifecycle policies configured?
   - Is EBS storage type appropriate (gp3 vs gp2)?
   - Are old snapshots being cleaned up?

4. **Network Costs**
   - Is NAT Gateway traffic optimized?
   - Are there cross-AZ data transfer costs that could be reduced?
   - Is CloudFront caching configured optimally?

5. **Unused Resources**
   - Are there any resources provisioned but not used?
   - Are dev/staging environments running 24/7 unnecessarily?

Output: Cost optimization recommendations with estimated savings.
```

---

## Checklist for New Repo

- [ ] Directory structure created
- [ ] Terraform layers 01-05 scaffolded
- [ ] Makefile with help, apply, destroy, status
- [ ] scripts/bootstrap-terraform.sh
- [ ] scripts/create-secrets.sh
- [ ] .gitignore (terraform, secrets, logs)
- [ ] Dependency validation in Makefile
- [ ] Health check scripts
- [ ] Logging in apply/destroy targets
- [ ] AI instruction file created (see Phase 8)

---

## Usage

1. **Adapt this prompt** to your AI assistant (see "AI Assistant: Adapt This Prompt")
2. **Answer Phase 1 questions** - Project identity and environment strategy
3. **Run discovery agents** - Let AI determine infrastructure requirements
4. **Scaffold repository** - AI creates structure from Phase 2
5. **Iterate on each layer** - Build and test incrementally
6. **Run adversarial review** - Use post-completion agents to find issues
7. **Add troubleshooting entries** - Document issues as they arise

### Workflow by Phase

```
┌─────────────────────────────────────────────────────────────────┐
│  DISCOVERY PHASE                                                │
│  ├── Application Requirements Agent                            │
│  └── Security Requirements Agent                                │
├─────────────────────────────────────────────────────────────────┤
│  STRUCTURE PHASE                                                │
│  ├── Create directory structure (Phase 2)                       │
│  ├── Scaffold Terraform layers (Phase 3)                        │
│  ├── Build Makefile (Phase 4)                                   │
│  ├── Write scripts (Phase 5)                                    │
│  ├── Architecture Review Agent                                  │
│  └── Makefile Review Agent                                      │
├─────────────────────────────────────────────────────────────────┤
│  IMPLEMENTATION PHASE                                           │
│  ├── Build each layer, test with `terraform plan`               │
│  ├── Create secrets management (Phase 6)                        │
│  └── Write project instruction file (Phase 8)                   │
├─────────────────────────────────────────────────────────────────┤
│  VALIDATION PHASE                                               │
│  ├── Adversarial Review Agent                                   │
│  ├── Runbook Validation Agent                                   │
│  └── Cost Review Agent                                          │
└─────────────────────────────────────────────────────────────────┘
```
