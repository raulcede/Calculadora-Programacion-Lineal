import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

def resolver_grafico(c, A_ub, b_ub, es_max=True):
    """
    Resuelve problemas de 2 variables gráficamente.
    """
    fig, ax = plt.subplots(figsize=(6, 5))
    x1_vals = np.linspace(0, 25, 300)

    # Graficar restricciones
    for i, (a, b) in enumerate(zip(A_ub, b_ub)):
        if a[1] != 0:
            y_vals = (b - a[0] * x1_vals) / a[1]
            ax.plot(x1_vals, y_vals, label=f'Restricción {i+1}')
        else:
            ax.axvline(x=b/a[0], label=f'Restricción {i+1}')

    ax.set_xlim((0, 15))
    ax.set_ylim((0, 15))
    ax.set_xlabel('Variable x1')
    ax.set_ylabel('Variable x2')
    ax.set_title('Método Gráfico - Región Factible')
    ax.grid(True)
    ax.legend()

    # Cálculo numérico del punto óptimo
    c_opt = [-x for x in c] if es_max else c
    res = linprog(c_opt, A_ub=A_ub, b_ub=b_ub, bounds=(0, None), method='highs')

    val_z = -res.fun if es_max else res.fun
    return res.x, val_z, fig