"""Calculadora PRN - App principal con pestañas (Generadores / Pruebas / Variables)
Ejecutar: python main.py
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

# algoritmos
from algorithms.cuadrados_medios import cuadrados_medios
from algorithms.productos_medios import productos_medios
from algorithms.multiplicador_constante import multiplicador_constante

# pruebas
from pruebas import prueba_medias, prueba_varianza, prueba_uniformidad

# util export
from utils.export import export_csv, export_xlsx

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Calculadora PRN - Notebook')
        self.geometry('1000x700')
        self.create_widgets()

    def create_widgets(self):
        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True)

        self.tab_generadores = ttk.Frame(nb)
        self.tab_pruebas = ttk.Frame(nb)
        self.tab_variables = ttk.Frame(nb)

        nb.add(self.tab_generadores, text='Generadores')
        nb.add(self.tab_pruebas, text='Pruebas')
        nb.add(self.tab_variables, text='Variables')

        self.build_generadores(self.tab_generadores)
        self.build_pruebas(self.tab_pruebas)
        self.build_variables(self.tab_variables)

    # ---------------- Generadores ----------------
    def build_generadores(self, parent):
        frm_left = ttk.Frame(parent, width=320)
        frm_left.pack(side='left', fill='y', padx=8, pady=8)
        frm_right = ttk.Frame(parent)
        frm_right.pack(side='left', fill='both', expand=True, padx=8, pady=8)

        # Selector algoritmo
        ttk.Label(frm_left, text='Algoritmo').pack(anchor='w', pady=(4,2))
        self.algo_var = tk.StringVar(value='cuadrados')
        ttk.Radiobutton(frm_left, text='Cuadrados Medios', variable=self.algo_var, value='cuadrados').pack(anchor='w')
        ttk.Radiobutton(frm_left, text='Productos Medios', variable=self.algo_var, value='productos').pack(anchor='w')
        ttk.Radiobutton(frm_left, text='Multiplicador Constante', variable=self.algo_var, value='constante').pack(anchor='w')

        ttk.Separator(frm_left, orient='horizontal').pack(fill='x', pady=6)

        # Parámetros comunes
        ttk.Label(frm_left, text='Dígitos (n)').pack(anchor='w', pady=(4,0))
        self.n_var = tk.IntVar(value=4)
        ttk.Entry(frm_left, textvariable=self.n_var).pack(fill='x', pady=2)

        ttk.Label(frm_left, text='Cantidad (N)').pack(anchor='w', pady=(4,0))
        self.N_var = tk.IntVar(value=20)
        ttk.Entry(frm_left, textvariable=self.N_var).pack(fill='x', pady=2)

        ttk.Label(frm_left, text='Alpha (significancia)').pack(anchor='w', pady=(4,0))
        self.alpha_var = tk.DoubleVar(value=0.05)
        self.alpha_cb = ttk.Combobox(frm_left, values=['0.10','0.05','0.01'])
        self.alpha_cb.set('0.05')
        self.alpha_cb.pack(fill='x', pady=2)

        ttk.Separator(frm_left, orient='horizontal').pack(fill='x', pady=6)

        # Semillas / A
        ttk.Label(frm_left, text='Semilla X0').pack(anchor='w', pady=(4,0))
        self.s0_var = tk.StringVar(value='5015')
        ttk.Entry(frm_left, textvariable=self.s0_var).pack(fill='x', pady=2)

        ttk.Label(frm_left, text='Semilla X1 (productos)').pack(anchor='w', pady=(4,0))
        self.s1_var = tk.StringVar(value='5739')
        ttk.Entry(frm_left, textvariable=self.s1_var).pack(fill='x', pady=2)

        ttk.Label(frm_left, text='Constante A (multiplicador)').pack(anchor='w', pady=(4,0))
        self.a_var = tk.StringVar(value='4547')
        ttk.Entry(frm_left, textvariable=self.a_var).pack(fill='x', pady=2)

        ttk.Button(frm_left, text='Generar', command=self.generar).pack(fill='x', pady=(12,6))
        ttk.Button(frm_left, text='Exportar CSV', command=self.export_current_csv).pack(fill='x', pady=4)
        ttk.Button(frm_left, text='Exportar XLSX', command=self.export_current_xlsx).pack(fill='x', pady=4)

        # Right: tabla + gráfica
        self.table = ttk.Treeview(frm_right, columns=('i','y','x','r'), show='headings', height=18)
        for c in ('i','y','x','r'):
            self.table.heading(c, text=c)
        self.table.pack(fill='both', expand=True)

        # plot area
        fig = plt.Figure(figsize=(6,2.5))
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=frm_right)
        self.canvas.get_tk_widget().pack(fill='both', expand=False, pady=6)

    def generar(self):
        try:
            n = int(self.n_var.get())
            N = int(self.N_var.get())
            algo = self.algo_var.get()
            s0 = int(self.s0_var.get())
            s1 = int(self.s1_var.get())
            a = int(self.a_var.get())
        except Exception as e:
            messagebox.showerror('Error','Verifique entradas numéricas.\n'+str(e))
            return

        if algo == 'cuadrados':
            rows = cuadrados_medios(s0, n, N)
        elif algo == 'productos':
            rows = productos_medios(s0, s1, n, N)
        else:
            rows = multiplicador_constante(s0, a, n, N)

        # rows: list of tuples (i,y,x,r)
        self.current_rows = rows
        # poblar tabla
        for it in self.table.get_children():
            self.table.delete(it)
        for r in rows:
            self.table.insert('', 'end', values=(r[0], r[1], r[2], f"{r[3]:.{n}f}"))

        rs = [r[3] for r in rows]
        xs = [r[0] for r in rows]
        self.ax.clear()
        self.ax.plot(xs, rs, marker='o', linewidth=1)
        self.ax.set_title('r por iteración')
        self.ax.set_ylim(-0.05,1.05)
        self.canvas.draw()

    def export_current_csv(self):
        rows = getattr(self, 'current_rows', None)
        if not rows:
            messagebox.showinfo('Info','Primero genere una secuencia.')
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV','*.csv')])
        if not path:
            return
        export_csv(path, rows)
        messagebox.showinfo('Exportado', f'CSV guardado en:\n{path}')

    def export_current_xlsx(self):
        rows = getattr(self, 'current_rows', None)
        if not rows:
            messagebox.showinfo('Info','Primero genere una secuencia.')
            return
        path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('XLSX','*.xlsx')])
        if not path:
            return
        export_xlsx(path, rows)
        messagebox.showinfo('Exportado', f'XLSX guardado en:\n{path}')

    # ---------------- Pruebas ----------------
    def build_pruebas(self, parent):
        frm_top = ttk.Frame(parent)
        frm_top.pack(fill='x', padx=8, pady=8)
        frm_bot = ttk.Frame(parent)
        frm_bot.pack(fill='both', expand=True, padx=8, pady=8)

        ttk.Label(frm_top, text='Seleccionar prueba:').pack(side='left', padx=4)
        self.test_var = tk.StringVar(value='medias')
        ttk.Radiobutton(frm_top, text='Medias (Z)', variable=self.test_var, value='medias').pack(side='left', padx=4)
        ttk.Radiobutton(frm_top, text='Varianza (Chi2)', variable=self.test_var, value='varianza').pack(side='left', padx=4)
        ttk.Radiobutton(frm_top, text='Uniformidad (K-S)', variable=self.test_var, value='ks').pack(side='left', padx=4)

        ttk.Button(frm_top, text='Ejecutar prueba sobre última secuencia', command=self.run_chosen_test).pack(side='right', padx=4)

        # Resultado textual + histograma/tablas abajo
        self.result_text = tk.Text(frm_bot, height=6)
        self.result_text.pack(fill='x', pady=6)

        # Frequencies table + histogram
        self.freq_table = ttk.Treeview(frm_bot, columns=('interval','obs','exp'), show='headings', height=8)
        for c in ('interval','obs','exp'):
            self.freq_table.heading(c, text=c)
        self.freq_table.pack(fill='x', pady=6)

        fig2 = plt.Figure(figsize=(6,2.5))
        self.ax2 = fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(fig2, master=frm_bot)
        self.canvas2.get_tk_widget().pack(fill='both', expand=True)

    def run_chosen_test(self):
        rows = getattr(self, 'current_rows', None)
        if not rows:
            messagebox.showinfo('Info','Primero genere la secuencia desde Generadores.')
            return
        rs = [r[3] for r in rows]
        alpha = float(self.alpha_cb.get()) if hasattr(self,'alpha_cb') else 0.05
        res = ''
        if self.test_var.get() == 'medias':
            res = prueba_medias(rs, alpha)
        elif self.test_var.get() == 'varianza':
            res = prueba_varianza(rs, alpha)
        else:
            res = prueba_uniformidad(rs, alpha)

        # mostrar resultado textual
        self.result_text.delete('1.0','end')
        self.result_text.insert('end', res if isinstance(res,str) else str(res))

        # tabla de frecuencias + histograma siempre (k = int(sqrt(N)) as default)
        k = max(5, int(len(rs)**0.5))
        counts, edges = np.histogram(rs, bins=k, range=(0,1))
        expected = [len(rs)/k]*k
        for it in self.freq_table.get_children():
            self.freq_table.delete(it)
        for i in range(k):
            rng = f"[{edges[i]:.3f}, {edges[i+1]:.3f})"
            self.freq_table.insert('', 'end', values=(rng, int(counts[i]), float(expected[i])))

        self.ax2.clear()
        self.ax2.bar(range(k), counts, align='center')
        self.ax2.set_title('Histograma (conteos)')
        self.canvas2.draw()

    # ---------------- Variables ----------------
    def build_variables(self, parent):
        frm = ttk.Frame(parent)
        frm.pack(fill='both', expand=True, padx=12, pady=12)
        ttk.Label(frm, text='Parámetros globales y material de entrega', font=('Arial',12,'bold')).pack(anchor='w', pady=4)
        txt = tk.Text(frm)
        texto = (
            "Proyecto: Calculadora PRN\n"
            "Lenguaje: Python 3.10+\n"
            "Dependencias: numpy, pandas, matplotlib, scipy\n\n"
            "Instrucciones: Generar secuencia en pestaña Generadores; luego en Pruebas ejecutar test.\n"
        )
        txt.insert('1.0', texto)
        txt.configure(state='disabled')
        txt.pack(fill='both', expand=True)

if __name__ == '__main__':
    app = App()
    app.mainloop()
