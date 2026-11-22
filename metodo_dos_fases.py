from scipy.optimize import linprog

def resolver_dos_fases(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, es_max=True):
    """
    Resuelve el Método de 2 Fases cuando existen igualdades o restricciones '>='.
    """
    c_opt = [-x for x in c] if es_max else c

    res = linprog(
        c_opt, 
        A_ub=A_ub if A_ub else None, 
        b_ub=b_ub if b_ub else None, 
        A_eq=A_eq if A_eq else None, 
        b_eq=b_eq if b_eq else None, 
        bounds=(0, None), 
        method='highs'
    )

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