# Release completeness audit — 2026-11-05

The owner reported a real Cloud BBT defect and two disabled custom voice buttons. This audit separates source preservation, integration into main, deployment and acceptance.

- Four historical source trees/backups were compared with the designated release checkout: 250 files inspected. Every runtime source file in those copies has a counterpart in the release. The one absent file is a historical legal-source-watch report, now preserved under `docs/historical/`.
- Three commits were previously reachable only from local branches: `aeef17b`, `0b3950f`, `dbc886a`. They are now pushed to their named branches. No local branch commit remains absent from origin.
- Seven older branches still have commits outside main ancestry. Their file-level reconciliation is in the JSON inventory. This is not permission to merge all prototypes: several use removed legacy modules and must be reconciled against newer contracts.
- Older `numeric_answer_matches` and `paired_statistics` definitions were moved to `qa_runtime`; current callers import them. They are not missing features.
- PR94 fixes the newly reported named-function BBT rendering paths. Its local targeted tests and CI passed; Cloud acceptance is separate. The owner's previously approved local infographic layout remains closed.
- The two custom Cloud voices have no configured HTTPS backend. Local voice playback evidence does not satisfy the independent, cross-device Cloud requirement. No owner-PC public tunnel has been opened.
- After dashboard reboot, a fresh Cloud tab loaded the Station 1 Math 12 form with no visible exception or connecting banner. The served commit, BBT repair and custom voices are not yet accepted. No new lesson was generated. The actual displayed Math Part1 and full displayed lesson were preserved before recovery.

## Integration items still requiring reconciliation

1. `codex/math12-basic-survey-method`: legacy academic-scope guard is absent as a module in main; compare its actual requirements with current policy/runtime checks before restoring behavior.
2. `codex/socratic-boundaries`: legacy lesson-contract module is absent; current Socratic context checks need behavior-level mapping, not blind copying.
3. `codex/t3-confirm-latency`: old WIP callback patch overlaps newer context-scoped request widgets; preserve the newer context isolation when reconciling latency changes.
4. `codex/unified-pedagogical-speech`: prototype files are now preserved remotely, but are not the deployed independent custom-voice service.
5. BBT readability and PR6 recovery branches overlap current renderers/context modules; retain the current fixes and record any uncovered behavior separately.

No global academic acceptance or all-device voice acceptance is claimed by this inventory.
