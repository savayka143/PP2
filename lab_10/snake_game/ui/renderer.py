import pygame

class Renderer:
    def __init__(self, screen, config, font):
        self.screen = screen
        self.config = config
        self.font = font

    def render(self, snake, fruit, score, paused):
        self.screen.fill(self.config.BG_COLOR)

        cs, cn = self.config.CELL_SIZE, self.config.CELL_NUMBER
        for row in range(cn):
            for col in range(cn):
                if (row + col) % 2 == 0:
                    rect = pygame.Rect(col * cs, row * cs, cs, cs)
                    pygame.draw.rect(self.screen, self.config.GRASS_COLOR, rect)

        f_rect = pygame.Rect(
            int(fruit.pos.x * cs),
            int(fruit.pos.y * cs),
            cs, cs
        )
        pygame.draw.rect(self.screen, self.config.FRUIT_COLOR, f_rect)

        for block in snake.body:
            b_rect = pygame.Rect(
                int(block.x * cs),
                int(block.y * cs),
                cs, cs
            )
            pygame.draw.rect(self.screen, self.config.SNAKE_COLOR, b_rect)

        score_surf = self.font.render(f"Score: {score}", True, self.config.SCORE_COLOR)
        self.screen.blit(score_surf, (10, 10))

        if paused:
            pause_surf = self.font.render("PAUSED", True, self.config.PAUSE_COLOR)
            rect = pause_surf.get_rect(center=(self.config.WIDTH // 2, self.config.HEIGHT // 2))
            self.screen.blit(pause_surf, rect)

        pygame.display.update()