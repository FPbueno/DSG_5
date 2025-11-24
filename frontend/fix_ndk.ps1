# Script para corrigir NDK corrompido
$ndkPath = "$env:LOCALAPPDATA\Android\Sdk\ndk\28.2.13676358"

if (Test-Path $ndkPath) {
    Write-Host "Removendo NDK corrompido: $ndkPath"
    Remove-Item -Path $ndkPath -Recurse -Force
    Write-Host "NDK removido. O Gradle baixará automaticamente uma nova versão."
} else {
    Write-Host "NDK não encontrado no caminho especificado."
}

