# CertLeap Academy Phase 3 Implementation Plan

## Scope

Phase 3 is intentionally split into two independently verifiable parts.

### 3A - Windows installer identity fix

1. Add regression tests proving that Windows display name, executable identity, service identity, and URI scheme are independent values.
2. Introduce one Windows installer identity module with these stable values:
   - Display name: `CertLeap Academy` (existing app display name remains the UI source of truth)
   - Executable stem: `certleap_academy`
   - Service name: `certleap`
   - URI scheme: `certleap`
3. Replace installer/runtime uses that incorrectly derive executable, service, or URI names from `get_app_name()`.
4. Keep `get_app_name()` for human-visible labels such as Start Menu folder, shortcut names, window title, DisplayName and uninstall display name.
5. Rename the self-extracting `.exe` release artifact as Portable; treat MSI as the canonical Windows Setup artifact.
6. Verify targeted identity tests, Windows Rust/build checks, MSI compile, and fresh-install/uninstall command generation.

### 3B - CertLeap server primary/fallback profile

1. Add tests for an explicit primary/fallback server-profile state machine before implementation.
2. Keep ID Server + Relay Server + Key as one atomic profile.
3. Default to the CertLeap private profile when configured.
4. Fail over only after repeated primary registration/connectivity failures, not by latency racing public and private servers concurrently.
5. While on fallback, periodically probe primary and fail back only after consecutive successful probes (hysteresis).
6. Keep existing upstream/public server behavior as fallback when the private profile is unavailable.
7. Apply the same profile behavior to Windows and Android through shared Rust core logic.
8. Add logs for profile transitions without logging the key.
9. Verify primary-up, primary-down, recovery, relay pairing, key pairing, Android build, Windows build, and Rust tests.

## Order / gates

- Complete and verify 3A before starting 3B.
- Do not merge Phase 3 into the stable branch until all applicable gates pass.
- Do not change macOS/Linux branding as part of this phase.
- Preserve technical RustDesk ABI/dependency identifiers unless a user-facing/runtime identity bug requires changing them.
