import pygame

class State:
    def __init__(self, game): self.game = game
    def handle_events(self, events): ...
    def update(self): ...
    def draw(self, screen): ...

class Menu(State):
    def __init__(self, game):
        super().__init__(game)
        pvai_button_width = 200
        pvai_button_height = 100
        pvai_button_x = 720 // 2 - pvai_button_width // 2
        pvai_button_y = 720 // 2 - pvai_button_height // 2
        self.pvai_button_rect = pygame.Rect(pvai_button_x, pvai_button_y, pvai_button_width, pvai_button_height)
        self.font = pygame.font.Font(None, 40)
        self.smaller_font = pygame.font.Font(None, 32)
        self.pvai_surface = self.font.render("Player vs AI", True, (0, 0, 0))
        self.pvai_rect = self.pvai_surface.get_rect()
        self.pvai_rect.center = (360, 360)
        self.pvp_button_rect = pygame.Rect(pvai_button_x, pvai_button_y - pvai_button_height - 20, pvai_button_width, pvai_button_height)
        self.pvp_surface = self.smaller_font.render("Player vs Player", True, (0, 0, 0))
        self.pvp_rect = self.pvp_surface.get_rect()
        self.pvp_rect.center = (self.pvp_button_rect.x + self.pvp_button_rect.width // 2, self.pvp_button_rect.y + self.pvp_button_rect.height // 2)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.pvai_button_rect.collidepoint(event.pos):
                self.game.change("pvai")
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.pvp_button_rect.collidepoint(event.pos):
                self.game.change("pvp")
    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (136, 231, 136), self.pvai_button_rect, border_radius=20)
        screen.blit(self.pvai_surface, self.pvai_rect)
        pygame.draw.rect(screen, (136, 231, 136), self.pvp_button_rect, border_radius=20)
        screen.blit(self.pvp_surface, self.pvp_rect)

class PVP(State):
    def __init__(self, game):
        super().__init__(game)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (self.game.screen_width // 3, 0), (self.game.screen_width // 3, self.game.screen_height), width=5)
        pygame.draw.line(screen, (0, 0, 0), (self.game.screen_width // 3 * 2, 0), (self.game.screen_width // 3 * 2, self.game.screen_height), width=5)
        pygame.draw.line(screen, (0, 0, 0), (0, self.game.screen_height // 3), (self.game.screen_width, self.game.screen_height // 3), width=5)
        pygame.draw.line(screen, (0, 0, 0), (0, self.game.screen_height // 3 * 2), (self.game.screen_width, self.game.screen_height // 3 * 2), width=5)

class PVAI(State):
    def __init__(self, game):
        super().__init__(game)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (self.game.screen_width // 3, 0), (self.game.screen_width // 3, self.game.screen_height), width=5)
        pygame.draw.line(screen, (0, 0, 0), (self.game.screen_width // 3 * 2, 0), (self.game.screen_width // 3 * 2, self.game.screen_height), width=5)
        pygame.draw.line(screen, (0, 0, 0), (0, self.game.screen_height // 3), (self.game.screen_width, self.game.screen_height // 3), width=5)
        pygame.draw.line(screen, (0, 0, 0), (0, self.game.screen_height // 3 * 2), (self.game.screen_width, self.game.screen_height // 3 * 2), width=5)