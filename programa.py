import math
import numpy as np
from numpy import trapezoid

x_data = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5]
y_data = [126.7, 131.3, 133.9, 165.6, 242.7, 450.6, 509, 584.7, 591.2, 553,5]

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
    return None

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

if x0 is None:
    print("xaty50 could not be determined. Check the input data.")
    exit()

for i in range(len(x_y_curve)):
    y = A2 + (A1-A2)/(1 + math.exp((x_data[i]-x0)/dx))
    treated_x_y_curve.append((x_data[i], y))
    print(f"({treated_x_y_curve[i][0]:.2f}) ({treated_x_y_curve[i][1]:.5f})")

y_treated_values = [point[1] for point in treated_x_y_curve]
y_treated_max = max(y_treated_values)
print(y_treated_max) ; print("")

f_curve = []

for i in range(len(x_y_curve)):
    f_curve.append(treated_x_y_curve[i][1] / y_treated_max)
    print(f_curve[i])

print("")

x_values_np = np.array(x_data)
f_values_np = np.array(f_curve)
E_t_curve = np.gradient(f_values_np, x_values_np)

for x_val, e_val in zip(x_values_np, E_t_curve):
    print(f"At x = {x_val:.2f} : E(t) = {e_val:.5f}")

integrand = x_values_np * E_t_curve
hydraulic_time = trapezoid(integrand, x_values_np)
print("")
print(f"{hydraulic_time:.5f}")

variance_calc = (x_values_np - hydraulic_time) ** 2 * E_t_curve
variance = trapezoid(variance_calc, x_values_np)
print(variance)
print("")
sigma_theta = (variance/(hydraulic_time**2))
print(sigma_theta)
N = 1/sigma_theta
integer_N = round(N)
print(integer_N)