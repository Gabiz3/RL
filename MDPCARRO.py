import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox

class CarroMDP:
    def __init__(self):
        self.estados = [
            "Desligado", "Ligado", "Bateria Fraca", "Pane Elétrica", "Pronto para Uso",
            "Falha no Motor", "Bateria Recarregada", "Bateria Morta", "Superaquecido",
            "Sistema Estável", "Curto-circuito", "Ligação Forçada", "Problema Resolvido",
            "Alternador Ruim", "Sucesso Parcial", "Falha Total", "Novo Sistema Energético",
            "Defeito na Instalação", "Sistema Resfriado", "Dano Interno"
        ]
        
        self.acoes = [
            "Ligar", "Recarregar", "Chamar Mecânico", "Verificar", "Substituir Peça",
            "Acelerar", "Trocar Bateria", "Desligar e Resfriar"
        ]
        self.indice_acao = {acao: idx for idx, acao in enumerate(self.acoes)}

        self.transicoes = {
            0: {0: [(1, 0.7), (2, 0.2), (3, 0.1)]},
            1: {3: [(4, 0.9), (5, 0.1)], 5: [(8, 0.3), (9, 0.7)]},
            2: {1: [(6, 0.6), (7, 0.4)], 0: [(10, 0.3), (11, 0.7)]},
            3: {2: [(12, 0.5), (13, 0.5)], 4: [(14, 0.4), (15, 0.6)]},
            4: {0: [(16, 1.0)]},
            5: {1: [(16, 1.0)]},
            6: {0: [(16, 1.0)]},
            7: {0: [(16, 1.0)]},
            8: {0: [(16, 1.0)]},
            9: {0: [(16, 1.0)]},
            10: {0: [(16, 1.0)]},
            11: {0: [(16, 1.0)]},
            12: {0: [(16, 1.0)]},
            13: {0: [(16, 1.0)]},
            14: {0: [(16, 1.0)]},
            15: {0: [(16, 1.0)]},
        }

        self.estados_finais = [16]
        self.recompensas = {estado: random.randint(-10, 15) for estado in range(len(self.estados))}
        self.recompensas[16] = 50
        self.reiniciar()
    
    def passo(self, acao):
        if self.estado in self.estados_finais:
            return self.estado, self.recompensas[self.estado], True
        if self.estado not in self.transicoes or acao not in self.transicoes[self.estado]:
            return self.estado, self.recompensas[self.estado], False
        proximos_estados, probabilidades = zip(*self.transicoes[self.estado][acao])
        self.estado = random.choices(proximos_estados, weights=probabilidades)[0]
        return self.estado, self.recompensas[self.estado], self.estado in self.estados_finais
    
    def reiniciar(self):
        self.estado = 0
        return self.estado

class InterfaceCarroSimples:
    def __init__(self, root):
        self.root = root
        self.root.title("🚗 Sistema Automotivo")
        self.root.configure(bg="#FFE4F7")  # Fundo rosa claro

        # Configura o estilo do ttk
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")
        self.estilo.configure("TFrame", background="#FFE4F7")
        self.estilo.configure("TLabel", background="#FFE4F7", foreground="#D81B60", font=("Comic Sans MS", 12))
        self.estilo.configure("TButton", font=("Comic Sans MS", 12), padding=6)

        self.ambiente = CarroMDP()
        self.pontos = 0
        self.historico_pontos = []

        self.criar_widgets()
        self.atualizar_tela()

    def criar_widgets(self):
        frame_principal = ttk.Frame(self.root, padding="20", style="TFrame")
        frame_principal.pack(fill=tk.BOTH, expand=True)

        self.rotulo_pontos = ttk.Label(frame_principal, text=f"Pontos: {self.pontos}", font=("Comic Sans MS", 16, "bold"))
        self.rotulo_pontos.pack(pady=10)

        self.rotulo_estado = ttk.Label(frame_principal, text="")
        self.rotulo_estado.pack(pady=5)

        self.botoes = []
        for i, acao in enumerate(self.ambiente.acoes):
            btn = tk.Button(frame_principal, text=acao, command=lambda a=i: self.executar_acao(a),
                            font=("Comic Sans MS", 12), bg="#F8BBD0", fg="white",
                            activebackground="#D81B60", activeforeground="white",
                            relief=tk.RIDGE, bd=2, padx=10, pady=5)
            btn.pack(fill=tk.X, pady=5)
            self.botoes.append(btn)

        self.figura, self.eixo = plt.subplots(figsize=(5, 3))
        self.eixo.set_facecolor("#FFF0F5")
        self.canvas = FigureCanvasTkAgg(self.figura, frame_principal)
        self.canvas.get_tk_widget().pack(pady=10)

    def executar_acao(self, acao):
        estado, recompensa, terminado = self.ambiente.passo(acao)
        self.pontos += recompensa
        self.historico_pontos.append(self.pontos)
        self.atualizar_tela()
        if terminado:
            messagebox.showinfo("Fim do jogo 🎉", f"Estado final: {self.ambiente.estados[estado]}\nPontos: {self.pontos}")
            self.reiniciar_jogo()

    def atualizar_tela(self):
        self.rotulo_estado.config(text=f"🚗 Estado: {self.ambiente.estados[self.ambiente.estado]}")
        self.rotulo_pontos.config(text=f"💖 Pontos: {self.pontos}")
        self.plotar_aprendizado()

    def plotar_aprendizado(self):
        self.eixo.clear()
        self.eixo.plot(range(len(self.historico_pontos)), self.historico_pontos, marker='o', color="#D81B60", linestyle="--")
        self.eixo.set_facecolor("#FFF0F5")
        self.eixo.set_title("📊 Evolução dos Pontos", fontsize=12, color="#AD1457")
        self.eixo.set_xlabel("Passos", fontsize=10, color="#D81B60")
        self.eixo.set_ylabel("Pontos", fontsize=10, color="#D81B60")
        for spine in self.eixo.spines.values():
            spine.set_color("#D81B60")
        self.canvas.draw()

    def reiniciar_jogo(self):
        self.ambiente.reiniciar()
        self.pontos = 0
        self.historico_pontos.clear()
        self.atualizar_tela()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceCarroSimples(root)
    root.mainloop()