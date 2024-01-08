import pygame


def scrolling_credits(screen, clock, start_y):
    text = """Спасибо за игру"""
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, (255, 255, 255))
    y = start_y
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(text_surf, (50, y))
        y -= 1  # скорость скроллинга

        if y < -text_surf.get_height():
            running = False

        pygame.display.flip()
        clock.tick(60)

