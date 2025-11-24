@echo off
set PUB_CACHE=C:\.pub-cache
if not exist "%PUB_CACHE%" mkdir "%PUB_CACHE%"
setx PUB_CACHE "%PUB_CACHE%"
echo PUB_CACHE configurado para: %PUB_CACHE%
echo Variável de ambiente atualizada. Reinicie o terminal para aplicar.

