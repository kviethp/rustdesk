#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn certleap_runtime_identity_is_not_derived_from_display_name() {
        assert_eq!(APP_EXE_STEM, "certleap_academy");
        assert_eq!(app_exe_name(), "certleap_academy.exe");
        assert_eq!(SERVICE_NAME, "certleap");
        assert_eq!(URI_SCHEME, "certleap");

        // Human-visible branding contains a space; runtime identifiers deliberately do not.
        assert_ne!(APP_EXE_STEM, "CertLeap Academy");
        assert_ne!(SERVICE_NAME, "CertLeap Academy");
        assert_ne!(URI_SCHEME, "certleap academy");
    }

    #[test]
    fn installed_executable_path_uses_binary_identity() {
        assert_eq!(
            installed_executable_path(r"C:\Program Files\CertLeap Academy"),
            r"C:\Program Files\CertLeap Academy\certleap_academy.exe"
        );
    }
}
