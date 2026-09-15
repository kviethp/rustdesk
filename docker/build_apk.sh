#!/bin/bash
set -e

echo "=== Building CertLeap Academy Android APK ==="

cd /workspace

export ANDROID_NDK_HOME=/opt/android-sdk/ndk/28.0.12433566
export ANDROID_NDK_ROOT=/opt/android-sdk/ndk/28.0.12433566
export VCPKG_ROOT=/opt/vcpkg

# 1. Setup vcpkg if needed
if [ ! -d "/opt/vcpkg" ]; then
    echo "Cloning and bootstrapping vcpkg..."
    git clone https://github.com/microsoft/vcpkg /opt/vcpkg
    cd /opt/vcpkg
    git checkout 9e593bb18ea69cc5095e012465dcd675a822ed0d
    ./bootstrap-vcpkg.sh -disableMetrics
    cd /workspace
fi

echo "Installing Android vcpkg dependencies..."
./flutter/build_android_deps.sh arm64-v8a

echo "Building librustdesk.so for arm64..."
cargo ndk --platform 21 --target aarch64-linux-android build --release --features flutter,hwcodec

echo "Copying native libraries..."
mkdir -p ./flutter/android/app/src/main/jniLibs/arm64-v8a
cp ${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/lib/aarch64-linux-android/libc++_shared.so ./flutter/android/app/src/main/jniLibs/arm64-v8a/
cp ./target/aarch64-linux-android/release/liblibrustdesk.so ./flutter/android/app/src/main/jniLibs/arm64-v8a/librustdesk.so

echo "Building Flutter APK..."
cd flutter
flutter pub get
flutter build apk --release --target-platform android-arm64

mkdir -p /workspace/build
cp build/app/outputs/flutter-apk/app-release.apk /workspace/build/certleap-academy-arm64-v8a.apk || \
cp build/app/outputs/flutter-apk/app-arm64-v8a-release.apk /workspace/build/certleap-academy-arm64-v8a.apk || true

echo "=== Build Complete! APK is located at /workspace/build/certleap-academy-arm64-v8a.apk ==="
