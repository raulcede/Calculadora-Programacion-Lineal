import random
import customtkinter as ctk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppCalculadora(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Calculadora de Programación lineal")
        self.geometry("1220x820")
        self.minsize(1000, 700)

        self.inputs_fo = []
        self.inputs_rest = []
        self.crear_interfaz()

    def crear_interfaz(self):
        header = ctk.CTkFrame(self, corner_radius=0, fg_color="#1e293b")
        header.pack(fill="x")

        lbl_title = ctk.CTkLabel(header, text="Calculadora de Programación Lineal", font=ctk.CTkFont(size=18, weight="bold"), text_color="#ffffff")
        lbl_title.pack(side="left", padx=20, pady=12)

        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        self.panel_izq = ctk.CTkScrollableFrame(main_container, width=420, corner_radius=8)
        self.panel_izq.pack(side="left", fill="both", padx=(0, 10), pady=5)

        ctk.CTkLabel(self.panel_izq, text="1. Parámetros del Problema", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        ctk.CTkLabel(self.panel_izq, text="Método a utilizar:").pack(anchor="w", padx=10)
        
        self.cb_metodo = ctk.CTkComboBox(self.panel_izq, values=["Método Simplex", "Método 2 Fases", "Método Gráfico"], command=self.on_metodo_change)
        self.cb_metodo.set("Método Simplex")
        self.cb_metodo.pack(fill="x", padx=10, pady=(0, 8))

        ctk.CTkLabel(self.panel_izq, text="Objetivo:").pack(anchor="w", padx=10)
        self.cb_tipo = ctk.CTkComboBox(self.panel_izq, values=["Maximizar", "Minimizar"])
        self.cb_tipo.set("Maximizar")
        self.cb_tipo.pack(fill="x", padx=10, pady=(0, 10))

        grid_params = ctk.CTkFrame(self.panel_izq, fg_color="transparent")
        grid_params.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(grid_params, text="Cantidad de variables:").grid(row=0, column=0, sticky="w", pady=2)
        self.sp_vars = ctk.CTkComboBox(grid_params, values=["2", "3", "4"], width=80)
        self.sp_vars.set("3")
        self.sp_vars.grid(row=0, column=1, padx=10, pady=2)

        ctk.CTkLabel(grid_params, text="Cantidad de restricciones:").grid(row=1, column=0, sticky="w", pady=2)
        self.sp_rest = ctk.CTkComboBox(grid_params, values=["2", "3", "4"], width=80)
        self.sp_rest.set("2")
        self.sp_rest.grid(row=1, column=1, padx=10, pady=2)

        btn_generar = ctk.CTkButton(self.panel_izq, text="Generar Casillas", fg_color="#2563eb", hover_color="#1d4ed8", command=self.generar_formulario)
        btn_generar.pack(fill="x", padx=10, pady=10)

        self.frame_matriz = ctk.CTkFrame(self.panel_izq, fg_color="transparent")
        self.frame_matriz.pack(fill="both", expand=True, padx=10, pady=5)

        panel_der = ctk.CTkFrame(main_container, corner_radius=8)
        panel_der.pack(side="right", fill="both", expand=True, pady=5)

        self.tab_res = ctk.CTkTabview(panel_der)
        self.tab_res.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_procedimiento = self.tab_res.add("Procedimiento Paso a Paso")
        self.tab_grafico = self.tab_res.add("Gráfica")

        self.box_procedimiento = ctk.CTkTextbox(self.tab_procedimiento, font=("Consolas", 12))
        self.box_procedimiento.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_grafica = ctk.CTkFrame(self.tab_grafico, corner_radius=8)
        self.frame_grafica.pack(fill="both", expand=True, padx=5, pady=5)
        self.canvas = None

        self.generar_formulario_ejercicio1()

    def on_metodo_change(self, choice):
        # Limpia el cuadro de texto al cambiar de opción
        self._escribir_en_interfaz("")

        if choice == "Método Gráfico":
            self.sp_vars.set("2")
            self.sp_vars.configure(state="disabled")
        else:
            self.sp_vars.configure(state="normal")
    def generar_formulario_ejercicio1(self):
        self.sp_vars.set("3")
        self.sp_rest.set("2")
        self.cb_metodo.set("Método Simplex")
        self.cb_tipo.set("Maximizar")
        self.generar_formulario(c_default=[1, 4, -1], rest_default=[[-5, 6, -2, "<=", 30], [-1, 3, 6, "<=", 12]])

    def generar_formulario(self, c_default=None, rest_default=None):
        for w in self.frame_matriz.winfo_children():
            w.destroy()

        self.inputs_fo, self.inputs_rest = [], []
        n_vars, n_rest = int(self.sp_vars.get()), int(self.sp_rest.get())

        ctk.CTkLabel(self.frame_matriz, text="2. Ingreso de Coeficientes", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(self.frame_matriz, text="Función Objetivo (Z):").pack(anchor="w", pady=(5, 2))
        
        f_fo = ctk.CTkFrame(self.frame_matriz, fg_color="transparent")
        f_fo.pack(fill="x", pady=(0, 10))

        for i in range(n_vars):
            val = str(c_default[i]) if c_default and i < len(c_default) else str(random.randint(-3, 8))
            inp = ctk.CTkEntry(f_fo, width=45, font=("Consolas", 12))
            inp.insert(0, val)
            inp.pack(side="left", padx=2)
            self.inputs_fo.append(inp)
            ctk.CTkLabel(f_fo, text=f"X{i+1}" + (" +" if i < n_vars - 1 else "")).pack(side="left", padx=1)

        ctk.CTkLabel(self.frame_matriz, text="Sujeto a:").pack(anchor="w", pady=(5, 2))
        for r in range(n_rest):
            f_r = ctk.CTkFrame(self.frame_matriz, fg_color="transparent")
            f_r.pack(fill="x", pady=2)
            row_coefs = []

            for c in range(n_vars):
                val_c = str(rest_default[r][c]) if rest_default and r < len(rest_default) and c < len(rest_default[r]) else str(random.randint(-2, 6))
                inp = ctk.CTkEntry(f_r, width=40, font=("Consolas", 12))
                inp.insert(0, val_c)
                inp.pack(side="left", padx=1)
                row_coefs.append(inp)
                ctk.CTkLabel(f_r, text=f"X{c+1}" + ("+" if c < n_vars - 1 else "")).pack(side="left", padx=1)

            cb_signo = ctk.CTkComboBox(f_r, values=["<=", ">=", "="], width=58, state="readonly")
            cb_signo.set(rest_default[r][-2] if rest_default and r < len(rest_default) else "<=")
            cb_signo.pack(side="left", padx=3)

            val_rhs = str(rest_default[r][-1]) if rest_default and r < len(rest_default) else str(random.randint(10, 40))
            inp_val = ctk.CTkEntry(f_r, width=45, font=("Consolas", 12))
            inp_val.insert(0, val_rhs)
            inp_val.pack(side="left", padx=1)

            self.inputs_rest.append((row_coefs, cb_signo, inp_val))

        btn_calc = ctk.CTkButton(self.frame_matriz, text="Resolver Ejercicio", fg_color="#10b981", hover_color="#059669", height=38, font=ctk.CTkFont(size=13, weight="bold"), command=self.ejecutar_solver)
        btn_calc.pack(fill="x", pady=(15, 10))

    def formato_tabla(self, headers, base_vars, matrix):
        out = " | ".join([f"{h:>6}" for h in headers]) + "\n"
        out += "-" * (len(out) - 1) + "\n"
        for i, row in enumerate(matrix):
            out += f"{base_vars[i]:>4} | " + " | ".join([f"{val:>6.2f}" for val in row]) + "\n"
        return out

    def resolver_simplex_loop(self, headers, base_vars, matrix, es_max=True):
        out, iteracion = "", 1
        while iteracion <= 15:
            z_coefs = matrix[0, 1:-1]

            # Criterio de optimalidad
            # Maximizar: todos >= 0 (forma Z - c_j X_j = 0)
            # Minimizar: todos <= 0
            if es_max:
                es_optimo = np.all(z_coefs >= -1e-7)
            else:
                es_optimo = np.all(z_coefs <= 1e-7)

            if es_optimo:
                out += f"\nOptimalidad alcanzada en la iteración {iteracion - 1}.\n\nSolución Óptima:\n"
                out += f"Z = {matrix[0, -1]:.4f}\n"
                for i in range(1, len(base_vars)):
                    out += f"{base_vars[i]} = {matrix[i, -1]:.4f}\n"
                for v in headers[1:-1]:
                    if v not in base_vars:
                        out += f"{v} = 0.0000\n"
                return out, matrix, base_vars, True

            # Elección de variable entrante:
            # Maximizar: el más negativo
            # Minimizar: el más positivo
            if es_max:
                col_pivote = np.argmin(z_coefs) + 1
            else:
                col_pivote = np.argmax(z_coefs) + 1

            var_entra = headers[col_pivote]
            razones = [val_rhs / val_col if val_col > 1e-7 else np.inf for val_col, val_rhs in zip(matrix[1:, col_pivote], matrix[1:, -1])]

            if np.all(np.array(razones) == np.inf):
                out += f"\nSolución no acotada (la variable {var_entra} crece indefinidamente).\n"
                return out, matrix, base_vars, False

            fila_pivote_idx = np.argmin(razones) + 1
            var_sale = base_vars[fila_pivote_idx]
            pivote_val = matrix[fila_pivote_idx, col_pivote]

            out += f"Iteración {iteracion}:\n"
            out += f"Variable entrante: {var_entra} | Variable saliente: {var_sale} | Pivote: {pivote_val:.4f}\n\n"

            matrix[fila_pivote_idx] /= pivote_val
            base_vars[fila_pivote_idx] = var_entra

            for k in range(len(matrix)):
                if k != fila_pivote_idx:
                    matrix[k] -= matrix[k, col_pivote] * matrix[fila_pivote_idx]

            out += self.formato_tabla(headers, base_vars, matrix) + "\n\n"
            iteracion += 1

        out += "\nLímite máximo de iteraciones alcanzado.\n"
        return out, matrix, base_vars, False
    def ejecutar_solver(self):
        self._escribir_en_interfaz("")
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        try:
            metodo = self.cb_metodo.get()
            es_max = self.cb_tipo.get() == "Maximizar"
            c = [float(inp.get()) for inp in self.inputs_fo]
            n_vars, n_rest = len(c), len(self.inputs_rest)

            if metodo == "Método Simplex":
                out = "MÉTODO SIMPLEX\n\n"
                out += f"{'Max' if es_max else 'Min'} Z = " + " + ".join([f"{coef:g}X{i+1}" for i, coef in enumerate(c)]) + "\nSujeto a:\n"

                A_ub, b_ub = [], []
                for coefs, cb_signo, val in self.inputs_rest:
                    r_vals, rhs = [float(inp.get()) for inp in coefs], float(val.get())
                    A_ub.append(r_vals)
                    b_ub.append(rhs)
                    out += "  " + " + ".join([f"{r_vals[j]:g}X{j+1}" for j in range(n_vars)]) + f" {cb_signo.get()} {rhs:g}\n"

                headers = ["Z"] + [f"X{i+1}" for i in range(n_vars)] + [f"S{i+1}" for i in range(n_rest)] + ["Sol"]
                base_vars = ["Z"] + [f"S{i+1}" for i in range(n_rest)]

                z_row = [1.0] + [-coef if es_max else coef for coef in c] + [0.0] * n_rest + [0.0]
                matrix = [z_row]
                for i in range(n_rest):
                    s_vars = [0.0] * n_rest
                    s_vars[i] = 1.0
                    matrix.append([0.0] + A_ub[i] + s_vars + [b_ub[i]])

                matrix = np.array(matrix, dtype=float)
                out += "\nTabla Inicial:\n" + self.formato_tabla(headers, base_vars, matrix) + "\n\n"
                res_out, _, _, _ = self.resolver_simplex_loop(headers, base_vars, matrix, es_max=es_max)
                out += res_out
                self._escribir_en_interfaz(out)


            elif "fase" in metodo.lower():
                out = "MÉTODO DE LAS DOS FASES\n"
                out += "=" * 55 + "\n\n"

                def _formatear_tabla(titulo, nombres_cols, base_vars, mat_tabla):
                    t_str = f"--- {titulo} ---\n"
                    hdr = "Base  | " + " | ".join([f"{v:>6s}" for v in nombres_cols]) + " |    Sol"
                    t_str += hdr + "\n" + "-" * len(hdr) + "\n"

                    z_nombre = "r" if "Fase 1" in titulo else "Z"
                    r_vals = " | ".join([f"{mat_tabla[0, j]:6.2f}" for j in range(len(nombres_cols))])
                    t_str += f"  {z_nombre:3s} | {r_vals} | {mat_tabla[0, -1]:6.2f}\n"
                    t_str += "-" * len(hdr) + "\n"

                    for i, var in enumerate(base_vars):
                        row_vals = " | ".join([f"{mat_tabla[i + 1, j]:6.2f}" for j in range(len(nombres_cols))])
                        t_str += f"{var:5s} | {row_vals} | {mat_tabla[i + 1, -1]:6.2f}\n"

                    t_str += "-" * len(hdr) + "\n\n"
                    return t_str

                # 1. Lectura dinámica de coeficientes
                c_orig = np.array(c, dtype=float)
                num_vars = len(c_orig)
                A_list, b_list, op_list = [], [], []

                for coefs, cb_signo, val in self.inputs_rest:
                    val_str = val.get().strip()
                    if not val_str:
                        continue
                    row_c = [float(coefs[j].get()) for j in range(num_vars)]
                    A_list.append(row_c)
                    b_list.append(float(val_str))
                    op_list.append(cb_signo.get().strip())

                num_rest = len(b_list)

                # Garantizar lados derechos (b) >= 0
                for i in range(num_rest):
                    if b_list[i] < 0:
                        b_list[i] *= -1
                        A_list[i] = [-x for x in A_list[i]]
                        if op_list[i] == "<=":
                            op_list[i] = ">="
                        elif op_list[i] == ">=":
                            op_list[i] = "<="

                # 2. Asignación de variables S (Holgura) y R (Artificiales)
                n_s, n_r = 0, 0
                for op in op_list:
                    if op in ["<=", ">="]:
                        n_s += 1
                    if op in [">=", "="]:
                        n_r += 1

                total_vars = num_vars + n_s + n_r
                nombres_vars = [f"X{i + 1}" for i in range(num_vars)] + \
                               [f"S{i + 1}" for i in range(n_s)] + \
                               [f"R{i + 1}" for i in range(n_r)]

                A_eq = np.zeros((num_rest, total_vars))
                base = []
                art_indices = []

                curr_s, curr_r = num_vars, num_vars + n_s

                for i in range(num_rest):
                    A_eq[i, :num_vars] = A_list[i]
                    op = op_list[i]
                    if op == "<=":
                        A_eq[i, curr_s] = 1.0
                        base.append(nombres_vars[curr_s])
                        curr_s += 1
                    elif op == ">=":
                        A_eq[i, curr_s] = -1.0
                        A_eq[i, curr_r] = 1.0
                        art_indices.append(curr_r)
                        base.append(nombres_vars[curr_r])
                        curr_s += 1
                        curr_r += 1
                    elif op == "=":
                        A_eq[i, curr_r] = 1.0
                        art_indices.append(curr_r)
                        base.append(nombres_vars[curr_r])
                        curr_r += 1

                b_eq = np.array(b_list, dtype=float)

                # =========================================================
                # FASE 1: Minimización de r
                # =========================================================
                out += "========================================\n"
                out += "FASE 1: Minimización de Variables Artificiales (r)\n"
                out += "========================================\n\n"

                tabla = np.zeros((num_rest + 1, total_vars + 1))
                tabla[1:, :-1] = A_eq
                tabla[1:, -1] = b_eq

                # Acondicionamiento correcto de la Fila r:
                # Inicialmente asignamos +1.0 a las variables artificiales en la fila 0
                for r_idx in art_indices:
                    tabla[0, r_idx] = 1.0

                # Hacer 0 el coeficiente de las variables artificiales en la Fila r mediante sustitución
                for i, var in enumerate(base):
                    if var.startswith("R"):
                        tabla[0] -= tabla[i + 1]

                out += _formatear_tabla("Fase 1 - Tabla Inicial", nombres_vars, base, tabla)

                iter_f1 = 0
                max_iter = 50
                while iter_f1 < max_iter:
                    # Criterio de entrada para Minimizar r: buscar el coeficiente más negativo en la fila 0
                    col_piv = np.argmin(tabla[0, :-1])
                    if tabla[0, col_piv] >= -1e-7:
                        break

                    cocientes = []
                    for val_col, val_rhs in zip(tabla[1:, col_piv], tabla[1:, -1]):
                        if val_col > 1e-7:
                            cocientes.append(val_rhs / val_col)
                        else:
                            cocientes.append(np.inf)

                    min_q = np.min(cocientes)
                    if min_q == np.inf:
                        out += "Problema no acotado en la Fase 1.\n"
                        self._escribir_en_interfaz(out)
                        return

                    candidatos = [i for i, q in enumerate(cocientes) if abs(q - min_q) < 1e-7]
                    fil_piv_idx = candidatos[0]
                    for idx in candidatos:
                        if base[idx].startswith("R"):
                            fil_piv_idx = idx
                            break

                    fil_piv = fil_piv_idx + 1

                    out += f"-> Iteración {iter_f1 + 1} (Fase 1): Entra {nombres_vars[col_piv]}, Sale {base[fil_piv - 1]}\n"

                    pivote = tabla[fil_piv, col_piv]
                    tabla[fil_piv] /= pivote
                    for k in range(len(tabla)):
                        if k != fil_piv:
                            tabla[k] -= tabla[k, col_piv] * tabla[fil_piv]

                    base[fil_piv - 1] = nombres_vars[col_piv]
                    iter_f1 += 1

                    out += _formatear_tabla(f"Fase 1 - Tabla Iteración {iter_f1}", nombres_vars, base, tabla)

                r_val = abs(tabla[0, -1])
                out += f"Fase 1 finalizada con r = {r_val:.4f}\n"

                if r_val > 1e-5:
                    out += "-> CONCLUSIÓN: El problema no tiene solución factible.\n"
                    self._escribir_en_interfaz(out)
                    return

                out += "-> CONCLUSIÓN: Variables artificiales eliminadas (r = 0). Existe solución factible.\n\n"

                # =========================================================
                # FASE 2: Optimización de Z
                # =========================================================
                out += "========================================\n"
                out += "FASE 2: Optimización de la Función Objetivo Z\n"
                out += "========================================\n\n"

                cols_validas = [j for j in range(total_vars) if j not in art_indices]
                nombres_f2 = [nombres_vars[j] for j in cols_validas]

                tabla_f2 = np.zeros((num_rest + 1, len(cols_validas) + 1))
                tabla_f2[1:, :-1] = tabla[1:, cols_validas]
                tabla_f2[1:, -1] = tabla[1:, -1]

                # Fila Z: Max Z -> Z - c1*X1 - c2*X2 = 0
                for j in range(num_vars):
                    tabla_f2[0, j] = -c_orig[j] if es_max else c_orig[j]

                # Acondicionar Fila Z con la Base actual
                for i, var in enumerate(base):
                    if var in nombres_f2:
                        var_idx = nombres_f2.index(var)
                        coef_b = tabla_f2[0, var_idx]
                        if abs(coef_b) > 1e-7:
                            tabla_f2[0] -= coef_b * tabla_f2[i + 1]

                out += _formatear_tabla("Fase 2 - Tabla Inicial", nombres_f2, base, tabla_f2)

                iter_f2 = 0
                while iter_f2 < max_iter:
                    if es_max:
                        col_piv = np.argmin(tabla_f2[0, :-1])
                        if tabla_f2[0, col_piv] >= -1e-7:
                            break
                    else:
                        col_piv = np.argmax(tabla_f2[0, :-1])
                        if tabla_f2[0, col_piv] <= 1e-7:
                            break

                    cocientes = []
                    for val_col, val_rhs in zip(tabla_f2[1:, col_piv], tabla_f2[1:, -1]):
                        if val_col > 1e-7:
                            cocientes.append(val_rhs / val_col)
                        else:
                            cocientes.append(np.inf)

                    min_q = np.min(cocientes)
                    if min_q == np.inf:
                        out += "La función objetivo no está acotada.\n"
                        self._escribir_en_interfaz(out)
                        return

                    candidatos = [i for i, q in enumerate(cocientes) if abs(q - min_q) < 1e-7]
                    fil_piv_idx = candidatos[0]
                    for idx in candidatos:
                        if tabla_f2[idx + 1, -1] > 1e-7:
                            fil_piv_idx = idx
                            break

                    fil_piv = fil_piv_idx + 1

                    out += f"-> Iteración {iter_f2 + 1} (Fase 2): Entra {nombres_f2[col_piv]}, Sale {base[fil_piv - 1]}\n"

                    pivote = tabla_f2[fil_piv, col_piv]
                    tabla_f2[fil_piv] /= pivote
                    for k in range(len(tabla_f2)):
                        if k != fil_piv:
                            tabla_f2[k] -= tabla_f2[k, col_piv] * tabla_f2[fil_piv]

                    base[fil_piv - 1] = nombres_f2[col_piv]
                    iter_f2 += 1

                    out += _formatear_tabla(f"Fase 2 - Tabla Iteración {iter_f2}", nombres_f2, base, tabla_f2)

                z_opt = tabla_f2[0, -1] if es_max else -tabla_f2[0, -1]
                out += "========================================\n"
                out += "SOLUCIÓN ÓPTIMA ALCANZADA\n"
                out += "========================================\n"
                out += f"-> Valor Óptimo Z = {abs(z_opt):.2f}\n"

                for j in range(num_vars):
                    var_nombre = f"X{j + 1}"
                    if var_nombre in base:
                        val_var = tabla_f2[base.index(var_nombre) + 1, -1]
                        out += f"-> {var_nombre} = {abs(val_var):.2f}\n"
                    else:
                        out += f"-> {var_nombre} = 0.00\n"

                self._escribir_en_interfaz(out)

            elif metodo == "Método Gráfico":
                import itertools

                out = "MÉTODO GRÁFICO - PROCEDIMIENTO PASO A PASO\n\n"

                out += f"Función Objetivo:\n  {'Max' if es_max else 'Min'} Z = {c[0]:g}X1 + {c[1]:g}X2\n\nSujeto a:\n"

                lineas = []
                restricciones = []

                for idx, (coefs, cb_signo, val) in enumerate(self.inputs_rest):
                    val_str = val.get().strip()
                    if not val_str:
                        continue
                    a = float(coefs[0].get())
                    b = float(coefs[1].get())
                    rhs = float(val_str)
                    op = cb_signo.get().strip()

                    nombre_r = f"R{idx + 1}"
                    out += f"  {nombre_r}: {a:g}X1 + {b:g}X2 {op} {rhs:g}\n"
                    lineas.append((a, b, rhs, nombre_r))
                    restricciones.append((a, b, op, rhs))

                # Agregar restricciones de no negatividad / ejes cartesianos
                lineas.append((1, 0, 0, "Eje X2 (X1=0)"))
                lineas.append((0, 1, 0, "Eje X1 (X2=0)"))
                restricciones.append((1, 0, ">=", 0))
                restricciones.append((0, 1, ">=", 0))

                out += "\n----------------------------------------\n"
                out += "PASO 1: Identificación de Puntos de Intersección\n"
                out += "----------------------------------------\n"

                puntos_interseccion = []
                # 1. Encontrar intersecciones asociando el nombre de cada línea
                for (l1, l2) in itertools.combinations(lineas, 2):
                    A_mat = np.array([[l1[0], l1[1]], [l2[0], l2[1]]], dtype=float)
                    B_mat = np.array([l1[2], l2[2]], dtype=float)

                    if abs(np.linalg.det(A_mat)) > 1e-7:
                        pt = np.linalg.solve(A_mat, B_mat)
                        puntos_interseccion.append((pt[0], pt[1], l1[3], l2[3]))

                puntos_factibles = []
                intersecciones_validas = []
                tol = 1e-5

                # 2. Filtrar puntos factibles y guardar el nombre de las líneas cruzadas
                for px, py, n1, n2 in puntos_interseccion:
                    if px < -tol or py < -tol:
                        continue

                    cumple = True
                    for a, b, op, rhs in restricciones:
                        val_eval = a * px + b * py
                        if op == "<=" and val_eval > rhs + tol:
                            cumple = False;
                            break
                        elif op == ">=" and val_eval < rhs - tol:
                            cumple = False;
                            break
                        elif op == "=" and abs(val_eval - rhs) > tol:
                            cumple = False;
                            break

                    if cumple:
                        ya_existe = any(abs(pf[0] - px) < tol and abs(pf[1] - py) < tol for pf in puntos_factibles)
                        if not ya_existe:
                            puntos_factibles.append((round(px, 4), round(py, 4)))

                            # Formatear la etiqueta de la intersección
                            if "Eje" in n1 and "Eje" in n2:
                                tag = "Origen"
                            elif "Eje" in n1:
                                tag = f"{n2} y {n1}"
                            elif "Eje" in n2:
                                tag = f"{n1} y {n2}"
                            else:
                                tag = f"{n1} y {n2}"

                            intersecciones_validas.append((tag, round(px, 4), round(py, 4)))

                if not puntos_factibles:
                    out += "No se encontraron puntos de intersección factibles.\n"
                    self._escribir_en_interfaz(out)
                    return

                for tag, px, py in intersecciones_validas:
                    out += f"• Intersección {tag}: ({px:g}, {py:g})\n"

                # 3. Evaluación en Z
                out += "\n----------------------------------------\n"
                out += "PASO 2: Evaluación de Vértices en la Función Objetivo\n"
                out += "----------------------------------------\n"

                resultados = []
                for px, py in puntos_factibles:
                    z_val = c[0] * px + c[1] * py
                    resultados.append((z_val, px, py))
                    out += f"• Punto ({px:g}, {py:g}):\n"
                    out += f"  Z = {c[0]:g}({px:g}) + {c[1]:g}({py:g}) = {z_val:.2f}\n\n"

                # 4. Solución Óptima
                out += "----------------------------------------\n"
                out += "PASO 3: Determinación de la Solución Óptima\n"
                out += "----------------------------------------\n"

                if es_max:
                    opt_z, opt_x1, opt_x2 = max(resultados, key=lambda item: item[0])
                else:
                    opt_z, opt_x1, opt_x2 = min(resultados, key=lambda item: item[0])

                out += f"El valor {'máximo' if es_max else 'mínimo'} de Z se alcanza en el punto ({opt_x1:g}, {opt_x2:g}).\n"
                out += f"-> Solución Óptima: X1 = {opt_x1:g}, X2 = {opt_x2:g}\n"
                out += f"-> Valor Óptimo Z = {opt_z:.2f}\n"

                self._escribir_en_interfaz(out)

                # 5. Renderizado Gráfico Dinámico con Matplotlib
                fig, ax = plt.subplots(figsize=(5, 4))

                max_x = max([pt[0] for pt in puntos_factibles] + [10]) * 1.4
                max_y = max([pt[1] for pt in puntos_factibles] + [10]) * 1.4
                x_vals = np.linspace(0, max_x, 300)

                for idx, (a, b, op, rhs) in enumerate(restricciones[:-2]):
                    if abs(b) > 1e-7:
                        ax.plot(x_vals, (rhs - a * x_vals) / b, label=f'R{idx + 1}: {a:g}X1+{b:g}X2 {op} {rhs:g}')
                    else:
                        ax.axvline(x=rhs / a, label=f'R{idx + 1}: {a:g}X1 {op} {rhs:g}', linestyle='--')

                if len(puntos_factibles) >= 3:
                    cx = np.mean([pt[0] for pt in puntos_factibles])
                    cy = np.mean([pt[1] for pt in puntos_factibles])
                    pts_ordenados = sorted(puntos_factibles, key=lambda pt: np.arctan2(pt[1] - cy, pt[0] - cx))
                    pts_arr = np.array(pts_ordenados)
                    ax.fill(pts_arr[:, 0], pts_arr[:, 1], color='#f43f5e', alpha=0.35, label='Región Factible')

                for px, py in puntos_factibles:
                    ax.plot(px, py, 'ro', markersize=6)
                    ax.annotate(f"({px:g},{py:g})", (px + max_x * 0.02, py + max_y * 0.02), fontsize=8, color="white",
                                weight="bold")

                # ax.plot(opt_x1, opt_x2, 'go', markersize=9, label=f'Óptimo ({opt_x1:g}, {opt_x2:g})')

                ax.set_xlim(0, max_x)
                ax.set_ylim(0, max_y)
                ax.grid(True, linestyle="--", alpha=0.4)
                ax.set_xlabel("X1")
                ax.set_ylabel("X2")
                ax.legend(fontsize=7, loc='upper right')

                fig.patch.set_facecolor("#1e293b")
                ax.set_facecolor("#0f172a")
                ax.xaxis.label.set_color("white")
                ax.yaxis.label.set_color("white")
                ax.tick_params(colors="white")

                self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill="both", expand=True)


        except Exception as e:
            messagebox.showerror("Error de Cálculo", f"Verifica los datos ingresados.\n\nDetalles: {e}")

    def _escribir_en_interfaz(self, texto):
        # Permite la escritura en el área de texto, limpia el contenido previo y refresca la vista
        if hasattr(self, 'box_procedimiento'):
            try:
                self.box_procedimiento.configure(state="normal")
            except Exception:
                pass

            # Limpiar contenido anterior
            if hasattr(self.box_procedimiento, 'delete'):
                self.box_procedimiento.delete("1.0", "end")
                self.box_procedimiento.insert("1.0", texto)

            try:
                self.box_procedimiento.configure(state="disabled")
            except Exception:
                pass

if __name__ == "__main__":
    app = AppCalculadora()
    app.mainloop()