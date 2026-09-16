from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def require_count(path: str, text: str, needle: str, expected: int = 1) -> None:
    count = text.count(needle)
    if count != expected:
        raise RuntimeError(
            f"{path}: expected {expected} occurrence(s) of {needle!r}, found {count}"
        )


# Mobile update prompt: keep the update notice but remove the upstream download action.
path = "flutter/lib/mobile/pages/connection_page.dart"
text = read(path)
text = text.replace("import 'package:url_launcher/url_launcher.dart';\n", "", 1)
start = text.index("  Widget _buildUpdateUI(String updateUrl) {")
end = text.index("\n  }", start) + len("\n  }")
new_method = """  Widget _buildUpdateUI(String updateUrl) {
    return updateUrl.isEmpty
        ? const SizedBox(height: 0)
        : Container(
            alignment: AlignmentDirectional.center,
            width: double.infinity,
            color: Colors.pinkAccent,
            padding: const EdgeInsets.symmetric(vertical: 12),
            child: Text(translate('Download new version'),
                style: const TextStyle(
                    color: Colors.white, fontWeight: FontWeight.bold)));
  }"""
text = text[:start] + new_method + text[end:]
write(path, text)
print(f"updated {path}")

# Desktop public-server upsell pointed to RustDesk pricing; hide it until a CertLeap URL is configured.
path = "flutter/lib/desktop/pages/connection_page.dart"
text = read(path)
require_count(path, text, "import 'package:url_launcher/url_launcher_string.dart';\n")
text = text.replace("import 'package:url_launcher/url_launcher_string.dart';\n", "", 1)
start = text.index("  void onUsePublicServerGuide() {")
end = text.index("\n  }", start) + len("\n  }")
text = text[:start] + text[end + 1 :]
start = text.index("    setupServerWidget() =>")
end = text.index("    basicWidget() =>", start)
text = text[:start] + "    setupServerWidget() => const SizedBox.shrink();\n\n" + text[end:]
write(path, text)
print(f"updated {path}")

# Desktop update/help cards: remove upstream download, changelog and Linux documentation links.
path = "flutter/lib/desktop/pages/desktop_home_page.dart"
text = read(path)
old = """      String btnText = isToUpdate ? 'Update' : 'Download';
      GestureTapCallback onPressed = () async {
        final Uri url = Uri.parse('https://rustdesk.com/download');
        await launchUrl(url);
      };
"""
new = """      String btnText = isToUpdate ? 'Update' : '';
      GestureTapCallback onPressed = () {};
"""
require_count(path, text, old)
text = text.replace(old, new, 1)
old = """          help: isToUpdate ? 'Changelog' : null,
          link: isToUpdate
              ? 'https://github.com/rustdesk/rustdesk/releases/tag/${bind.mainGetNewVersion()}'
              : null);"""
new = """          help: null,
          link: null);"""
require_count(path, text, old)
text = text.replace(old, new, 1)
linux_links = [
    (
        "            help: 'Help',\n            link:\n                'https://rustdesk.com/docs/en/client/linux/#permissions-issue',",
        "            help: null,\n            link: null,",
    ),
    (
        "            help: 'Help',\n            link: 'https://rustdesk.com/docs/en/client/linux/#x11-required'));",
        "            help: null,\n            link: null));",
    ),
    (
        "            help: 'Help',\n            link: 'https://rustdesk.com/docs/en/client/linux/#login-screen'));",
        "            help: null,\n            link: null));",
    ),
]
for old, new in linux_links:
    require_count(path, text, old)
    text = text.replace(old, new, 1)
write(path, text)
print(f"updated {path}")

# Desktop About page: preserve product/license details, remove upstream website/privacy actions.
path = "flutter/lib/desktop/pages/desktop_setting_page.dart"
text = read(path)
require_count(path, text, "      const linkStyle = TextStyle(decoration: TextDecoration.underline);\n")
text = text.replace(
    "      const linkStyle = TextStyle(decoration: TextDecoration.underline);\n", "", 1
)
require_count(path, text, "_Card(title: translate('About RustDesk')")
text = text.replace(
    "_Card(title: translate('About RustDesk')",
    "_Card(title: translate('About CertLeap Academy')",
    1,
)
privacy = """              InkWell(
                  onTap: () {
                    launchUrlString('https://rustdesk.com/privacy.html');
                  },
                  child: Text(
                    translate('Privacy Statement'),
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),
"""
privacy_new = """              Text(translate('Privacy Statement'))
                  .marginSymmetric(vertical: 4.0),
"""
require_count(path, text, privacy)
text = text.replace(privacy, privacy_new, 1)
website = """              InkWell(
                  onTap: () {
                    launchUrlString('https://rustdesk.com');
                  },
                  child: Text(
                    translate('Website'),
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),
"""
require_count(path, text, website)
text = text.replace(website, "", 1)
write(path, text)
print(f"updated {path}")

# Installer EULA label remains visible but no longer opens the upstream privacy page.
path = "flutter/lib/desktop/pages/install_page.dart"
text = read(path)
old = """                          InkWell(
                            hoverColor: Colors.transparent,
                            onTap: () => launchUrlString(
                                'https://rustdesk.com/privacy.html'),
                            child: Tooltip(
                              message: 'https://rustdesk.com/privacy.html',
                              child: Row(children: [
                                Icon(Icons.launch_outlined, size: 16)
                                    .marginOnly(right: 5),
                                Text(
                                  translate('End-user license agreement'),
                                  style: const TextStyle(
                                      decoration: TextDecoration.underline),
                                )
                              ]),
                            ),
                          ),
"""
new = """                          Text(translate('End-user license agreement')),
"""
require_count(path, text, old)
text = text.replace(old, new, 1)
write(path, text)
print(f"updated {path}")

# Android system-visible service identity.
path = "flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/MainService.kt"
text = read(path)
replacements = {
    'const val DEFAULT_NOTIFY_TITLE = "RustDesk"': 'const val DEFAULT_NOTIFY_TITLE = "CertLeap Academy"',
    '"rustdesk:wakelock"': '"certleap:wakelock"',
    '"RustDeskVD"': '"CertLeapVD"',
    'val channelId = "RustDesk"': 'val channelId = "certleap_service"',
    'val channelName = "RustDesk Service"': 'val channelName = "CertLeap Academy Service"',
    'description = "RustDesk Service Channel"': 'description = "CertLeap Academy Service Channel"',
}
for old, new in replacements.items():
    require_count(path, text, old)
    text = text.replace(old, new, 1)
write(path, text)
print(f"updated {path}")

path = "flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/FloatingWindowService.kt"
text = read(path)
require_count(path, text, "idShowRustDesk", 2)
require_count(path, text, "Show RustDesk", 1)
text = text.replace("idShowRustDesk", "idShowCertLeap")
text = text.replace("Show RustDesk", "Show CertLeap Academy")
write(path, text)
print(f"updated {path}")

# Static MSI support examples should not point at upstream branding either.
path = "res/msi/Package/Fragments/AddRemoveProperties.wxs"
text = read(path)
require_count(path, text, "https://github.com/rustdesk/rustdesk", 5)
text = text.replace("https://github.com/rustdesk/rustdesk", "")
write(path, text)
print(f"updated {path}")

# Verification for app-facing references handled in this script.
checks = {
    "flutter/lib/mobile/pages/connection_page.dart": [
        "rustdesk.com/download",
        "package:url_launcher/url_launcher.dart",
    ],
    "flutter/lib/desktop/pages/connection_page.dart": [
        "rustdesk.com/pricing",
        "onUsePublicServerGuide",
        "package:url_launcher/url_launcher_string.dart",
    ],
    "flutter/lib/desktop/pages/desktop_home_page.dart": [
        "rustdesk.com/download",
        "github.com/rustdesk/rustdesk/releases",
        "rustdesk.com/docs/en/client/linux",
    ],
    "flutter/lib/desktop/pages/desktop_setting_page.dart": [
        "About RustDesk",
        "rustdesk.com/privacy.html",
        "launchUrlString('https://rustdesk.com')",
    ],
    "flutter/lib/desktop/pages/install_page.dart": ["rustdesk.com/privacy.html"],
    "flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/MainService.kt": [
        'DEFAULT_NOTIFY_TITLE = "RustDesk"',
        '"rustdesk:wakelock"',
        '"RustDeskVD"',
        'channelId = "RustDesk"',
        '"RustDesk Service"',
        '"RustDesk Service Channel"',
    ],
    "flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/FloatingWindowService.kt": [
        "Show RustDesk",
        "idShowRustDesk",
    ],
    "res/msi/Package/Fragments/AddRemoveProperties.wxs": [
        "https://github.com/rustdesk/rustdesk"
    ],
}
failures = []
for check_path, forbidden in checks.items():
    current = read(check_path)
    for needle in forbidden:
        if needle in current:
            failures.append(f"{check_path}: still contains {needle!r}")
if failures:
    raise RuntimeError("App-facing rebrand verification failed:\n" + "\n".join(failures))
print("App-facing audit findings removed.")
