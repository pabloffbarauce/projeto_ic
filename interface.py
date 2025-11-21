import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import calculos
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class programa:
    def __init__(self, root):
        self.janela = root
        self.janela.title("programa")
        self.janela.geometry("1100x750")

        # janela
        main_container = tk.Frame(self.janela)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # painel esquerdo
        left_frame = tk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # área de entrada dos dados
        tk.Label(left_frame, text="Entrada de Dados", font=("Arial", 12, "bold")).pack(pady=5)

        input_container = tk.Frame(left_frame)
        input_container.pack(pady=5)

        # coluna X
        frame_x = tk.Frame(input_container)
        frame_x.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_x, text="Tempo (X)", font=("Arial", 9, "bold")).pack()
        self.txt_input_x = scrolledtext.ScrolledText(frame_x, width=12, height=10)
        self.txt_input_x.pack()

        # coluna Y
        frame_y = tk.Frame(input_container)
        frame_y.pack(side=tk.LEFT, padx=5)
        tk.Label(frame_y, text="Conc. (Y)", font=("Arial", 9, "bold")).pack()
        self.txt_input_y = scrolledtext.ScrolledText(frame_y, width=12, height=10)
        self.txt_input_y.pack()

        # botões
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(pady=10, fill=tk.X)
        tk.Button(btn_frame, text="Exemplo", command=self.example).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpar", command=self.clean_data).pack(side=tk.LEFT, padx=5)

        self.btn_calc = tk.Button(left_frame, text="CALCULAR & PLOTAR", command=self.data_processing,
                                  bg="#4caf50", fg="white", font=("Arial", 10, "bold"), height=2)
        self.btn_calc.pack(fill=tk.X, pady=5)

        # resumos das estatísticas
        results_frame = tk.LabelFrame(left_frame, text="Resumo Estatístico", font=("Arial", 9, "bold"))
        results_frame.pack(fill=tk.X, pady=5)

        self.res_labels = {}
        vars_to_show = [("Máximo Y", "max_y"), ("Tempo Hid. (θh)", "th"),
                        ("Variância (σ²)", "var"), ("N (Tanques)", "N")]

        # grid para estatísticas
        for idx, (titulo, key) in enumerate(vars_to_show):
            tk.Label(results_frame, text=titulo + ":", font=("Arial", 9)).grid(row=idx, column=0, sticky="e", padx=5,
                                                                               pady=2)
            lbl = tk.Label(results_frame, text="---", font=("Arial", 9, "bold"), fg="#2196f3")
            lbl.grid(row=idx, column=1, sticky="w", padx=5, pady=2)
            self.res_labels[key] = lbl

        #  valores F
        lbl_tabela = tk.Label(left_frame, text="Tabela de Dados: Curva F", font=("Arial", 10, "bold"))
        lbl_tabela.pack(pady=(10, 0))

        # container pra tabela e rolagem
        tree_frame = tk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # colunas
        columns = ('tempo', 'valor_f')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)

        # eixos do gráfico
        self.tree.heading('tempo', text='Tempo (min)')
        self.tree.heading('valor_f', text='Valor F(t)')

        # Tamanho das colunas
        self.tree.column('tempo', width=80, anchor='center')
        self.tree.column('valor_f', width=100, anchor='center')

        # barra de rolagem
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # gráfico

        # grafico preenchendo o resto do programa
        right_frame = tk.Frame(main_container, bg="white", bd=2, relief=tk.GROOVE)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # começar pequeno
        self.figure = Figure(figsize=(4, 3), dpi=100)

        # nao cortar eixos
        self.figure.set_tight_layout(True)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Aguardando dados...")
        self.ax.set_xlabel("Tempo")
        self.ax.set_ylabel("F(t)")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, master=right_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def clean_data(self):
        self.txt_input_x.delete(1.0, tk.END)
        self.txt_input_y.delete(1.0, tk.END)
        for key in self.res_labels: self.res_labels[key].config(text="---")

        # limpar gráfico
        self.ax.clear()
        self.ax.set_title("Aguardando dados...")
        self.ax.grid(True)
        # reaplicar o tight_layout depois de limpar
        self.figure.set_tight_layout(True)
        self.canvas.draw()

        # limpa tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

    def ler_campo_texto(self, widget_texto):
        conteudo = widget_texto.get(1.0, tk.END)
        lista_numeros = []
        for linha in conteudo.split('\n'):
            linha = linha.strip()
            if linha:
                try:
                    valor = float(linha.replace(',', '.'))
                    lista_numeros.append(valor)
                except ValueError:
                    raise ValueError(f"Valor inválido: '{linha}'")
        return lista_numeros

    def example(self):
        self.clean_data()
        x_exemplo = "0.25\n0.5\n0.75\n1\n1.25\n1.5\n1.75\n2\n2.25\n2.5\n2.75\n3\n3.25\n3.5\n3.75\n4\n4.25\n4.5\n4.75\n5\n5.25\n5.5\n5.75\n6\n6.25\n6.5\n6.75"
        y_exemplo = "0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0.064053751\n0.131690929\n0.154087346\n0.16019037\n0.176315789\n0.180011198\n0.178443449\n0.180011198\n0.191041433\n0.183706607\n0.182754759\n0.182866741\n0.18980963\n0.199384099\n0.193673012"
        self.txt_input_x.insert(tk.END, x_exemplo)
        self.txt_input_y.insert(tk.END, y_exemplo)

    def data_processing(self):
        try:
            x_data = self.ler_campo_texto(self.txt_input_x)
            y_data = self.ler_campo_texto(self.txt_input_y)

            if len(x_data) != len(y_data) or len(x_data) == 0:
                messagebox.showerror("Erro", "Quantidades de X e Y diferem ou estão vazias.")
                return

            # cálculos
            x_y_curve = calculos.initial_data(x_data, y_data)

            treated_curve = calculos.boltzmann(x_data, x_y_curve)
            if treated_curve is None:
                messagebox.showerror("Erro", "Erro ao ajustar curva (Boltzman falhou).")
                return

            f_curve, y_max = calculos.f_curve_calc(treated_curve)
            stats = calculos.final_stats(x_data, f_curve)

            # 3. passando os resultados pra tela
            self.res_labels["max_y"].config(text=f"{y_max:.4f}")
            self.res_labels["th"].config(text=f"{stats['hydraulic_time']:.4f}")
            self.res_labels["var"].config(text=f"{stats['variance']:.4f}")
            # destacando N
            self.res_labels["N"].config(text=f"{stats['N']:.2f}")

            # preencher a tabela
            # limpar dados
            for item in self.tree.get_children():
                self.tree.delete(item)

            # novos dados de x e y
            for i in range(len(x_data)):
                val_x = x_data[i]
                val_f = f_curve[i]

                # inserir na tabela formatado
                self.tree.insert("", "end", values=(f"{val_x:.2f}", f"{val_f:.5f}"))

            # atualizar gráfico
            self.ax.clear()
            self.ax.plot(x_data, f_curve, label='Curva F(t)', color='blue', linewidth=2)
            self.ax.fill_between(x_data, f_curve, alpha=0.1, color='blue')

            # referencia visual F = 1
            self.ax.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='Limite F=1')

            self.ax.set_title("Curva F: Distribuição Cumulativa")
            self.ax.set_xlabel("Tempo")
            self.ax.set_ylabel("F(t)")
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.legend()

        except ValueError as ve:
            messagebox.showerror("Erro de Formato", str(ve))
        except Exception as e:
            messagebox.showerror("Erro Crítico", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = programa(root)
    root.mainloop()