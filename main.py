import pygame
from states import PVP
from states import PVAI
from states import Menu

pygame.init()

class Game:
    def __init__(self):
        self.states = {
            "pvp": PVP(self),
            "pvai": PVAI(self),
            "menu": Menu(self)
        }
        self.state = self.states["menu"]
        self.running = True

        self.screen_width = 720
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tic Tac Toe")

    def change(self, name):
        self.state = self.states[name]

    def quit(self):
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.state.handle_events(pygame.event.get())
            self.state.update()
            self.state.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()