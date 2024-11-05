import tkinter as tk
from tkinter import messagebox
import random
import threading
import time

class Jogada:
    opcoes = {1: 'Tesoura', 2: 'Papel', 3: 'Pedra'}
    imagens = {
        'Tesoura': '✌️',
        'Papel': '🤚',
        'Pedra': '✊'
    }

    def __init__(self, valor):
        self.valor = valor
        self.nome = self.opcoes[valor]
        self.imagem = self.imagens[self.nome]

    def comparar(self, outra_jogada):
        if self.valor == outra_jogada.valor:
            return 'Empate'
        elif (self.valor == 1 and outra_jogada.valor == 2) or \
             (self.valor == 2 and outra_jogada.valor == 3) or \
             (self.valor == 3 and outra_jogada.valor == 1):
            return 'Vitória'
        else:
            return 'Derrota'

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.vitorias = 0

class JogadorHumano(Jogador):
    def fazer_jogada(self, valor):
        return Jogada(valor)

class JogadorComputador(Jogador):
    def fazer_jogada(self):
        escolha = random.randint(1, 3)
        return Jogada(escolha)

class JogoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Pedra, Papel e Tesoura")
        self.master.geometry("600x400")
        self.master.config(bg="#222831")

        self.jogador_humano = JogadorHumano("Você")
        self.jogador_computador = JogadorComputador("Computador")
        self.empates = 0

        self.frame_inicial = tk.Frame(self.master, bg="#222831")
        self.frame_inicial.pack(expand=True)

        self.label_titulo = tk.Label(
            self.frame_inicial, text="Pedra, Papel e Tesoura",
            font=("Arial", 24, "bold"), fg="#eeeeee", bg="#222831"
        )
        self.label_titulo.pack(pady=20)

        self.label_instrucao = tk.Label(
            self.frame_inicial, text="Escolha uma opção:",
            font=("Arial", 16), fg="#eeeeee", bg="#222831"
        )
        self.label_instrucao.pack(pady=10)

        self.frame_botoes = tk.Frame(self.frame_inicial, bg="#222831")
        self.frame_botoes.pack()

        self.botao_tesoura = tk.Button(
            self.frame_botoes, text="Tesoura ✌️", font=("Arial", 14),
            command=lambda: self.jogar(1), bg="#00adb5", fg="#eeeeee",
            activebackground="#393e46", activeforeground="#00adb5", width=12
        )
        self.botao_tesoura.grid(row=0, column=0, padx=10, pady=10)

        self.botao_papel = tk.Button(
            self.frame_botoes, text="Papel 🤚", font=("Arial", 14),
            command=lambda: self.jogar(2), bg="#00adb5", fg="#eeeeee",
            activebackground="#393e46", activeforeground="#00adb5", width=12
        )
        self.botao_papel.grid(row=0, column=1, padx=10, pady=10)

        self.botao_pedra = tk.Button(
            self.frame_botoes, text="Pedra ✊", font=("Arial", 14),
            command=lambda: self.jogar(3), bg="#00adb5", fg="#eeeeee",
            activebackground="#393e46", activeforeground="#00adb5", width=12
        )
        self.botao_pedra.grid(row=0, column=2, padx=10, pady=10)

        self.label_placar = tk.Label(
            self.frame_inicial, text="Placar - Você: 0 | Computador: 0 | Empates: 0",
            font=("Arial", 14), fg="#eeeeee", bg="#222831"
        )
        self.label_placar.pack(pady=20)

    def jogar(self, escolha_jogador):
        self.jogada_humano = self.jogador_humano.fazer_jogada(escolha_jogador)
        self.esperando_adversario()

    def esperando_adversario(self):
        self.frame_inicial.pack_forget()
        self.frame_espera = tk.Frame(self.master, bg="#222831")
        self.frame_espera.pack(expand=True)

        self.label_espera = tk.Label(
            self.frame_espera, text="Esperando adversário...",
            font=("Arial", 20), fg="#00adb5", bg="#222831"
        )
        self.label_espera.pack(pady=100)

        # Simular espera de 6 segundos em uma thread separada
        threading.Thread(target=self.processar_jogada).start()

    def processar_jogada(self):
        time.sleep(1)
        self.jogada_computador = self.jogador_computador.fazer_jogada()
        resultado = self.jogada_humano.comparar(self.jogada_computador)

        if resultado == 'Vitória':
            self.jogador_humano.vitorias += 1
            cor_resultado = "#4caf50"  # Verde
        elif resultado == 'Derrota':
            self.jogador_computador.vitorias += 1
            cor_resultado = "#f44336"  # Vermelho
        else:
            self.empates += 1
            cor_resultado = "#ffc107"  # Amarelo

        self.mostrar_resultado(resultado, cor_resultado)

    def mostrar_resultado(self, resultado, cor_resultado):
        self.frame_espera.pack_forget()
        self.frame_resultado = tk.Frame(self.master, bg="#222831")
        self.frame_resultado.pack(expand=True)

        self.label_resultado = tk.Label(
            self.frame_resultado, text=f"{resultado}!",
            font=("Arial", 30, "bold"), fg=cor_resultado, bg="#222831"
        )
        self.label_resultado.pack(pady=20)

        self.label_jogada = tk.Label(
            self.frame_resultado,
            text=f"Você: {self.jogada_humano.nome} {self.jogada_humano.imagem}\n"
                 f"Computador: {self.jogada_computador.nome} {self.jogada_computador.imagem}",
            font=("Arial", 18), fg="#eeeeee", bg="#222831"
        )
        self.label_jogada.pack(pady=10)

        self.label_placar = tk.Label(
            self.frame_resultado,
            text=f"Placar - Você: {self.jogador_humano.vitorias} | "
                 f"Computador: {self.jogador_computador.vitorias} | Empates: {self.empates}",
            font=("Arial", 16), fg="#eeeeee", bg="#222831"
        )
        self.label_placar.pack(pady=20)

        if self.jogador_humano.vitorias == 3 or self.jogador_computador.vitorias == 3:
            self.botao_reiniciar = tk.Button(
                self.frame_resultado, text="Jogar Novamente", font=("Arial", 14),
                command=self.reiniciar_jogo, bg="#00adb5", fg="#eeeeee",
                activebackground="#393e46", activeforeground="#00adb5", width=15
            )
            self.botao_reiniciar.pack(pady=10)
        else:
            self.botao_continuar = tk.Button(
                self.frame_resultado, text="Continuar", font=("Arial", 14),
                command=self.continuar_jogo, bg="#00adb5", fg="#eeeeee",
                activebackground="#393e46", activeforeground="#00adb5", width=15
            )
            self.botao_continuar.pack(pady=10)

    def continuar_jogo(self):
        self.frame_resultado.pack_forget()
        self.frame_inicial.pack(expand=True)
        self.atualizar_placar()

    def reiniciar_jogo(self):
        self.jogador_humano.vitorias = 0
        self.jogador_computador.vitorias = 0
        self.empates = 0
        self.frame_resultado.pack_forget()
        self.frame_inicial.pack(expand=True)
        self.atualizar_placar()

    def atualizar_placar(self):
        self.label_placar.config(
            text=f"Placar - Você: {self.jogador_humano.vitorias} | "
                 f"Computador: {self.jogador_computador.vitorias} | Empates: {self.empates}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    jogo_gui = JogoGUI(root)
    root.mainloop()
