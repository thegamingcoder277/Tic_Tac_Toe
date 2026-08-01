import random
import pygame

WIN_LINES = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]

AI_DELAY_MS = 500

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
                self.game.states["pvai"].reset()
                self.game.change("pvai")
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.pvp_button_rect.collidepoint(event.pos):
                self.game.states["pvp"].reset()
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
        self.turn = 'X'
        self.board = [['b','b','b'],
                      ['b','b','b'],
                      ['b','b','b']]
        self.game_over = False
        self.winner = None
        self.winning_cells = None
        button_y = self.game.screen_height // 2 + 110
        gap = 20
        total_width = 200 * 2 + gap
        button_left = (self.game.screen_width - total_width) // 2
        self.main_menu_button_rect = pygame.Rect(button_left, button_y, 200, 60)
        self.play_again_button_rect = pygame.Rect(button_left + 200 + gap, button_y, 200, 60)
        self.button_font = pygame.font.Font(None, 36)
        self.main_menu_surface = self.button_font.render("Main Menu", True, (0, 0, 0))
        self.main_menu_rect = self.main_menu_surface.get_rect(center=self.main_menu_button_rect.center)
        self.play_again_surface = self.button_font.render("Play Again", True, (0, 0, 0))
        self.play_again_rect = self.play_again_surface.get_rect(center=self.play_again_button_rect.center)
    def reset(self):
        self.turn = 'X'
        self.board = [['b','b','b'],
                      ['b','b','b'],
                      ['b','b','b']]
        self.game_over = False
        self.winner = None
        self.winning_cells = None
    def check_winner(self):
        for line in WIN_LINES:
            marks = {self.board[r][c] for r, c in line}
            if len(marks) == 1 and 'b' not in marks:
                return line
        return None
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.game_over and self.main_menu_button_rect.collidepoint(event.pos):
                self.game.change('menu')
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.game_over and self.play_again_button_rect.collidepoint(event.pos):
                self.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                col = event.pos[0] * 3 // self.game.screen_width
                row = event.pos[1] * 3 // self.game.screen_height
                if self.board[row][col] == 'b':
                    self.board[row][col] = self.turn.lower()
                    winning_line = self.check_winner()
                    if winning_line:
                        self.winner = self.board[winning_line[0][0]][winning_line[0][1]].upper()
                        self.winning_cells = winning_line
                        self.game_over = True
                    elif all(mark != 'b' for row in self.board for mark in row):
                        self.game_over = True
                    else:
                        self.turn = 'O' if self.turn == 'X' else 'X'
    def result_text(self):
        return f"{self.winner} wins!" if self.winner else "It's a draw!"
    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (self.game.screen_width // 3, 0), (self.game.screen_width // 3, self.game.screen_height), width=5)
        pygame.draw.line(screen, (0, 0, 0), (self.game.screen_width // 3 * 2, 0), (self.game.screen_width // 3 * 2, self.game.screen_height), width=5)
        pygame.draw.line(screen, (0, 0, 0), (0, self.game.screen_height // 3), (self.game.screen_width, self.game.screen_height // 3), width=5)
        pygame.draw.line(screen, (0, 0, 0), (0, self.game.screen_height // 3 * 2), (self.game.screen_width, self.game.screen_height // 3 * 2), width=5)

        cell_w = self.game.screen_width // 3
        cell_h = self.game.screen_height // 3
        margin = 30
        for i, row in enumerate(self.board):
            for j, mark in enumerate(row):
                if mark == 'b':
                    continue
                x = j * cell_w
                y = i * cell_h
                if mark == 'x':
                    pygame.draw.line(screen, (0, 0, 0), (x + margin, y + margin), (x + cell_w - margin, y + cell_h - margin), 10)
                    pygame.draw.line(screen, (0, 0, 0), (x + margin, y + cell_h - margin), (x + cell_w - margin, y + margin), 10)
                elif mark == 'o':
                    pygame.draw.circle(screen, (0, 0, 0), (x + cell_w // 2, y + cell_h // 2), cell_w // 2 - margin, width=10)

        if self.game_over:
            font = pygame.font.Font(None, 60)
            text = self.result_text()
            surface = font.render(text, True, (200, 0, 0))
            rect = surface.get_rect(center=(self.game.screen_width // 2, self.game.screen_height // 2))
            pygame.draw.rect(screen, (255, 255, 255), rect.inflate(40, 20), border_radius=10)
            screen.blit(surface, rect)

        if self.winner:
            centers = [
                (c * cell_w + cell_w // 2, r * cell_h + cell_h // 2)
                for r, c in self.winning_cells
            ]
            pygame.draw.line(screen, (0, 200, 0), centers[0], centers[2], width=12)

        if self.game_over:
            pygame.draw.rect(screen, (136, 180, 231), self.main_menu_button_rect, border_radius=15)
            screen.blit(self.main_menu_surface, self.main_menu_rect)
            pygame.draw.rect(screen, (136, 231, 136), self.play_again_button_rect, border_radius=15)
            screen.blit(self.play_again_surface, self.play_again_rect)

class PVAI(PVP):
    def __init__(self, game):
        super().__init__(game)
        self.ai_pending = False
    def reset(self):
        super().reset()
        self.ai_pending = False
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.game_over and self.main_menu_button_rect.collidepoint(event.pos):
                self.game.change('menu')
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.game_over and self.play_again_button_rect.collidepoint(event.pos):
                self.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over and self.turn == 'X':
                col = event.pos[0] * 3 // self.game.screen_width
                row = event.pos[1] * 3 // self.game.screen_height
                if self.board[row][col] == 'b':
                    self.board[row][col] = 'x'
                    winning_line = self.check_winner()
                    if winning_line:
                        self.winner = 'X'
                        self.winning_cells = winning_line
                        self.game_over = True
                    elif all(mark != 'b' for row in self.board for mark in row):
                        self.game_over = True
                    else:
                        self.turn = 'O'
                        self.ai_pending = True
                        self.ai_move_time = pygame.time.get_ticks() + AI_DELAY_MS
    def update(self):
        if self.ai_pending and not self.game_over and pygame.time.get_ticks() >= self.ai_move_time:
            self.ai_pending = False
            self.ai_move()
    def ai_move(self):
        move = self.find_move('o') or self.find_move('x')
        if move is None and self.board[1][1] == 'b':
            move = (1, 1)
        if move is None:
            empty = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == 'b']
            move = random.choice(empty)
        r, c = move
        self.board[r][c] = 'o'
        winning_line = self.check_winner()
        if winning_line:
            self.winner = 'O'
            self.winning_cells = winning_line
            self.game_over = True
        elif all(mark != 'b' for row in self.board for mark in row):
            self.game_over = True
        else:
            self.turn = 'X'
    def find_move(self, mark):
        for line in WIN_LINES:
            cells = [self.board[r][c] for r, c in line]
            if cells.count(mark) == 2 and cells.count('b') == 1:
                for r, c in line:
                    if self.board[r][c] == 'b':
                        return (r, c)
        return None
    def result_text(self):
        if self.winner == 'X':
            return "You win!"
        if self.winner == 'O':
            return "AI wins!"
        return "It's a draw!"