"""
Jogo: Fuga Espacial
Descrição: Um grupo de diplomatas escapam de uma fortaleza estelar a bordo de uma nave danificada.
A nave precisa se desviar das ameaças e sobreviver até atingir a zona de segurança diplomática.
"""

import pygame


class Background:
    """
    Esta classe define o Plano de Fundo do jogo
    """

    image = None
    margin_left = None
    margin_right = None

    def __init__(self):

        # Atribui imagem pára o background
        background_fig = pygame.image.load("Images/background.png")
        background_fig.convert()
        background_fig = pygame.transform.scale(background_fig, (800, 602))
        self.image = background_fig

        margin_left_fig = pygame.image.load("Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60, 602))
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_right_fig, (60, 602))
        self.margin_right = margin_right_fig

    def update(self, dt):
        pass

    # Imagem do backeground na tela
    def draw(self, screen):
        screen.blit(self.image, (0, 0))

        # 60 depois da primeira margem
        screen.blit(self.margin_left, (0, 0))

        # 60 antes da segunda margem
        screen.blit(self.margin_right, (740, 0))

    # Define posições do plano de fundo para criar o movimento
    def move(self, screen, scr_height, movL_x, movL_y, movR_x, movR_y):
        for i in range(0, 2):
            screen.blit(self.image, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_left, (movL_x, movR_y - i * scr_height))
            screen.blit(self.margin_right, (movR_x, movR_y - i * scr_height))


class Game:
    screen = None
    screen_size = None
    width = 800
    height = 680
    run = True
    background = None

    def __init__(self, size, fullscreen):
        """
        Função que inicializa o pygame, define a resolução da tela,         caption e desabilita o mouse.
        """

        pygame.init()

        # tamanho da tela
        self.screen = pygame.display.set_mode((self.width, self.height))

        # define o tamanho da tela do jogo
        self.screen_size = self.screen.get_size()

        # desabilitar o mouse
        pygame.mouse.set_visible(0)

        # definir caption da janela do jogo
        pygame.display.set_caption("Fuga Espacial")

    def handle_events(self):
        """
        Trata o evento e toma a ação necessária.
        """

        # Trata a saída do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    # handle_events()

    def elements_update(self, dt):
        # Atualiza elementos
        self.background.update(dt)

    def elements_draw(self):
        # Desenhar elementos
        self.background.draw(self.screen)

    def loop(self):
        """
        Laço principal
        """

        # variaáveis para moviemnto de Plano de Fundo/Background
        velocidade_background = 10

        # movimento da margem esquerda
        movL_x = 0
        movL_y = 0

        # movimento da margem direita
        movR_x = 740
        movR_y = 0

        # Criar o plano de fundo
        self.background = Background()

        # Inicializa o relogio e o dt que vai limitar o valor de FPS (frames por segundo) do jogo
        clock = pygame.time.Clock()
        dt = 16

        # Inicio do loop principal do programa
        while self.run:
            clock.tick(1000 / dt)

            # Handle Input events
            self.handle_events()

            # Atualiza o background buffer
            self.elements_draw()

            # Atualiza a tela
            pygame.display.update()
            clock.tick(2000)

            # adiciona movimento ao background
            self.background.move(
                self.screen, self.height, movL_x, movL_y, movR_x, movR_y
            )
            movL_y = movL_y + velocidade_background
            movR_y = movR_y + velocidade_background

            # se a imagem ultrapassar a extremidade da tela, move de volta
            if movL_y > 600 and movR_y > 600:
                movL_y -= 600
                movR_y -= 600

        # while self.run

    # loop()


# Inicia o jogo: Cria o objeto game e chama o loop básico
game = Game("resolution", "fullscreen")
game.loop()
