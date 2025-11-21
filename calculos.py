import math
import numpy as np
from numpy import trapezoid


def xAty50(x_y_curve):
    if len(x_y_curve) < 2:
        return None

    sortedx_y_curve = sorted(x_y_curve)
    y_values = [point[1] for point in sortedx_y_curve]
    y_min = min(y_values)
    y_max = max(y_values)
    y_mid = y_min + (y_max - y_min) / 2

    if y_min == y_max:
        return None

    for i in range(1, len(sortedx_y_curve)):
        p1 = sortedx_y_curve[i - 1]
        p2 = sortedx_y_curve[i]
        x1, y1 = p1
        x2, y2 = p2

        if (y1 < y_mid < y2) or (y1 >= y_mid > y2):
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


def initial_data(x_data, y_data):
    x_y_curve = []
    for i in range(len(x_data)):
        x_y_curve.append((x_data[i], y_data[i])) # juntando x e y em uma tupla
    return x_y_curve


def boltzmann(x_data, x_y_curve):
    """
    Realiza o ajuste da curva usando a função logística.
    Retorna a lista de tuplas tratadas (treated_x_y_curve).
    """
    x_values = [point[0] for point in x_y_curve]
    x_min, x_max = min(x_values), max(x_values)

    # Cálculo dos parâmetros
    dx = (x_max - x_min) / 20.0
    A1, A2 = curveParameters(x_y_curve)
    x0 = xAty50(x_y_curve)

    if x0 is None:
        return None  # Retorna None para indicar erro

    treated_x_y_curve = []
    for i in range(len(x_y_curve)):
        # Fórmula sigmoidal original
        y = A2 + (A1 - A2) / (1 + math.exp((x_data[i] - x0) / dx))
        treated_x_y_curve.append((x_data[i], y))

    return treated_x_y_curve


def f_curve_calc(treated_x_y_curve):
    """
    Calcula a Curva F normalizando os dados tratados.
    Retorna a lista f_curve e o valor máximo usado na normalização.
    """
    y_treated_values = [point[1] for point in treated_x_y_curve]
    y_treated_max = max(y_treated_values)

    f_curve = []
    for i in range(len(treated_x_y_curve)):
        f_curve.append(treated_x_y_curve[i][1] / y_treated_max)

    return f_curve, y_treated_max


def final_stats(x_data, f_curve):
    """
    Realiza cálculos de derivada e integral para encontrar parâmetros de residência (RTD).
    Retorna um dicionário com todos os resultados estatísticos.
    """
    x_values_np = np.array(x_data)
    f_values_np = np.array(f_curve)

    # Cálculo da Curva E (Derivada)
    E_t_curve = np.gradient(f_values_np, x_values_np)

    # Tempo Hidráulico (Primeiro momento)
    integrand = x_values_np * E_t_curve
    hydraulic_time = trapezoid(integrand, x_values_np)

    # Variância (Segundo momento central)
    variance_calc = (x_values_np - hydraulic_time) ** 2 * E_t_curve
    variance = trapezoid(variance_calc, x_values_np)

    # Variância adimensional e N
    sigma_theta = (variance / (hydraulic_time ** 2))

    # Evita divisão por zero se sigma for 0 (apenas segurança)
    N = 1 / sigma_theta if sigma_theta != 0 else 0

    return {
        "x_values_np": x_values_np,
        "E_t_curve": E_t_curve,
        "hydraulic_time": hydraulic_time,
        "variance": variance,
        "sigma_theta": sigma_theta,
        "N": N
    }


# --- Bloco Principal de Execução ---

def main():
    # 1. Dados de entrada
    x_data = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5, 5.25,
              5.5, 5.75, 6, 6.25, 6.5, 6.75]
    y_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.064053751, 0.131690929, 0.154087346, 0.16019037, 0.176315789,
              0.180011198, 0.178443449, 0.180011198, 0.191041433, 0.183706607, 0.182754759, 0.182866741, 0.18980963,
              0.199384099, 0.193673012]

    # 2. tratando os dados
    x_y_curve = initial_data(x_data, y_data)

    # ajustando a curva
    treated_x_y_curve = boltzmann(x_data, x_y_curve)

    if treated_x_y_curve is None:
        print("xaty50 could not be determined. Check the input data.")
        return

    print("Valores ajustados:")
    for i in range(len(treated_x_y_curve)):
        print(f"({treated_x_y_curve[i][0]:.2f}) ({treated_x_y_curve[i][1]:.5f})")

    # curva F
    f_curve, y_treated_max = f_curve_calc(treated_x_y_curve)

    print(y_treated_max)
    print("")
    print("Curva F:")
    for val in f_curve:
        print(val)
    print("")

    #  estatísticas e curva E
    stats = final_stats(x_data, f_curve)

    # mostrando a curva E em função do tempo
    for x_val, e_val in zip(stats["x_values_np"], stats["E_t_curve"]):
        print(f"At x = {x_val:.2f} : E(t) = {e_val:.5f}")

    print("")
    print(f"θh: {stats['hydraulic_time']:.5f}")
    print(f"σ²: {stats['variance']}")
    print("")
    print(f"σθ²: {stats['sigma_theta']}")
    print(f"O valor de N é: {stats['N']:.2f}")


if __name__ == "__main__":
    main()