# Plan: Documentation & Script Improvements

## Scope
- Fix documentation errors and contradictions
- Consolidate prerequisites into single authoritative source
- Improve PowerShell scripts (validation, dynamic values)
- Add IronBank registry documentation to user-facing docs
- Document local Bun installation purpose
- Update eisa-ng/README.md with project-specific content

---

## 1. Documentation Fixes

### 1.1 Fix Path Inconsistency (Critical)
**File:** `C:\Projects\Gitlab\eisa\docs\workflows\BUN.md`
- Line 133: Change `.\setup\setup-windows.ps1` → `.\setup-windows.ps1`

### 1.2 Fix README vs SETUP-GUIDE Contradiction
**File:** `C:\Projects\Gitlab\eisa\README.md`
- Change `make start` → `make up` for first-time setup (matches SETUP-GUIDE recommendation)
- Add note: "Use `make start` for subsequent runs (background mode)"

### 1.3 Add IronBank Registry Section to SETUP-GUIDE
**File:** `C:\Projects\Gitlab\eisa\docs\setup\SETUP-GUIDE.md`
- Add new section explaining:
  - Local dev uses IronBank images (requires DoD CAC/credentials)
  - CI uses Red Hat images (different auth - CI has subscription credentials)
  - If you get Red Hat login prompts, check `docker-compose.override.yml` has `<<: *dev-images`

### 1.4 Document Local Bun Purpose
**File:** `C:\Projects\Gitlab\eisa\docs\workflows\BUN.md`
- Clarify why setup-windows.ps1 installs Bun locally:
  - IDE intellisense for package.json
  - Running Angular CLI commands outside Docker
  - Quick package.json edits without rebuilding
  - Non-Docker development scenarios (rare but supported)

### 1.5 Consolidate Prerequisites (Single Authoritative Source)
**File:** `C:\Projects\Gitlab\eisa\docs\setup\SETUP-GUIDE.md`
- Create comprehensive prerequisites section with explicit versions:
  - Windows 10/11 with WSL2
  - Docker Desktop (latest)
  - .NET 8.0 SDK (8.0.119 per global.json)
  - Git for Windows
  - GNU Make (installed by setup script)
  - PowerShell 7 (installed by setup script)
- Add verification checklist:
  - `docker --version`
  - `dotnet --version` (should show 8.0.x)
  - `make --version`
  - `git --version`
- Reference this from README.md instead of duplicating

### 1.6 Document Environment Variables
**File:** `C:\Projects\Gitlab\eisa\docs\setup\SETUP-GUIDE.md`
- Add section on `.env` file configuration
- Document `SKIP_CLIENT_BUILD=true` for backend-only development
- Note that default credentials in .env are for local dev only

### 1.7 Update eisa-ng/README.md
**File:** `C:\Projects\Gitlab\eisa\eisa-ng\README.md`
- Replace auto-generated Angular CLI boilerplate with project-specific content:
  - EISA Angular 17 frontend overview
  - How it integrates with .NET backend services
  - Reference docs/workflows/BUN.md for package management
  - Quick commands reference (build, serve, test)

---

## 2. Script Fixes

### 2.1 really-clean.ps1 - Dynamic Volume Discovery
**File:** `C:\Projects\Gitlab\eisa\really-clean.ps1`
- Replace hard-coded volume names with dynamic discovery:
  ```powershell
  # Instead of: @('eisa_eisa-ng-node_modules', 'eisa_eisa-ng-bun-cache')
  # Use: docker volume ls --filter "name=eisa" -q
  ```

### 2.2 really-clean.ps1 - Add dotnet Validation
**File:** `C:\Projects\Gitlab\eisa\really-clean.ps1`
- Add early check for dotnet CLI availability before cleanup steps

### 2.3 setup-windows.ps1 - Document Error Codes
**File:** `C:\Projects\Gitlab\eisa\setup-windows.ps1`
- Add comments explaining Windows error codes:
  - `-1978335189` = package already installed
  - `-1978335212` = package not found

---

## 3. Files to Modify

| File | Changes |
|------|---------|
| `docs/workflows/BUN.md` | Fix path, document local Bun purpose |
| `docs/setup/SETUP-GUIDE.md` | Add IronBank section, consolidate prerequisites, .env docs |
| `README.md` | Fix make start → make up, reference SETUP-GUIDE for prerequisites |
| `eisa-ng/README.md` | Replace boilerplate with project-specific Angular content |
| `really-clean.ps1` | Dynamic volumes, add dotnet check |
| `setup-windows.ps1` | Document error codes |

---

## 4. Implementation Order

1. **Documentation fixes first** (lower risk)
   - BUN.md path fix
   - README.md contradiction fix
   - SETUP-GUIDE.md additions (IronBank, prerequisites, .env)
   - eisa-ng/README.md update

2. **Script fixes second** (test after each change)
   - setup-windows.ps1 comments only (safe)
   - really-clean.ps1 improvements

---

## 5. Not In Scope
- CONTRIBUTING.md creation
- docs/README.md index file
