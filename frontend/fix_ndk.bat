@echo off
REM Script para corrigir NDK corrompido
set NDK_PATH=%LOCALAPPDATA%\Android\Sdk\ndk\28.2.13676358

if exist "%NDK_PATH%" (
    echo Removendo NDK corrompido: %NDK_PATH%
    rmdir /s /q "%NDK_PATH%"
    echo NDK removido. O Gradle baixara automaticamente uma nova versao.
) else (
    echo NDK nao encontrado no caminho especificado.
)

pause

