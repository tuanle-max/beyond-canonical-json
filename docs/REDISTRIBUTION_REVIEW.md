# Redistribution Review

## Finding
Inspection of the public archives shows **dependency declarations only** (`go.mod`/`go.sum`) and one **first-party compiled Go binary** (`implementations/go-dev/boo`, built from the first-party `main.go`). No embedded third-party source packages are vendored in the archives. Python dependencies (e.g., `rfc8785`, `cryptography`) are imports resolved from the environment, not bundled.

## Decision
No third-party source is redistributed, so no third-party redistribution condition is triggered by this release. Module references in `go.sum` must be retrieved upstream under their own licenses when rebuilding. Third-party names/licenses are not relicensed here. Compiled `boo` is first-party.

## Residual
If a reviewer requires omission of the compiled binary, it is reconstructible from `main.go` via `go build`; it is not read by the authoritative or public verification. Current release retains it (first-party).

## CORRECTION (Patch 1)
The earlier statement that the release embedded no third-party source was INCORRECT. `go version -m` shows the compiled `boo` binary embeds `github.com/gowebpki/jcs v1.0.1` (Apache-2.0) and `golang.org/x/text v0.19.0` (BSD-3-Clause), plus the Go 1.23.12 runtime (BSD-3-Clause + PATENTS). This patch supplies the required license/notice materials and satisfies redistribution obligations for the corrected distribution. The superseded tag v1.0.0-artifact remains notice-incomplete and is NOT claimed compliant.
