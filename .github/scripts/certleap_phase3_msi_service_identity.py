from pathlib import Path

path = Path("res/msi/Package/Components/RustDesk.wxs")
text = path.read_text(encoding="utf-8")
original = text

replacements = [
    (
        'Property="CreateStartService" Value="$(var.Product);&quot;[INSTALLFOLDER_INNER]$(var.AppExeName).exe&quot; --service"',
        'Property="CreateStartService" Value="$(var.ProductLower);&quot;[INSTALLFOLDER_INNER]$(var.AppExeName).exe&quot; --service"',
        "CreateStartService",
    ),
    (
        'Property="TryStopDeleteService" Value="$(var.Product)"',
        'Property="TryStopDeleteService" Value="$(var.ProductLower)"',
        "TryStopDeleteService",
    ),
    (
        'Property="AppName" Value="$(var.Product)"',
        'Property="AppName" Value="$(var.ProductLower)"',
        "SetPropertyIsServiceRunning",
    ),
]

for old, new, label in replacements:
    if new in text:
        continue
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one old service identity, found {count}")
    text = text.replace(old, new, 1)

for _, new, label in replacements:
    if new not in text:
        raise RuntimeError(f"{label}: stable service identity was not applied")

if text != original:
    path.write_text(text, encoding="utf-8")
    print("Patched MSI service identity to ProductLower")
else:
    print("MSI service identity already uses ProductLower")
