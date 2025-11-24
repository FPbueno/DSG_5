# Problema: Erro de Build com Caracteres Especiais no Caminho

## Problema Identificado

O Flutter está falhando ao compilar porque o caminho do projeto contém caracteres especiais:

- `C:\Área de Trabalho\Repositórios\ABP\frontend`

Os erros mostram:

- `Error: Unable to read file: C:\rea de Trabalho\...` (caracteres corrompidos)
- `Could not write file to C:\Área de Trabalho\...` (falha ao escrever shaders)

## Solução Recomendada

Mova o projeto para um caminho sem caracteres especiais, por exemplo:

- `C:\Projects\ABP\frontend`
- `C:\Dev\ABP\frontend`
- `C:\Repos\ABP\frontend`

## Passos para Resolver

1. Feche o Flutter/IDE
2. Mova a pasta `ABP` para um novo local sem caracteres especiais
3. Abra o projeto no novo local
4. Execute: `flutter clean`
5. Execute: `flutter pub get`
6. Tente compilar novamente: `flutter build apk --release`

## Alternativa (Temporária)

Se não puder mover o projeto, tente criar um link simbólico:

```powershell
# Como Administrador
New-Item -ItemType SymbolicLink -Path "C:\ABP" -Target "C:\Área de Trabalho\Repositórios\ABP"
```

Depois use `C:\ABP\frontend` para compilar.
