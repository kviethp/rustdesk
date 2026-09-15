# Run Android build inside Docker
$ErrorActionPreference = "Stop"

Write-Host "Building Docker image certleap-android-builder..." -ForegroundColor Cyan
docker build -f docker/Dockerfile.android -t certleap-android-builder .

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build Docker image."
    exit 1
}

Write-Host "Running Android APK build in container..." -ForegroundColor Cyan
docker run --rm -v "${PWD}:/workspace" certleap-android-builder bash /workspace/docker/build_apk.sh

if ($LASTEXITCODE -eq 0) {
    Write-Host "Success! APK generated at build\certleap-academy-arm64-v8a.apk" -ForegroundColor Green
} else {
    Write-Error "Build failed inside container."
}
