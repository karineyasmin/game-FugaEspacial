"""
Jogo: Fuga Espacial
Descrição: Um grupo de diplomatas escapam de uma fortaleza estelar a bordo de uma nave danificada.
 A nave precisa se desviar das ameaças e spbreviver até atingir a zona de segurança diplomática.
"""

import sys
import pygame
import time
import random
import os


class Background:
    """Representa o plano de fundo do jogo, incluindo a imagem de fundo e as margens esquerda e direita."""

    image = None
    margin_left = None
    margin_right = None

    def __init__(self):
        """Inicializa a classe Background, carregando e escalando a imagem de fundo e as margens."""
        # Carrega a imagem de fundo e a escala para o tamanho desejado
        background_fig = pygame.image.load("Images/background.png")
        background_fig.convert()
        background_fig = pygame.transform.scale(background_fig, (800, 602))
        self.image = background_fig  # Atribui a imagem para o fundo

        # Carrega e escala a margem esquerda
        margin_left_fig = pygame.image.load("Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60, 602))
        self.margin_left = margin_left_fig

        # Carrega e escala a margem direita
        margin_right_fig = pygame.image.load("Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_right_fig, (60, 602))
        self.margin_right = margin_right_fig

    def move(self, screen, scr_height, movL_x, movL_y, movR_x, movR_y):
        """
        Move o fundo e as margens de acordo com as posições fornecidas.

        Args:
            screen (Surface): A superfície onde o plano de fundo será desenhado.
            scr_height (int): A altura da tela, utilizada para o cálculo de movimentação.
            movL_x (int): A posição x da margem esquerda.
            movL_y (int): A posição y da margem esquerda.
            movR_x (int): A posição x da margem direita.
            movR_y (int): A posição y da margem direita.
        """
        for i in range(0, 2):
            # Desenha a imagem de fundo e as margens em posições y alteradas
            screen.blit(self.image, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_left, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_right, (movR_x, movR_y - i * scr_height))

    def draw(self, screen):
        """Desenha a imagem de fundo e as margens na tela."""
        screen.blit(self.image, (0, 0))  # Desenha a imagem do fundo na posição (0, 0)
        screen.blit(
            self.margin_left, (0, 0)
        )  # Desenha a margem esquerda na posição (0, 0)
        screen.blit(
            self.margin_right, (740, 0)
        )  # Desenha a margem direita na posição (740, 0)

    def draw_freedom(self, screen):
        """Desenha apenas a imagem de fundo na tela."""
        screen.blit(self.image, (0, 0))  # Desenha a imagem do fundo na posição (0, 0)


class Player:
    """Representa o jogador no jogo, incluindo sua posição e imagem."""

    image = None
    x = None
    y = None

    def __init__(self, x, y):
        """
        Inicializa a classe Player, carregando a imagem do jogador e definindo sua posição inicial.

        Args:
            x (int): A coordenada x inicial do jogador.
            y (int): A coordenada y inicial do jogador.
        """
        player_fig = pygame.image.load("Images/player.png")
        player_fig.convert()
        player_fig = pygame.transform.scale(player_fig, (90, 90))
        self.image = player_fig
        self.x = x
        self.y = y

    def move(self, mudar_x):
        """
        Move o jogador alterando sua coordenada x.

        Args:
            mudar_x (int): O valor a ser adicionado à coordenada x do jogador.
        """
        self.x += mudar_x  # Altera a coordenada x do jogador

    def draw(self, screen, x, y):
        """
        Desenha a imagem do jogador na tela.

        Args:
            screen (Surface): A superfície onde o jogador será desenhado.
            x (int): A coordenada x onde a imagem do jogador será desenhada.
            y (int): A coordenada y onde a imagem do jogador será desenhada.
        """
        screen.blit(self.image, (x, y))


class Hazard:
    """Representa as ameaças ao jogador no jogo."""

    image = None
    x = None
    y = None

    def __init__(self, img, x, y):
        """
        Inicializa a classe Hazard, carregando a imagem da ameaça e definindo sua posição inicial.

        Args:
            img (str): O caminho para a imagem da ameaça.
            x (int): A coordenada x inicial da ameaça.
            y (int): A coordenada y inicial da ameaça.
        """
        hazard_fig = pygame.image.load(img)
        hazard_fig.convert()
        hazard_fig = pygame.transform.scale(hazard_fig, (130, 130))
        self.image = hazard_fig
        self.x = x
        self.y = y

    def move(self, screen, velocidade_hazard):
        """
        Move a ameaça na direção y e desenha na tela.

        Args:
            screen (Surface): A superfície onde a ameaça será desenhada.
            velocidade_hazard (int): A velocidade com que a ameaça se move.
        """
        self.y += velocidade_hazard / 4  # Movimenta a ameaça
        self.draw(screen, self.x, self.y)  # Desenha a ameaça na nova posição
        self.y += velocidade_hazard  # Aplica velocidade total na coordenada y

    def draw(self, screen, x, y):
        """
        Desenha a imagem da ameaça na tela.

        Args:
            screen (Surface): A superfície onde a ameaça será desenhada.
            x (int): A coordenada x onde a imagem da ameaça será desenhada.
            y (int): A coordenada y onde a imagem da ameaça será desenhada.
        """
        screen.blit(self.image, (x, y))


class Soundtrack:
    """Gerencia a reprodução de trilhas sonoras e efeitos sonoros no jogo."""

    soundtrack = None
    sound = None

    def __init__(self, soundtrack):
        """
        Inicializa a classe Soundtrack, verificando se a trilha sonora existe.

        Args:
            soundtrack (str): O caminho para o arquivo da trilha sonora.
        """
        if os.path.isfile(soundtrack):
            self.soundtrack = soundtrack
        else:
            print(soundtrack + " not found .. ignoring", file=sys.stderr)

    def play(self):
        """Reproduz a trilha sonora em loop indefinidamente."""
        pygame.mixer.music.load(self.soundtrack)
        pygame.mixer.music.set_volume(0.5)  # Define o volume da música
        pygame.mixer.music.play(loops=-1)  # Reproduz a música em loop indefinido

    def set(self, soundtrack):
        """
        Define uma nova trilha sonora se o arquivo existir.

        Args:
            soundtrack (str): O caminho para o novo arquivo da trilha sonora.
        """
        if os.path.isfile(soundtrack):
            self.soundtrack = soundtrack
        else:
            print(soundtrack + " not found ... ignoring", file=sys.stderr)

    def play_sound(self, sound):
        """
        Reproduz um efeito sonoro se o arquivo existir.

        Args:
            sound (str): O caminho para o arquivo do efeito sonoro.
        """
        if os.path.isfile(sound):
            self.sound = sound
            pygame.mixer.music.load(self.sound)
            pygame.mixer.music.set_volume(0.5)  # Define o volume do efeito sonoro
            pygame.mixer.music.play()  # Reproduz o efeito sonoro
        else:
            print(sound + " file not found ... ignoring", file=sys.stderr)


class Game:
    """Representa o jogo, incluindo a tela, o jogador, as ameaças e a lógica do jogo."""

    screen = None
    screen_size = None
    width = 800
    height = 600
    run = True
    background = None
    player = None
    hazard = []
    mudar_x = 0.0

    def __init__(self, size, fullscreen):
        """
        Inicializa o Pygame, define a resolução da tela, a legenda da janela e oculta o cursor do mouse.

        Args:
            size (str): A resolução da tela (não utilizado neste contexto).
            fullscreen (str): O modo de tela cheia (não utilizado neste contexto).
        """
        self.soundtrack = None
        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )  # Tamanho da tela
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible(0)  # Oculta o cursor do mouse

        # Define a legenda da janela do jogo
        pygame.display.set_caption("Fuga Espacial")

    def handle_events(self):
        """Trata eventos de entrada e atualiza o estado do jogo."""
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
            ):  # Para de executar o jogo ao clicar no 'x' da janela
                self.run = False

            if event.type == pygame.KEYDOWN:  # Se clicar em qualquer tecla
                if event.key == pygame.K_LEFT:  # Seta da esquerda
                    self.mudar_x = -7  # Move para a esquerda
                if event.key == pygame.K_RIGHT:  # Seta da direita
                    self.mudar_x = 7  # Move para a direita

            if event.type == pygame.KEYUP:  # Se soltar qualquer tecla
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.mudar_x = 0  # Para o movimento

    def write_message(self, message, R, G, B, x, y):
        """
        Escreve uma mensagem na tela.

        Args:
            message (str): A mensagem a ser exibida.
            R (int): Componente vermelho da cor do texto.
            G (int): Componente verde da cor do texto.
            B (int): Componente azul da cor do texto.
            x (int): Coordenada x onde a mensagem será desenhada.
            y (int): Coordenada y onde a mensagem será desenhada.
        """
        my_font1 = pygame.font.Font("Fonts/Fonte4.ttf", 100)  # Define a fonte
        render_text = my_font1.render(message, False, (R, G, B))  # Renderiza a mensagem
        self.screen.blit(render_text, (x, y))  # Desenha a mensagem na tela

    def elements_draw(self):
        """Desenha os elementos do jogo na tela."""
        self.background.draw(self.screen)  # Desenha o fundo

    def score_card(self, screen, h_passou, score):
        """
        Exibe a quantidade de hazards que passaram e a pontuação.

        Args:
            screen (Surface): A superfície onde o placar será desenhado.
            h_passou (int): A quantidade de hazards que passaram.
            score (int): A pontuação atual do jogador.
        """
        font = pygame.font.SysFont(None, 35)
        passou = font.render(
            "Passou: " + str(h_passou), True, (255, 255, 128)
        )  # Texto de hazards
        score_text = font.render(
            "Score: " + str(score), True, (253, 231, 32)
        )  # Texto de pontuação
        screen.blit(passou, (0, 50))  # Desenha o texto de hazards
        screen.blit(score_text, (0, 100))  # Desenha o texto de pontuação

    def draw_explosion(self, screen, x, y):
        """
        Desenha a imagem da explosão na tela.

        Args:
            screen (Surface): A superfície onde a explosão será desenhada.
            x (int): Coordenada x onde a explosão será desenhada.
            y (int): Coordenada y onde a explosão será desenhada.
        """
        explosion_fig = pygame.image.load("Images/explosion.png")
        explosion_fig.convert()
        explosion_fig = pygame.transform.scale(
            explosion_fig, (150, 150)
        )  # Escala a explosão
        screen.blit(explosion_fig, (x, y))  # Desenha a explosão


    def loop(self):
        """Inicia o loop principal do jogo, onde a lógica do jogo é atualizada e os elementos são desenhados na tela."""
        score = 0  # Pontuação inicial do jogador
        h_passou = 0  # Contador de hazards que passaram

        # Variáveis para o movimento do plano de fundo
        velocidade_background = 10  # Velocidade do fundo
        velocidade_hazard = 10  # Velocidade dos hazards

        # Movimento da margem esquerda e direita
        movL_x = 0
        movL_y = 0
        movR_x = 740
        movR_y = 0

        # Criar plano de fundo
        self.background = Background()

        # Criar e reproduzir a trilha sonora do jogo
        self.soundtrack = Soundtrack("Sounds/song.wav")
        self.soundtrack.play()

        # Variáveis de localização dos hazards
        hzrd = 0  # Índice do hazard atual
        h_x = random.randrange(125, 660)  # Posição horizontal aleatória do hazard
        h_y = -500  # Posição vertical inicial do hazard

        # Criar os hazards
        self.hazard.append(Hazard("Images/satelite.png", h_x, h_y))
        self.hazard.append(Hazard("Images/nave.png", h_x, h_y))
        self.hazard.append(Hazard("Images/cometaVermelho.png", h_x, h_y))
        self.hazard.append(Hazard("Images/meteoros.png", h_x, h_y))
        self.hazard.append(Hazard("Images/buracoNegro.png", h_x, h_y))

        # Posição inicial do jogador
        x = (self.width - 56) / 2
        y = self.height - 125

        # Criar o jogador
        self.player = Player(x, y)

        # Inicializa o relógio para controle de FPS
        clock = pygame.time.Clock()
        dt = 29  # Delay entre os frames

        # Início do loop principal do jogo
        while self.run:
            clock.tick(1000 / dt)  # Limita a taxa de atualização

            self.handle_events()  # Trata eventos de entrada
            self.elements_draw()  # Desenha os elementos do jogo

            # Adiciona movimento ao fundo
            self.background.move(self.screen, self.height, movL_x, movL_y, movR_x, movR_y)
            movL_y += velocidade_background  # Atualiza a posição da margem esquerda
            movR_y += velocidade_background  # Atualiza a posição da margem direita

            # Se a imagem ultrapassar a extremidade da tela, move de volta
            if movL_y > 600 and movR_y > 600:
                movL_y -= 600
                movR_y -= 600
            # O fundo é atualizado continuamente, reiniciando a posição das margens conforme necessário

            # Movimentação do jogador
            self.player.move(self.mudar_x)  # Altera a coordenada x do jogador
            self.player.draw(self.screen, self.player.x, self.player.y)  # Desenha o jogador

            # Mostrar placar
            self.score_card(self.screen, h_passou, score)

            # Restrições do movimento do jogador
            if self.player.x > 760 - 92 or self.player.x < 40 + 5:  # Colisão com as margens
                self.soundtrack.play_sound("Sounds/jump2.wav")  # Toca som de colisão
                self.write_message(
                    "VOCÊ BATEU :(", 255, 255, 255, 80, 200
                )  # Mensagem de batida
                pygame.display.update()  # Atualiza a tela
                time.sleep(3)  # Pausa antes de reiniciar o loop
                self.loop()  # Reinicia o loop
                self.run = False  # Encerra o jogo

            # Movimenta o hazard e o desenha
            self.hazard[hzrd].move(self.screen, velocidade_hazard)

            # Atualiza a posição do hazard se ele sair da tela
            if self.hazard[hzrd].y > self.height:
                self.hazard[hzrd].y = 0 - self.hazard[hzrd].image.get_height()
                self.hazard[hzrd].x = random.randrange(
                    125, 650 - self.hazard[hzrd].image.get_height()
                )
                hzrd = random.randint(0, 4)  # Seleciona um hazard aleatório
                h_passou += 1  # Atualiza a quantidade de hazards que passaram
                score = h_passou * 10  # Atualiza a pontuação

            # Aumenta a velocidade dos hazards se a pontuação atingir 60
            if score == 60:
                velocidade_hazard += 0.1

            # Verifica colisão entre o jogador e o hazard
            player_rect = self.player.image.get_rect()
            player_rect.topleft = (self.player.x, self.player.y)
            hazard_rect = self.hazard[hzrd].image.get_rect()
            hazard_rect.topleft = (self.hazard[hzrd].x, self.hazard[hzrd].y)

            if hazard_rect.colliderect(player_rect):  # Colisão detectada
                self.soundtrack.play_sound("Sounds/crash.wav")  # Toca som da colisão
                self.draw_explosion(
                    self.screen,
                    self.player.x - (self.player.image.get_width() / 2),
                    self.player.y - (self.player.image.get_height() / 2),
                )  # Desenha a explosão
                self.write_message(
                    "GAME OVER :(", 255, 0, 0, 80, 200
                )  # Mensagem de Game Over
                pygame.display.update()  # Atualiza a tela
                time.sleep(3)  # Pausa antes de encerrar o jogo
                self.run = False  # Encerra o jogo

            # Vitória do jogador
            if score == 100:  # Se atingir score de 100, vence o jogo
                self.soundtrack.play_sound("Sounds/racetheme.mp3")  # Música da vitória
                self.background.draw_freedom(self.screen)  # Desenha a área de vitória
                self.write_message(
                    "100 PONTOS", 255, 117, 24, 90, 100
                )  # Mensagem de pontuação
                self.write_message(
                    "VOCÊ VENCEU!", 255, 117, 24, 2, 300
                )  # Mensagem de vitória
                pygame.display.update()  # Atualiza a tela
                time.sleep(10)  # Pausa antes de encerrar o jogo
                self.run = False  # Encerra o jogo

            # Atualiza a tela após o movimento
            pygame.display.update()
            clock.tick(2000)  # Controla a taxa de quadros


game = Game("resolution", "fullscreen")  # instanciar objeto jogo
game.loop()  # iniciar jogo
