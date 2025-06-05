from tkinter import *
import random
# Codigo original
root = Tk()  # Criando a janela


class Aplicacao:
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_tela()

        self.subrotinas_ativas = {}  # subrotinas ativas
        # self.subrotinas_fila = []  # fila de subrotinas pendentes
        self.subrotinas_concluidas = []  # subrotinas finalizadas
        self.labels_tempo = {}  # labels para exibir tempo restante
        self.fila_subrotinas = []  # fila de subrotinas pendentes

        # self.configurar_subrotinas()
        self.criar_labels_listas()
        self.atualizar_labels()  # Inicia a atualização automática dos Labels

        root.mainloop()

        # configura a tela da janela
    def tela(self):
        # a um titulo para a janela
        self.root.title("Simulador de Overlay e Paginaçao")
        self.root.configure(background="#D2E6F3")  # cor de fundo da janela
        self.root.geometry("1100x600")  # tamanho da janela
        self.root.resizable(True, True)  # faz a janela ser redimensionavel
        self.root.maxsize(width=1920, height=1080)  # tamanho maximo da janela
        self.root.minsize(width=1100, height=600)  # tamanho minimo da janela

    # cria e configura os frames da tela
    def frames_da_tela(self):
        # frame da memoria
        self.frame_memoria = Frame(
            self.root, width=1000, height=100, bg="#D8E7F1", relief="sunken", bd=6)
        self.frame_memoria.place(relx=0.5, y=120, anchor="center")
        # frame dos botoes iniciar e parar
        self.frame_botoes = Frame(self.root, bg="#D2E6F3")
        self.frame_botoes.place(relx=0.5, y=200, anchor="center")
        # frames das ativas
        self.frame_ativas = Frame(
            self.root, bg="#D2E6F3", width=200, height=350, relief="sunken", bd=4)
        self.frame_ativas.place(
            relx=0.5, rely=0.7, anchor="center")  # Frame das Ativas
        self.frame_ativas.pack_propagate(False)
        # frame da fila
        self.frame_fila = Frame(self.root, bg="#D2E6F3",
                                width=200, height=350, relief="sunken", bd=4)
        self.frame_fila.place(relx=0.15, rely=0.7,
                              anchor="center")  # Frame da Fila
        self.frame_fila.pack_propagate(False)
        # frame das concluidas
        self.frame_concluidas = Frame(
            self.root, bg="#D2E6F3", width=200, height=350, relief="sunken", bd=4)
        self.frame_concluidas.place(
            relx=0.85, rely=0.7, anchor="center")  # Frame das Concluídas
        self.frame_concluidas.pack_propagate(False)
    # ajusta os frames de acordo o modo

    def ajustar_tamanho_frames(self, modo):
        if modo == "pagina":
            largura = 200
            altura = 333
        else:  # overlay
            largura = 150
            altura = 352

        self.frame_fila.config(width=largura, height=altura)
        self.frame_ativas.config(width=largura, height=altura)
        self.frame_concluidas.config(width=largura, height=altura)
    # coloca os labels dentro de cada frame

    def criar_labels_listas(self):
        # label lista subrotina ativas
        self.label_ativas_titulo = Label(self.frame_ativas, text="Ativas:", bg="#D2E6F3", font=(
            'Helvetica', 12, 'bold'), anchor="w")
        self.label_ativas_titulo.pack(fill=X, side=TOP)
        self.label_ativas = Label(
            self.frame_ativas, text="Ativas:", bg="#EEE017", font=('Helvetica', 11, 'bold'))
        self.label_ativas.pack(fill=BOTH, expand=True)
        # label lista subrotinas na fila
        self.label_fila_titulo = Label(self.frame_fila, text="Fila:", bg="#D2E6F3", font=(
            'Helvetica', 12, 'bold'), anchor="w")
        self.label_fila_titulo.pack(fill=X, side=TOP)
        self.label_fila = Label(
            self.frame_fila, text="Fila:", bg="#99AAB5", font=('Helvetica', 11, 'bold'))
        self.label_fila.pack(fill=BOTH, expand=True)
        # label lista subrotinas concluidas
        self.label_concluidas_titulo = Label(
            self.frame_concluidas, text="Concluídas:", bg="#D2E6F3", font=('Helvetica', 12, 'bold'), anchor="w")
        self.label_concluidas_titulo.pack(fill=X, side=TOP)
        self.label_concluidas = Label(
            self.frame_concluidas, text="Concluídas:", bg="#41DA83", font=('Helvetica', 11, 'bold'))
        self.label_concluidas.pack(fill=BOTH, expand=True)

    # elementos da tela
    def widgets_tela(self):
        # criando botao overley
        self.botao_overlay = Button(self.frame_botoes, text="Overlay", font=(
            'Helvetica', 14), command=self.overley, width=10, bg="#72DA77", fg="#FFFFFF")
        self.botao_overlay.grid(row=0, column=1, padx=20, pady=5)
        # criando botao paginação
        self.botao_paginacao = Button(self.frame_botoes, text="Paginação", font=(
            'Helvetica', 14), command=self.paginacao, width=10, bg="#72DA77", fg="#FFFFFF")
        self.botao_paginacao.grid(row=0, column=2, padx=20, pady=5)
        # criando botao parar
        self.botao_parar = Button(self.frame_botoes, text="Parar", font=(
            'Helvetica', 14), command=self.parar, width=10, bg="#EB2121", fg="#FFFFFF")
        self.botao_parar.grid(row=0, column=0, padx=20, pady=5)
        # label com titulo memoria
        self.lb_memoria = Label(self.root, text="MEMÓRIA FISICA", bg="#D2E6F3",
                                foreground="#1D0202", font=('Helvetica', 15, 'bold'))
        self.lb_memoria.place(relx=0.5, y=40, anchor="center")

    # funcoes do botao overley
    def overley(self):
        for widget in self.frame_memoria.winfo_children():
            widget.destroy()
        self.resetar_subrotinas()
        self.configurar_subrotinas(modo="subrotina")
        # Remove o label do título se existir
        if hasattr(self, 'label_memoria_virtual'):
            self.label_memoria_virtual.destroy()
        self.ajustar_tamanho_frames("overley")
        self.iniciar_overley()

     # funcoes do botao paginação
    def paginacao(self):
        for widget in self.frame_memoria.winfo_children():
            widget.destroy()
        self.resetar_subrotinas()
        self.configurar_subrotinas(modo="pagina")
        # Cria o label do título acima do frame da fila
        if hasattr(self, 'label_memoria_virtual'):
            self.label_memoria_virtual.destroy()
        self.label_memoria_virtual = Label(
            self.root, text="MEMÓRIA VIRTUAL", bg="#D2E6F3", foreground="#161414", font=('Helvetica', 12, 'bold'))
        self.label_memoria_virtual.place(relx=0.15, rely=0.40, anchor="center")
        self.ajustar_tamanho_frames("pagina")
        self.iniciar_paginacao()

    # funcoes botao parar
    def parar(self):
        for widget in self.frame_memoria.winfo_children():
            # percorre todos os elementos da memoria e limpa todas as subrotinas e rotina principal
            widget.destroy()
        self.resetar_subrotinas()  # reseta as subrotinas
        self.fila_subrotinas.clear()  # limpa a fila também
        self.atualizar_labels()       # força atualização imediata das listas

    # reseta as listas de subrotinas
    def resetar_subrotinas(self):
        self.subrotinas_concluidas.clear()
        self.subrotinas_ativas.clear()
        self.labels_tempo.clear()

    # cria e configura as subrotinas
    def configurar_subrotinas(self, modo="subrotina"):
        if modo == "pagina":
            self.fila_subrotinas = [f"Página {i}" for i in range(15)]
            self.enderecos_virtuais = {
                f"Página {i}": f"{str(i*1024).zfill(5)} - {str((i+1)*1024 - 1).zfill(5)}" for i in range(15)
            }
        else:
            self.fila_subrotinas = [f"Subrotina {i + 1}" for i in range(15)]
            self.enderecos_virtuais = {}
        self.tempo_execucao = {sub: random.randint(
            3000, 7000) for sub in self.fila_subrotinas}
        self.resetar_subrotinas()

    # cria fisicamente a rotina principal do overley e inicia as subrotinas
    def iniciar_overley(self):
        # criando a rotina principal
        self.rotina_principal = Frame(
            self.frame_memoria, bg="#A8DADC", relief=RAISED, bd=0)
        self.rotina_principal.place(relwidth=0.25, relheight=1, relx=0, rely=0)
        label = Label(self.rotina_principal, text="Rotina Principal",
                      font=("Arial", 20), bg="#F8140C")
        label.pack(expand=True, fill=BOTH)

        # Iniciando as subrotinas
        for i in range(5):
            if self.fila_subrotinas:  # verifica se ainda tem subrotinas na fila
                # tira da fila e executa na posicao i da memoria
                self.executar_subrotina_overley(self.fila_subrotinas.pop(0), i)
     # cria fisicamente a rotina da paginacao e inicia as subrotinas

    def iniciar_paginacao(self):
        # Iniciando as subrotinas
        for i in range(5):
            if self.fila_subrotinas:  # verifica se ainda tem subrotinas na fila
                # tira da fila e executa na posicao i da memoria
                self.executar_subrotina_paginacao(
                    self.fila_subrotinas.pop(0), i)
    # cria fisicamente as subrotinas e seus tempos de execucao

    def executar_subrotina_overley(self, subrotina, index):
        cor = random.choice(
            ["#EAF740", "#EAF740", "#EAF740", "#EAF740", "#EAF740", "#EAF740"])
        # cria o frame da subrotina
        frame_subrotina = Frame(
            self.frame_memoria, bg=cor, relief=RAISED, bd=2)
        largura_subrotina = 0.15
        posicoes_alinhadas = [0.25, 0.40, 0.55, 0.70, 0.85]
        frame_subrotina.place(relwidth=largura_subrotina,
                              relheight=1, relx=posicoes_alinhadas[index], rely=0)

        # cria o titulo da subrotina
        label = Label(frame_subrotina, text=subrotina,
                      font=("Arial", 15), bg=cor)
        label.pack(expand=True, fill=BOTH)

        # converte o tempo de ms para s
        tempo_restante = self.tempo_execucao[subrotina] / 1000.0
        tempo_label = Label(
            frame_subrotina, text=f"{tempo_restante:.1f}s", font=("Arial", 15), bg=cor)
        tempo_label.pack()
        self.labels_tempo[subrotina] = tempo_label
        self.subrotinas_ativas[index] = subrotina
        # Adiciona a função de atualização de tempo

        def atualizar_tempo():
            nonlocal tempo_restante
            if tempo_restante > 0:
                tempo_restante -= 0.1
                self.labels_tempo[subrotina].config(
                    text=f"{tempo_restante:.1f}s")
                self.root.after(100, atualizar_tempo)
            else:
                self.finalizar_subrotina_overley(
                    subrotina, index, frame_subrotina)
        self.root.after(100, atualizar_tempo)

    def executar_subrotina_paginacao(self, subrotina, index):
        cor = random.choice(
            ["#EEE017", "#EEE017", "#EEE017", "#EEE017", "#EEE017"])
        num_subrotinas = 5  # 5 sub-rotinas para paginação
        largura_subrotina = 1.00 / num_subrotinas  # Usa quase toda a largura
        posicoes_alinhadas = [
            i * largura_subrotina for i in range(num_subrotinas)]
        frame_subrotina = Frame(
            self.frame_memoria, bg=cor, relief=RAISED, bd=2)
        frame_subrotina.place(relwidth=largura_subrotina,
                              relheight=1, relx=posicoes_alinhadas[index], rely=0)
        label = Label(frame_subrotina, text=subrotina,
                      font=("Arial", 15), bg=cor)
        label.pack(expand=True, fill=BOTH)

        tempo_restante = self.tempo_execucao[subrotina] / 1000.0
        tempo_label = Label(
            frame_subrotina, text=f"{tempo_restante:.1f}s", font=("Arial", 15), bg=cor)
        tempo_label.pack()
        self.labels_tempo[subrotina] = tempo_label
        self.subrotinas_ativas[index] = subrotina

        def atualizar_tempo():
            nonlocal tempo_restante
            if tempo_restante > 0:
                tempo_restante -= 0.1
                self.labels_tempo[subrotina].config(
                    text=f"{tempo_restante:.1f}s")
                self.root.after(100, atualizar_tempo)
            else:
                self.finalizar_subrotina_paginacao(
                    subrotina, index, frame_subrotina)
        self.root.after(100, atualizar_tempo)

    # remove uma subrotina finalizada e substitui por uma nova
    def finalizar_subrotina_overley(self, subrotina, index, frame_subrotina):
        frame_subrotina.destroy()
        del self.subrotinas_ativas[index]
        self.subrotinas_concluidas.append(subrotina)

        if self.fila_subrotinas:
            nova_subrotina = self.fila_subrotinas.pop(0)
            self.executar_subrotina_overley(nova_subrotina, index)
        else:
            if not self.subrotinas_ativas:
                self.root.after(500, self.remover_rotina_principal)

    def remover_rotina_principal(self):
        if hasattr(self, 'rotina_principal') and self.rotina_principal.winfo_exists():
            # Adiciona à lista de concluídas
            self.subrotinas_concluidas.append("Rotina Principal")
            self.rotina_principal.destroy()

    def finalizar_subrotina_paginacao(self, subrotina, index, frame_subrotina):
        frame_subrotina.destroy()
        del self.subrotinas_ativas[index]
        self.subrotinas_concluidas.append(subrotina)
        if self.fila_subrotinas:
            nova_subrotina = self.fila_subrotinas.pop(0)
            self.executar_subrotina_paginacao(nova_subrotina, index)

    # atualiza periodicamente as listas para adicionar as subrotinas em seus devidos lugares
    def atualizar_labels(self):
        def label_com_endereco(nome):
            if hasattr(self, "enderecos_virtuais") and nome in self.enderecos_virtuais:
                endereco = self.enderecos_virtuais[nome]
                ini, fim = endereco.split(' - ')
                ini = ini.zfill(5)
                fim = fim.zfill(5)
                endereco_formatado = f"{ini} - {fim}"
                return f"{endereco_formatado}   {nome}"
            return nome

        # Limpa os labels antigos
        for widget in self.frame_ativas.winfo_children():
            if widget != self.label_ativas_titulo:
                widget.destroy()
        for widget in self.frame_fila.winfo_children():
            if widget != self.label_fila_titulo:
                widget.destroy()
        for widget in self.frame_concluidas.winfo_children():
            if widget != self.label_concluidas_titulo:
                widget.destroy()

        # Cria um label para cada item ATIVO
        for nome in self.subrotinas_ativas.values():
            lbl = Label(self.frame_ativas, text=label_com_endereco(nome), bg="#EEE017", fg="#8A810B", font=(
                'Helvetica', 8, 'bold'), width=26, height=1, bd=1, relief="solid")
            lbl.pack(fill=X, padx=2, pady=1)

        # Cria um label para cada item na FILA
        for nome in self.fila_subrotinas[:10]:
            lbl = Label(self.frame_fila, text=label_com_endereco(nome), bg="#F1332C", fg="#6E0505", font=(
                'Helvetica', 8, 'bold'), width=26, height=1, bd=1, relief="solid")
            lbl.pack(fill=X, padx=2, pady=1)

        # Cria um label para cada item CONCLUÍDO
        for nome in self.subrotinas_concluidas:
            lbl = Label(self.frame_concluidas, text=label_com_endereco(nome), bg="#41DA83", fg="#117211", font=(
                'Helvetica', 8, 'bold'), width=26, height=1, bd=1, relief="solid")
            lbl.pack(fill=X, padx=2, pady=1)

        self.root.after(500, self.atualizar_labels)


Aplicacao()
