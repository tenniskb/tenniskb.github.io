# Claude-TNKB — Tennis Knowledge Base (Consolidated)

This repo is the consolidated working copy of Henry's tennis knowledge base expansion project, created 2026-07-22. It brings together content that was previously scattered across three separate repos (`tenniskb`, `tennisknowledgebase`, `tenniskb-1`) plus a local Obsidian-style vault, following the plan in `Tennis-KB-Expansion-IA-Spec.md`.

## Structure

- `Foundation/`, `Advanced/`, `Elite/` — the three-tier site content (Basics + Deep-Dives, En + Vi), reconciled from tenniskb's live repo and the local vault. This is the actual knowledge-base content.
- `Science-Lab/` — anatomy-lab and angle-atlas deep-dives, ported from tennisknowledgebase (previously buried under Elite-only navigation).
- `Site-New-Sections/` — the `players` and `system/drill-visualizer` sections, also ported from tennisknowledgebase.
- `New-documents/` — raw and coach-voice-rewritten source manuals from the vault, including `tenniskb-1-new-sources/` (Advanced Adaptive Tennis System, Arm Configuration Biomechanics, Big Loop/Compact Loop, Grip Change Map).
- `Tennis-KB-Expansion-IA-Spec.md` — the full information-architecture spec: vision, current-state audit, audience segmentation, source inventory, site map, content standards, 16-phase roadmap, and open items. Start here.
- The other root-level `.md` files are prior planning documents kept for historical reference.

## Status

Content reconciliation (Section 8 of the spec) is done for the structural port — topics are in their correct tier, the two mis-tiered Elite topics were relocated, and the missing tenniskb-only/tennisknowledgebase-only topics were added. Known outstanding items:

- Some deep-dive topics carry a duplicate folder + flat-file pair (inherited from tenniskb's own repo structure) — cosmetic, not yet cleaned up.
- Naming-drift cosmetics (e.g. "Fascia Spirals" vs. "Fascia Spiral", "&" vs. "and") not yet normalized.
- This is currently raw markdown served as-is (no MkDocs build yet) — what you're reading at [tenniskb.github.io/tnkb](https://tenniskb.github.io/tnkb/) is this README, not a built site. Turning it into an actual navigable site (Section 8's publishing plan) is still ahead.

See the spec's Section 9 (Open Items) for the full list.
