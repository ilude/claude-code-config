# Archive Reprocessing System

**Auto-activates when**: Working with `tools/scripts/lib/`, reprocessing scripts, transform versions, or discussing archive transformations.

## Quick Reference

**When to use reprocessing:**
- Applying new transformations to existing archives (flattening, normalization)
- After bumping transformation versions (v1.0 → v1.1)
- After vocabulary updates (v1 → v2)
- After model changes (haiku → sonnet)
- Regenerating derived outputs (free to recompute)

**When NOT to use:**
- Adding new videos → use `ingest_youtube.py`
- Rebuilding Qdrant cache from scratch → use `reingest_from_archive.py` (for now)

## System Overview

Flexible, version-tracked reprocessing system using design patterns:
- **Strategy pattern**: Pluggable metadata transformers (eliminate copy-paste)
- **Template Method**: Reusable reprocessing workflows
- **Observer pattern**: Progress hooks (console, metrics)

**Key feature**: Incremental processing with semantic versioning that works during active development (not git-dependent).

## Core Components

### 1. Version Registry (`tools/scripts/lib/transform_versions.py`)

Central source of truth for all transformation versions:

```python
VERSIONS = {
    "normalizer": "v1.0",        # Tag normalization logic
    "vocabulary": "v1",           # Vocabulary version
    "qdrant_flattener": "v1.0",   # Metadata flattening
    "weight_calculator": "v1.0",  # Recommendation weights
    "llm_model": "claude-3-5-haiku-20241022",
}
```

**When to bump versions:**
- Logic change: `normalizer v1.0 → v1.1`
- Vocabulary update: `vocabulary v1 → v2`
- Breaking change: `v1.x → v2.0`

### 2. Metadata Transformers (`tools/scripts/lib/metadata_transformers.py`)

Strategy pattern for reusable transformations:

```python
from tools.scripts.lib.metadata_transformers import (
    QdrantMetadataFlattener,
    RecommendationWeightCalculator,
    create_qdrant_transformer,
)

# Pre-built transformer
transformer = create_qdrant_transformer()
metadata = transformer.transform(archive_data)

# Custom transformer
class MyTransformer(BaseTransformer):
    def get_version(self) -> str:
        return get_version("my_transformer")

    def transform(self, archive_data: dict) -> dict:
        return {"transformed": True}
```

### 3. Reprocessing Pipeline (`tools/scripts/lib/reprocessing_pipeline.py`)

Template Method base class for workflows:

```python
from tools.scripts.lib.reprocessing_pipeline import (
    BaseReprocessingPipeline,
    ConsoleHooks,
)

class MyPipeline(BaseReprocessingPipeline):
    def get_output_type(self) -> str:
        return "my_transformation_v1"

    def get_version_keys(self) -> list[str]:
        return ["my_transformer"]

    def process_archive(self, archive: YouTubeArchive) -> str:
        # Your logic here
        return json.dumps(result)

# Run it
pipeline = MyPipeline(hooks=ConsoleHooks())
stats = pipeline.run(limit=10)
```

## Common Tasks

### Test Reprocessing (Dry Run)

```bash
# Qdrant metadata (fast, no LLM)
uv run python tools/scripts/reprocess_qdrant_metadata.py --dry-run --limit 10

# Tag normalization (slow, calls LLM)
uv run python tools/scripts/reprocess_normalized_tags.py --dry-run --limit 3
```

### Full Reprocessing

```bash
# Qdrant metadata (~12 minutes for 470 videos)
uv run python tools/scripts/reprocess_qdrant_metadata.py

# Tag normalization (~2 hours for 470 videos)
uv run python tools/scripts/reprocess_normalized_tags.py
```

### After Version Bump

```bash
# Edit version
vim tools/scripts/lib/transform_versions.py
# Change: "normalizer": "v1.1"  # was v1.0

# Reprocess (only processes stale archives)
uv run python tools/scripts/reprocess_normalized_tags.py
```

## Archive Data Structure

Archives track three types of outputs:

```json
{
  "llm_outputs": [
    {
      "output_type": "tags",
      "cost_usd": 0.0012,
      "model": "claude-3-5-haiku-20241022"
    }
  ],
  "derived_outputs": [
    {
      "output_type": "normalized_metadata_v1",
      "transformer_version": "v1.0+v1",
      "transform_manifest": {
        "normalizer": "v1.0",
        "vocabulary": "v1",
        "created_at": "2025-11-10T..."
      },
      "source_outputs": ["tags"]
    }
  ]
}
```

**Key difference:**
- `llm_outputs`: Cost money, archived permanently
- `derived_outputs`: Free to regenerate, version-tracked for staleness

## Incremental Processing

**How staleness detection works:**
1. Each `derived_output` stores `transform_manifest` (snapshot of versions)
2. When reprocessing, compare stored manifest to current `VERSIONS`
3. If any tracked version changed → reprocess
4. If all versions match → skip (up-to-date)

**Performance:**
- First run: Process all 470 videos (~12min for Qdrant, ~2hr for normalization)
- Subsequent runs: ~5s (skips all if up-to-date)
- After version bump: Only reprocesses affected archives

## Built-in Reprocessing Scripts

### reprocess_qdrant_metadata.py

Applies `QdrantMetadataFlattener + RecommendationWeightCalculator`:
- Flattens tags → boolean filter fields (`subject_ai_agents=True`)
- Calculates recommendation weights (bulk=0.5, single=1.0)
- Fast (no LLM calls)

### reprocess_normalized_tags.py

Applies lesson-010 tag normalization:
- Two-phase normalization (raw → normalized)
- Semantic context from Qdrant
- Vocabulary consistency
- Slow (LLM calls per video)

Options:
- `--no-context`: Skip semantic retrieval (faster, lower quality)
- `--no-vocabulary`: Skip vocabulary normalization

## Creating New Transformations

### 1. Add Version to Registry

```python
# tools/scripts/lib/transform_versions.py
VERSIONS = {
    "my_transformer": "v1.0",  # Add this
}
```

### 2. Create Transformer

```python
# tools/scripts/lib/metadata_transformers.py or new file
class MyTransformer(BaseTransformer):
    def get_version(self) -> str:
        return get_version("my_transformer")

    def get_dependencies(self) -> list[str]:
        return ["vocabulary", "llm_model"]

    def transform(self, archive_data: dict) -> dict:
        # Your transformation logic
        return {"result": "value"}
```

### 3. Create Reprocessing Script

```python
# tools/scripts/reprocess_my_transformation.py
class MyReprocessor(BaseReprocessingPipeline):
    def get_output_type(self) -> str:
        return "my_output_v1"

    def get_version_keys(self) -> list[str]:
        return ["my_transformer"]

    def process_archive(self, archive: YouTubeArchive) -> str:
        transformer = MyTransformer()
        result = transformer.transform(archive.model_dump())
        return json.dumps(result)
```

## Integration with Archive Service

Archive service automatically supports derived outputs:

```python
from tools.services.archive import create_local_archive_writer
from tools.scripts.lib.transform_versions import get_transform_manifest

archive_writer = create_local_archive_writer()

# Add derived output
archive_writer.add_derived_output(
    video_id="abc123",
    output_type="my_transformation_v1",
    output_value=json.dumps(result),
    transformer_version="v1.0",
    transform_manifest=get_transform_manifest(),
    source_outputs=["tags"],
)

# Retrieve
archive = archive_writer.get("abc123")
derived = archive.get_latest_derived_output("my_transformation_v1")
```

## Observer Hooks

Add custom progress tracking:

```python
class MetricsHooks:
    def on_start(self, total: int):
        print(f"Starting {total} archives")

    def on_archive_success(self, video_id: str, elapsed: float):
        print(f"{video_id}: {elapsed:.2f}s")

    def on_complete(self, stats: dict):
        print(f"Done: {stats}")

pipeline = MyPipeline(hooks=MetricsHooks())
```

## Comparison to Old Approach

**Before (`reingest_from_archive.py`):**
- ❌ Hardcoded transformation logic
- ❌ Copy-pasted flattening code across 3+ scripts
- ❌ No version tracking
- ❌ Regenerates everything (wasteful)

**After (reprocessing system):**
- ✅ Strategy pattern (reusable transformers)
- ✅ Single source of truth
- ✅ Semantic version tracking
- ✅ Incremental processing (skip unchanged)
- ✅ Template Method (consistent workflows)
- ✅ Observer hooks (visibility)

## Documentation

Full docs available:
- `tools/scripts/lib/README.md`: Complete system documentation
- `tools/scripts/lib/QUICKSTART.md`: Quick reference
- `lessons/lesson-010/COMPLETE.md`: Tag normalization lesson

## Design Philosophy

**Fail-fast, experiment-driven:**
- Semantic versioning works during development (not git-dependent)
- Simple enough to understand, flexible enough to extend
- Incremental is the win (not parallelization)
- Strategy/Template patterns eliminate copy-paste
- Observer hooks provide visibility

**Non-goals:**
- Distributed processing (single machine is fine)
- Map-reduce patterns (over-engineering)
- Git integration (semantic versions better for iteration)
