import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, filedialog
import calculos
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class programa:
    def __init__(self, root):
        self.janela = root
        self.janela.title("Análise Hidrodinâmica")
        self.janela.geometry("800x600")
        self.janela.after(800, lambda: self.janela.geometry("1600x900"))

        self.last_x = None
        self.last_y = None
        self.last_treated = None
        self.last_f_curve = None
        self.last_stats = None

        main_container = tk.Frame(self.janela)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Label(left_frame, text="Entrada de Dados", font=("Arial", 12, "bold")).pack(pady=5)

        input_container = tk.Frame(left_frame)
        input_container.pack(pady=5)

        frame_x = tk.Frame(input_container)
        frame_x.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_x, text="Tempo (X)", font=("Arial", 9, "bold")).pack()
        self.txt_input_x = scrolledtext.ScrolledText(frame_x, width=12, height=10)
        self.txt_input_x.pack()
        self.lbl_count_x = tk.Label(frame_x, text="Elementos: 0", font=("Arial", 8, "italic"))
        self.lbl_count_x.pack()

        frame_y = tk.Frame(input_container)
        frame_y.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_y, text="Concentração (Y)", font=("Arial", 9, "bold")).pack()
        self.txt_input_y = scrolledtext.ScrolledText(frame_y, width=12, height=10)
        self.txt_input_y.pack()
        self.lbl_count_y = tk.Label(frame_y, text="Elementos: 0", font=("Arial", 8, "italic"))
        self.lbl_count_y.pack()

        self.txt_input_x.bind("<KeyRelease>", self.update_counters)
        self.txt_input_y.bind("<KeyRelease>", self.update_counters)

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(pady=10, fill=tk.X)
        tk.Button(btn_frame, text="Exemplo", command=self.example).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpar", command=self.clean_data).pack(side=tk.LEFT, padx=5)

        self.btn_calc = tk.Button(left_frame, text="CALCULAR & PLOTAR", command=self.data_processing,
                                  bg="#4caf50", fg="white", font=("Arial", 10, "bold"), height=2)
        self.btn_calc.pack(fill=tk.X, pady=5)

        self.btn_export = tk.Button(left_frame, text="EXPORTAR .XLSX", command=self.export_excel,
                                    bg="#2196f3", fg="white", font=("Arial", 10, "bold"), height=2)
        self.btn_export.pack(fill=tk.X, pady=5)

        results_frame = tk.LabelFrame(left_frame, text="Resumo Estatístico", font=("Arial", 9, "bold"))
        results_frame.pack(fill=tk.X, pady=5)

        self.res_labels = {}
        vars_to_show = [("Máximo Y", "max_y"), ("Tempo Hid. (θh)", "th"),
                        ("Variância (σ²)", "var"), ("N (Tanques)", "N")]

        for idx, (titulo, key) in enumerate(vars_to_show):
            tk.Label(results_frame, text=titulo + ":", font=("Arial", 9)).grid(row=idx, column=0, sticky="e", padx=5,
                                                                               pady=2)
            lbl = tk.Label(results_frame, text="---", font=("Arial", 9, "bold"), fg="#2196f3")
            lbl.grid(row=idx, column=1, sticky="w", padx=5, pady=2)
            self.res_labels[key] = lbl

        lbl_tabela = tk.Label(left_frame, text="Tabela de Dados: Curva F", font=("Arial", 10, "bold"))
        lbl_tabela.pack(pady=(10, 0))

        tree_frame = tk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ('tempo', 'valor_f')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        self.tree.heading('tempo', text='Tempo (min)')
        self.tree.heading('valor_f', text='Valor F(t)')
        self.tree.column('tempo', width=80, anchor='center')
        self.tree.column('valor_f', width=100, anchor='center')

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        right_frame = tk.Frame(main_container, bg="white", bd=2, relief=tk.GROOVE)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.figure = Figure(figsize=(8, 7), dpi=100)
        self.figure.tight_layout()
        self.figure.subplots_adjust(hspace=0.6)

        self.ax1 = self.figure.add_subplot(211)
        self.ax1.set_ylim(0, 1)
        self.ax1.set_title("Curva C: Dados Brutos")
        self.ax1.grid(True)

        self.ax2 = self.figure.add_subplot(212)
        self.ax2.set_ylim(0, 1)
        self.ax2.set_title("Curva C: Ajuste de Boltzmann")
        self.ax2.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        self.canvas.draw()

    def update_counters(self, event=None):
        def count_valid_lines(widget):
            content = widget.get(1.0, tk.END).strip()
            if not content:
                return 0
            return len([line for line in content.split('\n') if line.strip()])

        nx = count_valid_lines(self.txt_input_x)
        ny = count_valid_lines(self.txt_input_y)

        color = "black" if nx == ny else "red"

        self.lbl_count_x.config(text=f"Elementos: {nx}", fg=color)
        self.lbl_count_y.config(text=f"Elementos: {ny}", fg=color)

    def clean_data(self):
        self.txt_input_x.delete(1.0, tk.END)
        self.txt_input_y.delete(1.0, tk.END)
        for key in self.res_labels: self.res_labels[key].config(text="---")

        self.last_x = None
        self.last_y = None
        self.last_treated = None
        self.last_f_curve = None
        self.last_stats = None

        self.update_counters()

        self.ax1.cla()
        self.ax1.set_ylim(0, 1)
        self.ax1.set_title("Curva C: Dados Brutos")
        self.ax1.grid(True)

        self.ax2.cla()
        self.ax2.set_ylim(0, 1)
        self.ax2.set_title("Curva C: Ajuste de Boltzmann")
        self.ax2.grid(True)

        self.canvas.draw_idle()

        for item in self.tree.get_children():
            self.tree.delete(item)

    def ler_campo_texto(self, widget_texto):
        conteudo = widget_texto.get(1.0, tk.END)
        lista_num = []
        for linha in conteudo.split('\n'):
            linha = linha.strip()
            if linha:
                try:
                    lista_num.append(float(linha.replace(',', '.')))
                except ValueError:
                    raise ValueError(f"Valor inválido: '{linha}'")
        return lista_num

    def example(self):
        self.clean_data()
        x_ex = "0\n90\n180\n210\n300\n420\n450\n480\n510\n540\n570\n600\n630\n660\n690\n720\n750\n780\n810\n840\n870\n900\n930\n960\n990\n1020\n1050\n1110\n1170\n1260\n1380\n1470\n1620\n1770\n2100"
        y_ex = "0.0005\n0.0011\n0.0014\n0.0016\n0.0019\n0.0025\n0.0045\n0.0052\n0.0058\n0.0070\n0.0083\n0.0108\n0.0149\n0.0326\n0.0333\n0.0363\n0.0529\n0.0557\n0.0659\n0.0885\n0.0895\n0.1020\n0.1074\n0.1245\n0.1381\n0.1518\n0.1709\n0.1813\n0.1822\n0.2029\n0.2081\n0.2174\n0.2239\n0.2275\n0.2314"
        self.txt_input_x.insert(tk.END, x_ex)
        self.txt_input_y.insert(tk.END, y_ex)
        self.update_counters()

    def data_processing(self):
        try:
            x_data = self.ler_campo_texto(self.txt_input_x)
            y_data = self.ler_campo_texto(self.txt_input_y)

            if len(x_data) != len(y_data) or not x_data:
                messagebox.showerror("Erro",
                                     f"As colunas X ({len(x_data)}) e Y ({len(y_data)}) precisam ter a mesma quantidade de elementos.")
                return

            treated_curve, params, cov = calculos.boltzmann(x_data, y_data)
            y_adjusted = [p[1] for p in treated_curve]

            f_curve, y_max = calculos.f_curve_calc(treated_curve)
            stats = calculos.final_stats(x_data, f_curve)

            self.last_x = x_data
            self.last_y = y_data
            self.last_treated = treated_curve
            self.last_f_curve = f_curve
            self.last_stats = stats

            self.res_labels["max_y"].config(text=f"{y_max:.4f}")
            self.res_labels["th"].config(text=f"{stats['hydraulic_time']:.4f}")
            self.res_labels["var"].config(text=f"{stats['variance']:.4f}")
            self.res_labels["N"].config(text=f"{stats['N']:.2f}")

            for item in self.tree.get_children(): self.tree.delete(item)
            for i in range(len(x_data)):
                self.tree.insert("", "end", values=(f"{x_data[i]:.2f}", f"{f_curve[i]:.5f}"))

            y_min_raw = min(min(y_data), min(y_adjusted))
            y_max_raw = max(max(y_data), max(y_adjusted))
            margin = (y_max_raw - y_min_raw) * 0.1 if y_max_raw != y_min_raw else 1

            self.ax1.clear()
            self.ax1.scatter(x_data, y_data, color='red', s=15, label='Experimental')
            self.ax1.plot(x_data, y_data, color='red', alpha=0.3, linestyle='--')
            self.ax1.set_ylim(y_min_raw - margin, y_max_raw + margin)
            self.ax1.set_title("Curva C: Dados Brutos")
            self.ax1.set_ylabel("C(t)")
            self.ax1.set_xlabel("Tempo (min)")
            self.ax1.grid(True, linestyle=':', alpha=0.7)
            self.ax1.legend()

            self.ax2.clear()
            self.ax2.plot(x_data, y_adjusted, color='blue', linewidth=2, label='Ajuste Boltzmann')
            self.ax2.fill_between(x_data, y_adjusted, color='blue', alpha=0.1)
            self.ax2.set_ylim(y_min_raw - margin, y_max_raw + margin)
            self.ax2.set_title("Curva C: Concentração Ajustada")
            self.ax2.set_xlabel("Tempo (min)")
            self.ax2.set_ylabel("C(t)")
            self.ax2.grid(True, linestyle=':', alpha=0.7)
            self.ax2.legend()

            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def export_excel(self):
        if self.last_stats is None:
            messagebox.showwarning("Aviso", "Calcule os dados antes de exportar (clique em CALCULAR & PLOTAR).")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Planilha Excel", "*.xlsx")],
            title="Salvar resultados como"
        )
        if not path:
            return

        try:
            calculos.export_to_excel(
                path, self.last_x, self.last_y, self.last_treated,
                self.last_f_curve, self.last_stats
            )
            messagebox.showinfo("Sucesso", f"Arquivo exportado em:\n{path}")
        except Exception as e:
            messagebox.showerror("Erro ao exportar", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = programa(root)
    root.mainloop()