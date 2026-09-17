from pathlib import Path

path = Path("src/platform/windows.rs")
text = path.read_text(encoding="utf-8")
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one old pattern, found {count}")
    text = text.replace(old, new, 1)


replace_once(
    "mod installer_handoff;\nmod installer_shell;",
    "mod installer_handoff;\nmod installer_identity;\nmod installer_shell;",
    "module declaration",
)

replace_once(
    "windows_service::service_dispatcher::start(crate::get_app_name(), ffi_service_main)",
    "windows_service::service_dispatcher::start(installer_identity::SERVICE_NAME, ffi_service_main)",
    "service dispatcher",
)
replace_once(
    "service_control_handler::register(crate::get_app_name(), event_handler)?",
    "service_control_handler::register(installer_identity::SERVICE_NAME, event_handler)?",
    "service handler",
)

replace_once(
    '''pub fn get_install_options() -> String {
    let app_name = crate::get_app_name();
    let subkey = format!(".{}", app_name.to_lowercase());''',
    '''pub fn get_install_options() -> String {
    let subkey = format!(".{}", installer_identity::URI_SCHEME);''',
    "install options URI key",
)
replace_once(
    '''        None => {
            let app_name = crate::get_app_name();
            let subkey = format!(".{}", app_name.to_lowercase());''',
    '''        None => {
            let subkey = format!(".{}", installer_identity::URI_SCHEME);''',
    "silent install URI key",
)

replace_once(
    '''    let exe = format!("{}\\\\{}.exe", path, crate::get_app_name());''',
    '''    let exe = installer_identity::installed_executable_path(&path);''',
    "installed executable path",
)

replace_once(
    '''    let app_name = crate::get_app_name();
    if src_exe_filename == format!("{app_name}.exe") {
        Ok("".to_owned())
    } else {
        Ok(format!(
            "
        move /Y \\\"{path}\\\\{src_exe_filename}\\\" \\\"{path}\\\\{app_name}.exe\\\"
        ",
        ))
    }''',
    '''    let app_exe_name = installer_identity::app_exe_name();
    if src_exe_filename == app_exe_name {
        Ok("".to_owned())
    } else {
        Ok(format!(
            "
        move /Y \\\"{path}\\\\{src_exe_filename}\\\" \\\"{path}\\\\{app_exe_name}\\\"
        ",
        ))
    }''',
    "rename installed executable",
)

# Every `ext` in these installer paths is a file/protocol registry identity, not a display label.
text = text.replace(
    "let ext = app_name.to_lowercase();",
    "let ext = installer_identity::URI_SCHEME;",
)

replace_once(
    '''fn get_before_uninstall(kill_self: bool) -> String {
    let app_name = crate::get_app_name();
    let ext = installer_identity::URI_SCHEME;''',
    '''fn get_before_uninstall(kill_self: bool) -> String {
    let app_name = crate::get_app_name();
    let service_name = installer_identity::SERVICE_NAME;
    let app_exe_name = installer_identity::app_exe_name();
    let ext = installer_identity::URI_SCHEME;''',
    "uninstall identities",
)
replace_once(
    '''    sc stop {app_name}
    sc delete {app_name}
    taskkill /F /IM {broker_exe}
    taskkill /F /IM {app_name}.exe{filter}
    reg delete HKEY_CLASSES_ROOT\\\\.{ext} /f''',
    '''    sc stop {service_name}
    sc delete {service_name}
    taskkill /F /IM {broker_exe}
    taskkill /F /IM {app_exe_name}{filter}
    reg delete HKEY_CLASSES_ROOT\\\\.{ext} /f''',
    "uninstall commands",
)

replace_once(
    '''    sc stop {app_name}
    sc delete {app_name}
    if exist \\\"%PROGRAMDATA%\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup\\\\{app_name} Tray.lnk\\\" del /f /q \\\"%PROGRAMDATA%\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup\\\\{app_name} Tray.lnk\\\"
    taskkill /F /IM {broker_exe}
    taskkill /F /IM {app_name}.exe{filter}''',
    '''    sc stop {service_name}
    sc delete {service_name}
    if exist \\\"%PROGRAMDATA%\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup\\\\{app_name} Tray.lnk\\\" del /f /q \\\"%PROGRAMDATA%\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup\\\\{app_name} Tray.lnk\\\"
    taskkill /F /IM {broker_exe}
    taskkill /F /IM {app_exe_name}{filter}''',
    "uninstall service commands",
)
replace_once(
    '''        app_name = crate::get_app_name(),
        broker_exe = WIN_TOPMOST_INJECTED_PROCESS_EXE,
    );''',
    '''        app_name = crate::get_app_name(),
        service_name = installer_identity::SERVICE_NAME,
        app_exe_name = installer_identity::app_exe_name(),
        broker_exe = WIN_TOPMOST_INJECTED_PROCESS_EXE,
    );''',
    "uninstall service format identities",
)

replace_once(
    '''fn get_install_service_commands(path: &str, exe: &str) -> ResultType<String> {
    let app_name = crate::get_app_name();''',
    '''fn get_install_service_commands(path: &str, exe: &str) -> ResultType<String> {
    let app_name = crate::get_app_name();
    let service_name = installer_identity::SERVICE_NAME;''',
    "service install identity",
)
replace_once(
    '''fn get_install_service_commands(path: &str, exe: &str) -> ResultType<String> {
    let app_name = crate::get_app_name();
    let service_name = installer_identity::SERVICE_NAME;''',
    '''fn get_install_service_commands(path: &str, exe: &str) -> ResultType<String> {
    let app_name = crate::get_app_name();
    let service_name = installer_identity::SERVICE_NAME;
    let app_exe_name = installer_identity::app_exe_name();''',
    "service install executable identity",
)
replace_once(
    '''sc stop {app_name}
sc delete {app_name}
sc create {app_name} binpath= \\\"\\\\\\\"{exe}\\\\\\\" --import-config \\\\\\\"{config_path}\\\\\\\"\\\" start= auto DisplayName= \\\"{app_name} Service\\\"
sc start {app_name}
sc stop {app_name}
sc delete {app_name}''',
    '''sc stop {service_name}
sc delete {service_name}
sc create {service_name} binpath= \\\"\\\\\\\"{exe}\\\\\\\" --import-config \\\\\\\"{config_path}\\\\\\\"\\\" start= auto DisplayName= \\\"{app_name} Service\\\"
sc start {service_name}
sc stop {service_name}
sc delete {service_name}''',
    "service install commands",
)
replace_once(
    "taskkill /F /IM {app_name}.exe{filter}",
    "taskkill /F /IM {app_exe_name}{filter}",
    "service install process identity",
)

replace_once(
    '''sc create {app_name} binpath= \\\"\\\\\\\"{exe}\\\\\\\" --service\\\" start= auto DisplayName= \\\"{app_name} Service\\\"
sc start {app_name}
\",
    app_name = crate::get_app_name())''',
    '''sc create {service_name} binpath= \\\"\\\\\\\"{exe}\\\\\\\" --service\\\" start= auto DisplayName= \\\"{app_name} Service\\\"
sc start {service_name}
\",
    service_name = installer_identity::SERVICE_NAME,
    app_name = crate::get_app_name())''',
    "service creation commands",
)

replace_once(
    '''pub fn is_self_service_running() -> bool {
    is_service_running(&crate::get_app_name())
}''',
    '''pub fn is_self_service_running() -> bool {
    is_service_running(installer_identity::SERVICE_NAME)
}''',
    "service status identity",
)

replace_once(
    '''    let app_exe_name = &format!("{}.exe", &app_name);''',
    '''    let app_exe_name = installer_identity::app_exe_name();''',
    "update executable identity",
)
replace_once(
    '''sc stop {app_name}
taskkill /F /IM {app_name}.exe{filter}''',
    '''sc stop {service_name}
taskkill /F /IM {app_exe_name}{filter}''',
    "update stop/process identities",
)
replace_once(
    '''        app_name = app_name,
        copy_exe = copy_exe_cmd(&src_exe, &exe, &path)?,''',
    '''        app_name = app_name,
        service_name = installer_identity::SERVICE_NAME,
        app_exe_name = app_exe_name,
        copy_exe = copy_exe_cmd(&src_exe, &exe, &path)?,''',
    "update format identities",
)

replace_once(
    '''    let app_name = crate::get_app_name().to_lowercase();''',
    '''    let app_name = installer_identity::APP_EXE_STEM.to_owned();''',
    "main process identity",
)

# update_install_option no longer needs to derive protocol identity from the display name.
text = text.replace(
    '''    let app_name = crate::get_app_name();
    let ext = installer_identity::URI_SCHEME;
    let cmds =
        format!("chcp 65001 && reg add HKEY_CLASSES_ROOT\\\\.{ext} /f /v {k} /t REG_SZ /d \\\"{v}\\\"");''',
    '''    let ext = installer_identity::URI_SCHEME;
    let cmds =
        format!("chcp 65001 && reg add HKEY_CLASSES_ROOT\\\\.{ext} /f /v {k} /t REG_SZ /d \\\"{v}\\\"");''',
)

# Required invariants after the patch.
required = [
    "mod installer_identity;",
    "installer_identity::installed_executable_path(&path)",
    "service_dispatcher::start(installer_identity::SERVICE_NAME",
    "service_control_handler::register(installer_identity::SERVICE_NAME",
    "service_name = installer_identity::SERVICE_NAME",
    "installer_identity::URI_SCHEME",
    "installer_identity::APP_EXE_STEM",
    "taskkill /F /IM {app_exe_name}{filter}",
]
for needle in required:
    if needle not in text:
        raise RuntimeError(f"missing required identity wiring after patch: {needle}")

if "taskkill /F /IM {app_name}.exe" in text:
    raise RuntimeError("display-name executable identity remains in Windows process commands")

if text != original:
    path.write_text(text, encoding="utf-8")
    print("Patched src/platform/windows.rs")
else:
    print("src/platform/windows.rs already patched")
