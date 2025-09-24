import math

x_data = [0,15,30,45,60,420,435, 450,465,480,495,510,525,540,555,570,585,600,615,630]
y_data = [0.029,0.029,0.0314,0.0338,0.0422,0.1106,0.1154,0.1178,0.1202,0.1346,0.1274,0.1286,0.137,0.137,0.1382,0.1418,0.1394,0.1394,0.1382,0.137]

x_y_curve = []

for i in range(len(x_data)):
    x_y_curve.append((x_data[i], y_data[i])) # Incorpora os dados no array da curva xy

def xAty50(x_y_curve):
    if len(x_y_curve) < 2: # Caso possua menos de dois elemnentos, não retorna nada
        return None

    sortedx_y_curve = sorted(x_y_curve) # Organiza o vetor através de x para ajudar na leitura dos valores de y
    y_values = [point[1] for point in sortedx_y_curve]
    y_min = min(y_values)
    y_max = max(y_values)
    y_mid = y_min + (y_max - y_min) / 2 # Adquire o valor exato do meio de y

    if y_min == y_max:
        return None

    for i in range(1, len(sortedx_y_curve)): # Laço de repetição que checa dois pontos e tenta encontrar se o
        p1 = sortedx_y_curve[i-1]            # valor do meio de y se encontra entre eles, caso encontre, faz
        p2 = sortedx_y_curve[i]              # uma interpolação linear para encontrar o valor exato de x que
        x1, y1 = p1                          # pertence ao y do meio.
        x2, y2 = p2

        if(y1 < y_mid < y2) or (y1 >= y_mid > y2):
            if y2 == y1:
                return (x1 + x2) / 2
            x_interpolated = x1 + (x2 - x1) * (y_mid - y1) / (y2 - y1)
            return x_interpolated

def curveParameters(x_y_curve):
    if len(x_y_curve) < 2:
        return None, None

    sortedx_y_curve = sorted(x_y_curve)
    y_values = [point[1] for point in sortedx_y_curve]
    yAtxMin = sortedx_y_curve[0][1]
    yAtxMax = sortedx_y_curve[-1][1]
    if yAtxMin > yAtxMax:
        return max(y_values), min(y_values)
    else:
        return min(y_values), max(y_values)

x_values = [point[0] for point in x_y_curve]
x_min, x_max = min(x_values), max(x_values)
dx = (x_max - x_min) / 20.0
A1, A2 = curveParameters(x_y_curve)
x0 = xAty50(x_y_curve)
treated_x_y_curve = []

for i in range(len(x_y_curve)):
    y = A2 + (A1-A2)/(1 + math.exp((x_data[i]-x0)/dx))
    treated_x_y_curve.append((x_data[i], y))
    print(treated_x_y_curve[i])





