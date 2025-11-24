@echo off
set PUB_CACHE=C:\.pub-cache
if not exist "%PUB_CACHE%" mkdir "%PUB_CACHE%"
set PUB_HOSTED_URL=https://pub.dartlang.org
cd /d "%~dp0"
echo Construindo APK...
flutter build apk --release
echo.
echo APK gerado em: build\app\outputs\flutter-apk\app-release.apk

