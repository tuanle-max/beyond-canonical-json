# BCJ-V19 Research Artifacts v1.0.0 - Licensing Notices Patch 1

**Publication-compliance patch, not a new scientific evaluation.**

- Adds `THIRD_PARTY_NOTICES.md` and `third_party_licenses/` for third-party modules embedded in the compiled `boo` binary (github.com/gowebpki/jcs v1.0.1, Apache-2.0; golang.org/x/text v0.19.0, BSD-3-Clause; Go 1.23.12 runtime, BSD-3-Clause + PATENTS).
- No scientific evidence or experimental result changed; all eight evidence archive identities are unchanged.
- Supersedes v1.0.0-artifact (which omitted these notices) as the recommended distribution; the original tag is unchanged.
- No new blanket license is granted for the authors' original research materials.

Verify: `python verify_v19_public_release.py experiments/v19` (exit 0). Level 2 PARTIAL; Level 3 NOT_EXECUTED; archival verification only.
