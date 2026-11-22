from scipy.optimize import linprog

def resolver_simplex(c, A_ub, b_ub, es_max=True):
    """
    Resuelve el método Simplex estándar para restricciones '<='.
    """
    c_opt = [-x for x in c] if es_max else c
    
    res = linprog(c_opt, A_ub=A_ub, b_ub=b_ub, bounds=(0, None), method='highs')

    if res.success:
        val_z = -res.fun if es_max else res.fun
        return {
            "exito": True,
            "z": val_z,
            "variables": res.x,
            "iteraciones": res.nit
        }
    else:
        return {"exito": False, "mensaje": res.message}