import pygame
from pygame import mixer
import time
import random
import os

class SudokuGame:
    def __init__(self):
        pygame.init()
        mixer.init()

        self.WHITE = (225, 255, 225)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.green = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GREY = (200, 200, 200)
        self.WIDTH = 605
        self.HEIGHT = 660
        self.SQUARE_SIZE = self.WIDTH // 9
        self.FPS = 24
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sudoku by IRAMA ✨")
        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(base_dir, 'assets')
        sounds_dir = os.path.join(base_dir, 'sounds')
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "Minecraft.ttf"), 30)
        self.font_2 = pygame.font.Font(os.path.join(os.path.dirname(__file__),"Minecraft.ttf"), 36)
        self.button_width = 360
        self.button_height = 60
        self.button_width2 = 600
        self.button_height2 = 100
        self.start_time = 0
        self.elapsed_time = 0
        self.score = 0
        self.board = None
        self.solution = None
        self.selected = None
        self.wrong_move = False
        self.difficulty = None
        self.answered_cells = set()

        try:
            self.background = pygame.image.load(os.path.join(assets_dir, 'background.png'))
            self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        except:
            print("Background is not found")

        try:
            self.trophy = pygame.image.load(os.path.join(assets_dir, 'trophy.png'))
            self.trophy = pygame.transform.scale(self.trophy, (500, 500))
        except:
            print("Trophy asset is not found")

        try:
            self.new_game_btn = pygame.image.load(os.path.join(assets_dir, 'new game.png'))
            self.quit_btn = pygame.image.load(os.path.join(assets_dir, 'quit.png'))
            self.easy_btn = pygame.image.load(os.path.join(assets_dir, 'easy.png'))
            self.medium_btn = pygame.image.load(os.path.join(assets_dir, 'medium.png'))
            self.hard_btn = pygame.image.load(os.path.join(assets_dir, 'hard.png'))
            self.play_again_btn = pygame.image.load(os.path.join(assets_dir, 'play again.png'))
            self.back_menu_btn = pygame.image.load(os.path.join(assets_dir, 'back to menu.png'))
            self.new_game_btn = pygame.transform.scale(self.new_game_btn, (self.button_width, self.button_height))
            self.quit_btn = pygame.transform.scale(self.quit_btn, (self.button_width, self.button_height))
            self.easy_btn = pygame.transform.scale(self.easy_btn, (self.button_width, self.button_height))
            self.medium_btn = pygame.transform.scale(self.medium_btn, (self.button_width, self.button_height))
            self.hard_btn = pygame.transform.scale(self.hard_btn, (self.button_width, self.button_height))
            self.play_again_btn = pygame.transform.scale(self.play_again_btn, (self.button_width, self.button_height))
            self.back_menu_btn = pygame.transform.scale(self.back_menu_btn, (300, 60))
        except:
            print("Button assets is not found")

        try:
            self.sudoku_game = pygame.image.load(os.path.join(assets_dir, 'sudoku game.png'))
            self.select_difficulty = pygame.image.load(os.path.join(assets_dir, 'select difficulty.png'))
            self.sudoku_game = pygame.transform.scale(self.sudoku_game, (self.button_width2, self.button_height2))
            self.select_difficulty = pygame.transform.scale(self.select_difficulty, (self.button_width2, self.button_height2))
        except:
            print("Title assets is not found")

        try:
            self.correct_sound = mixer.Sound(os.path.join(sounds_dir, 'correct.wav'))
            self.wrong_sound = mixer.Sound(os.path.join(sounds_dir, 'Wrong.mp3'))
            self.win_sound = mixer.Sound(os.path.join(sounds_dir, 'win.mp3'))
            self.button_sound = mixer.Sound(os.path.join(sounds_dir, 'button click.mp3'))
            self.notification_score = mixer.Sound(os.path.join(sounds_dir, 'notification score.mp3'))
            pygame.mixer.music.load(os.path.join(sounds_dir, 'game sound.mp3'))
            pygame.mixer.music.set_volume(0.3)
        except:
            print("Sounds is not found")

        try:
            pygame.mixer.music.play(-1)
        except:
            print("Music background is not found")

        try:
            self.fairy_cursor = pygame.image.load(os.path.join(assets_dir, 'peri.png'))
            self.fairy_cursor = pygame.transform.scale(self.fairy_cursor, (32, 32))
            self.fairy_cursor_data = pygame.cursors.Cursor((16, 16), self.fairy_cursor)
        except:
            print("Fairy cursor is not found")

        try:
            self.mouse_click_sound = mixer.Sound(os.path.join(sounds_dir, 'button click.mp3'))
        except:
            print("Mouse click sound is not found")

    def draw_background(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.WHITE)

    def format_time(self,seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{int(minutes):02}:{int(seconds):02}"

    def calculate_score(self,input_type):
        global score
        if input_type == 'correct':
            self.score += 10
        elif input_type == 'incorrect':
            self.score = max(0, self.score - 8)
        return self.score

    def draw_grid(self):
        self.draw_background()
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 2
            pygame.draw.line(self.screen, self.BLACK,
                             (i * self.SQUARE_SIZE, 0),
                             (i * self.SQUARE_SIZE, self.WIDTH), line_width)
            pygame.draw.line(self.screen, self.BLACK,
                             (0, i * self.SQUARE_SIZE),
                             (self.WIDTH, i * self.SQUARE_SIZE), line_width)
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    text = self.font_2.render(str(self.board[i][j]), True, self.BLACK)
                    self.screen.blit(text, (j * self.SQUARE_SIZE + 20, i * self.SQUARE_SIZE + 10))

        if self.selected:
            row, col = self.selected
            color = self.RED if self.wrong_move else self.BLUE
            pygame.draw.rect(self.screen, color,
                             (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 4)

        elapsed_seconds = time.time() - self.start_time
        stopwatch_text = self.font.render("Time: " + self.format_time(elapsed_seconds), True, self.BLACK)
        self.screen.blit(stopwatch_text, (10, self.WIDTH + 15))

        self.score_text = self.font.render(f"Score: {self.score}", True, self.BLACK)
        self.screen.blit(self.score_text, (self.WIDTH - 170, self.WIDTH + 15))

        if self.back_menu_btn:
            back_btn_x = (self.WIDTH - 294) // 2
            back_btn_y = self.WIDTH - 2
            back_menu_rect = self.back_menu_btn.get_rect(topleft=(back_btn_x, back_btn_y))
            self.screen.blit(self.back_menu_btn, back_menu_rect)
            return back_menu_rect

    def generate_puzzle(self,level):
        def shuffle_numbers():
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            return numbers
        self.board = [[0 for _ in range(9)] for _ in range(9)]

        numbers = shuffle_numbers()
        for i in range(9):
            self.board[i][i] = numbers[i]
        self.solve_sudoku(self.board)
        self.solution = [row[:] for row in self.board]
        if level == 'easy':
            num_remove = 3
        elif level == 'medium':
            num_remove = 37
        else:
            num_remove = 47

        removed_positions = set()
        while len(removed_positions) < num_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if (row, col) not in removed_positions:
                removed_positions.add((row, col))
                self.board[row][col] = 0
        
        return self.board, self.solution

    def solve_sudoku(self, board):
        def is_valid(pos, num):
            row, col = pos
            if num in board[row]:
                return False
            for i in range(9):
                if board[i][col] == num:
                    return False
            box_x, box_y = (row // 3) * 3, (col // 3) * 3
            for i in range(box_x, box_x + 3):
                for j in range(box_y, box_y + 3):
                    if board[i][j] == num:
                        return False
            return True

        def find_empty():
            for i, row in enumerate(board):
                for j, val in enumerate(row):
                    if val == 0:
                        return (i, j)
            return None

        empty = find_empty()
        if not empty:
            return True
            
        row, col = empty
        for num in range(1, 10):
            if is_valid((row, col), num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
                
        return False

    def draw_button(self, button_image, y_position, text=None):
        if button_image is None:
            color = self.GREY
            button_width, button_height = 300, 50
            button_x = (self.WIDTH - button_width) // 2
            button = pygame.Rect(button_x, y_position, button_width, button_height)
            pygame.draw.rect(self.screen, color, button, border_radius=20)
            if text:
                button_text = self.font.render(text, True, self.BLACK)
                text_rect = button_text.get_rect(center=button.center)
                self.screen.blit(button_text, text_rect)
        else:
            button_x = (self.WIDTH // 4.75)
            button = pygame.Rect(button_x, y_position, self.button_width, self.button_height)
            self.screen.blit(button_image, button)
            return button

    def play_button_sound(self):
        if self.button_sound:
            self.button_sound.play()

    def animate_confetti(self):
        particles = []
        for _ in range(200):
            x = random.randint(0, self.WIDTH)
            y = random.randint(0, self.HEIGHT)
            color = random.choice([self.RED, self.BLUE, self.GREY, self.green])
            size = random.randint(3, 7)
            speed = random.uniform(1, 5)
            particles.append([x, y, size, speed, color])

        for _ in range(380):
            self.screen.blit(self.background, (0, 0))
            for p in particles:
                p[1] += p[3]
                pygame.draw.circle(self.screen, p[4], (p[0], int(p[1])), p[2])
            pygame.display.flip()
            pygame.time.delay(7)
    def main_menu(self):
        self.screen.blit(self.background, (0, 0))
        if self.sudoku_game:
            title_rect = self.sudoku_game.get_rect(center=(self.WIDTH//2, 100))
            self.screen.blit(self.sudoku_game, title_rect)

        start_button = self.draw_button(self.new_game_btn, 250)
        quit_button = self.draw_button(self.quit_btn, 350)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos):
                        if self.button_sound:
                            self.button_sound.play()
                        return 'start'
                    elif quit_button.collidepoint(mouse_pos):
                        if self.button_sound:
                            self.button_sound.play()
                        return pygame.quit()

    def choose_difficulty(self):
        self.screen.blit(self.background, (0, 0))
        if self.select_difficulty:
            title_rect = self.select_difficulty.get_rect(center=(self.WIDTH//2, 100))
            self.screen.blit(self.select_difficulty, title_rect)

        easy_button = self.draw_button(self.easy_btn, 250)
        medium_button = self.draw_button(self.medium_btn, 350)
        hard_button = self.draw_button(self.hard_btn, 450)
        
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if easy_button.collidepoint(mouse_pos):
                        if self.button_sound:
                            self.button_sound.play()
                        return 'easy'
                    if medium_button.collidepoint(mouse_pos):
                        if self.button_sound:
                            self.button_sound.play()
                        return 'medium'
                    if hard_button.collidepoint(mouse_pos):
                        if self.button_sound:
                            self.button_sound.play()
                        return 'hard'

    def is_game_won(self, board, solution):
        return all(board[i][j] == solution[i][j] for i in range(9) for j in range(9))

    def show_win_screen(self):
        pygame.mixer.music.stop()
        if self.win_sound:
            self.win_sound.play()
        self.animate_confetti()
        self.screen.blit(self.background, (0, 0))

        if self.trophy:
            trophy_rect = self.trophy.get_rect(centerx=self.WIDTH // 2, top=40)
            self.screen.blit(self.trophy, trophy_rect)

        texts = [
            ("CONGRATULATIONS, YOU WIN!", 100),
            (f"Final Score: {self.score}", 300),
            (f"Completion Time: {self.format_time(time.time() - self.start_time)}", 350)]
        
        for text, y in texts:
            surface = self.font.render(text, True, self.BLACK)
            rect = surface.get_rect(center=(self.WIDTH//2, y))
            self.screen.blit(surface, rect)

        buttons = {
            'play_again': (self.play_again_btn, self.HEIGHT // 2 + 150),
            'quit': (self.quit_btn, self.HEIGHT // 2 + 230)}
        
        button_rects = {
            name: self.draw_button(img, y_pos)
            for name, (img, y_pos) in buttons.items()}
        
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_rects['play_again'].collidepoint(mouse_pos):
                        self.play_button_sound()
                        try:
                            pygame.mixer.music.play(-1)
                        except:
                            print("Music background is not found")
                        return
                    elif button_rects['quit'].collidepoint(mouse_pos):
                        self.play_button_sound()
                        pygame.quit()
                        exit()

    def run_game(self):
        clock = pygame.time.Clock()
        running = True
        pygame.mouse.set_cursor(self.fairy_cursor_data)

        while running:
            menu_choice = self.main_menu()
            if menu_choice == 'quit':
                pygame.quit()
                return
                
            level = self.choose_difficulty()
            if level is None:
                pygame.quit()
                return

            self.board, self.solution = self.generate_puzzle(level)
            self.start_time = time.time()
            self.score = 0
            self.selected = (0, 0)
            self.wrong_move = False
            self.answered_cells = set()
            game_running = True
            last_score_reduction = time.time()
            score_reduction_interval = 45
            score_reduction_amount = 4

            while game_running:
                clock.tick(self.FPS)
                current_time = time.time()
                if current_time - last_score_reduction >= score_reduction_interval:
                    self.score = max(0, self.score - score_reduction_amount)
                    last_score_reduction = current_time
                    if self.score:
                        self.notification_score.play()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        game_running = False
                        return

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        back_menu_rect = self.draw_grid()

                        if back_menu_rect.collidepoint(pos):
                            if self.button_sound:
                                self.button_sound.play()
                            game_running = False
                            break

                        row, col = pos[1] // self.SQUARE_SIZE, pos[0] // self.SQUARE_SIZE
                        if row < 9 and col < 9:
                            self.selected = (row, col)

                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_LEFT, pygame.K_a] and self.selected[1] > 0:
                            self.selected = (self.selected[0], self.selected[1] - 1)
                        elif event.key in [pygame.K_RIGHT, pygame.K_d] and self.selected[1] < 8:
                            self.selected = (self.selected[0], self.selected[1] + 1)
                        elif event.key in [pygame.K_UP, pygame.K_w] and self.selected[0] > 0:
                            self.selected = (self.selected[0] - 1, self.selected[1])
                        elif event.key in [pygame.K_DOWN, pygame.K_s] and self.selected[0] < 8:
                            self.selected = (self.selected[0] + 1, self.selected[1])

                        if pygame.K_1 <= event.key <= pygame.K_9:
                            num = event.key - pygame.K_0
                        elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                            num = event.key - pygame.K_KP1 + 1
                        else:
                            num = None

                        if self.selected and num:
                            row, col = self.selected
                            if (row, col) not in self.answered_cells and self.board[row][col] == 0:
                                if self.solution[row][col] == num:
                                    self.board[row][col] = num
                                    self.correct_sound.play()
                                    self.wrong_move = False
                                    self.score = self.calculate_score('correct')
                                else:
                                    self.wrong_sound.play()
                                    self.wrong_move = True
                                    self.score = self.calculate_score('incorrect')

                if game_running:
                    back_menu_rect = self.draw_grid()
                    pygame.display.flip()
                
                    if self.is_game_won(self.board, self.solution):
                        self.show_win_screen()
                        game_running = False

    def start(self):
        try:
            self.run_game()
        except Exception as e:
            print(f"Error Occurred: {e}")
        finally:
            pygame.quit()

if __name__ == "__main__":
    game = SudokuGame()
    game.start()