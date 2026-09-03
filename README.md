# Análise Hidrodinâmica
Ferramenta para análise hidrodinâmica de reatores biológicos a partir de ensaios realizado com traçador, baseada no modelo de Levenspiel adaptado por Vuitik (2017, Apêndice A).
A partir dos dados de tempo e concentração, o programa realiza o ajuste sigmoidal de Boltzmann nos dados, calcula a curva F normalizada, a curva E (distribuição do tempo de residência), o tempo de detenção hidráulico médio (θh), a variância (σ²), a variância adimensional (σθ²) e o número de reatores de mistura perfeita em série (N). 

## Funcionalidades do software
- Ajuste não-linear de Boltzmann através do algoritmo de Levenberg-Marquadt (`scipy.optimize.curve_fit`)
- Cálculo de θh, σ², σθ² e N
- Plotagem de gráfico bruto e ajustado
- Exportação de resultados para planilha

## Pré-requisitos
- Python 3.9 ou superior
- Bibliotecas: `numpy`, `scipy`, `matplotlib`, `openpyxl` e `tkinter`

## Instalação

### Windows

Se você ainda não tem Python instalado:
 
1. Baixe o instalador em [python.org/downloads](https://www.python.org/downloads/).
2. Ao rodar o instalador, marque a caixa **"Add python.exe to PATH"** na primeira tela antes de clicar em "Install Now" (ESSENCIAL).

Com o Python instalado, instale as bibliotecas necessárias através do Windows Powershell:
```bash
pip install numpy scipy matplotlib openpyxl
```

### Linux
Para checar se a distribuição do Linux possui o Python, utilize o comando:
```bash
python3 --version
```

Caso o comando não seja reconhecido, instale o Python:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

Em seguida, instale as bibliotecas necessárias do projeto:
```bash
sudo apt install python3-tk python3-numpy python3-scipy python3-openpyxl python3-matplotlib
```

## Como usar o programa
 
1. Insira os valores de **tempo** e **concentração** nos campos correspondentes (um valor por linha, ambas as colunas com a mesma quantidade de elementos).
2. Clique em **"Exemplo"** para carregar um conjunto de dados de demonstração, se quiser apenas testar o programa.
3. Clique em **"CALCULAR & PLOTAR"** para rodar o ajuste e visualizar os gráficos e o resumo estatístico.
4. Clique em **"EXPORTAR .XLSX"** para salvar os resultados completos (tempo, concentração, concentração ajustada, curva F, curva E, θh, σ², σθ² e N) em uma planilha.

## Metodologia utilizada
 
- LEVENSPIEL, O. *Chemical Reaction Engineering*. 3. ed. New York: John Wiley & Sons, 1999.
- VUITIK, G. A. *Efeitos da recirculação em reatores anaeróbios compartimentados no tratamento de vinhaça*. 2017. Tese (Doutorado em Hidráulica e Saneamento) – Escola de Engenharia de São Carlos, Universidade de São Paulo, São Carlos, 2017.

