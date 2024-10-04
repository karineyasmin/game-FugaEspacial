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

    def __init__(self):

        # Atribui imagem pára o background
        background_fig = pygame.image.load("Images/background.png")
        background_fig.convert()
        self.image = background_fig

    def update(self, dt):
        pass

    # Imagem do backeground na tela
    def draw(self, screen):
        screen.blit(self.image, (0, 0))


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

        # while self.run

    # loop()


# Inicia o jogo: Cria o objeto game e chama o loop básico
game = Game("resolution", "fullscreen")
game.loop()
