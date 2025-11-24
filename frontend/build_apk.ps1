$env:PUB_CACHE = "C:\.pub-cache"
Set-Location $PSScriptRoot
Write-Host "Construindo APK..."
flutter build apk --release
Write-Host ""
Write-Host "APK gerado em: build\app\outputs\flutter-apk\app-release.apk"


