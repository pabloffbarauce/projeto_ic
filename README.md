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

**Método recomendado: baixar o executável pronto**
 
Outro método é através do download do executável já compilado, disponível na [página de Releases](https://github.com/pabloffbarauce/projeto_ic/releases) do repositório. Basta baixar o arquivo `.exe` da versão mais recente e executá-lo — não é necessário instalar Python nem nenhuma biblioteca.
 
> O Windows pode exibir um aviso do SmartScreen na primeira execução, por não reconhecer o publicador do arquivo. Clique em **"Mais informações"** e depois em **"Executar assim mesmo"** para prosseguir.

**Método alternativo: rodar via código-fonte**

Se você ainda não tem Python instalado:
 
1. Baixe o instalador em [python.org/downloads](https://www.python.org/downloads/).
2. Ao rodar o instalador, marque a caixa **"Add python.exe to PATH"** na primeira tela antes de clicar em "Install Now" (ESSENCIAL).

Com o Python instalado, instale as bibliotecas necessárias através do Windows Powershell:
```bash
pip install numpy scipy matplotlib openpyxl
```

Outro método é através do download

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

A partir disso, entre na pasta em que os arquivos calculos.py e interface.py estão e execute:
```bash
cd <insira-seu-diretório>
python3 interface.py
```

## Como usar o programa
 
1. Insira os valores de **tempo** e **concentração** nos campos correspondentes (um valor por linha, ambas as colunas com a mesma quantidade de elementos).
2. Clique em **"Exemplo"** para carregar um conjunto de dados de demonstração, se quiser apenas testar o programa.
3. Clique em **"CALCULAR & PLOTAR"** para rodar o ajuste e visualizar os gráficos e o resumo estatístico.
4. Clique em **"EXPORTAR .XLSX"** para salvar os resultados completos (tempo, concentração, concentração ajustada, curva F, curva E, θh, σ², σθ² e N) em uma planilha.

## Imagens do software

Programa sem entrada de dados:
<img width="1593" height="928" alt="image" src="https://github.com/user-attachments/assets/0f50810a-8f1f-4bdd-b4c4-062862f53d60" />

Exemplo de entrada de dados:
<img width="1591" height="920" alt="image" src="https://github.com/user-attachments/assets/06b03e12-0339-4cb8-850f-19eafcff99de" />

Planilha exportada:
<img width="917" height="741" alt="image" src="https://github.com/user-attachments/assets/e7f88b8e-1c67-48f3-97d3-326ba27cfaf5" />


## Metodologia utilizada
 
- LEVENSPIEL, O. *Chemical Reaction Engineering*. 3. ed. New York: John Wiley & Sons, 1999.
- VUITIK, G. A. *Efeitos da recirculação em reatores anaeróbios compartimentados no tratamento de vinhaça*. 2017. Tese (Doutorado em Hidráulica e Saneamento) – Escola de Engenharia de São Carlos, Universidade de São Paulo, São Carlos, 2017.

