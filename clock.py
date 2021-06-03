import pygame
import sys

# --- constants ---

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)


# --- main ---

def main():
    pygame.init()
    pygame.display.set_caption("Metronmome")
    font = pygame.font.Font(None, 40)
    screen = pygame.display.set_mode((500, 400), 0, 32)
    # time in millisecond from start program
    current_time = pygame.time.get_ticks()

    # how long to show or hide
    bpm = 120

    delay = (60/bpm * 1000) / 2# 500ms = 0.5s

    # time of next change
    change_time = current_time + delay
    show = True
    sound_play = True
    sound = pygame.mixer.Sound('./assets/click.wav')

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- updates ---

        current_time = pygame.time.get_ticks()

        # is time to change ?
        if current_time >= change_time:
            # time of next change
            change_time = current_time + delay
            show = not show
            sound_play = not sound_play

        # --- draws ---

        screen.fill(BLACK)
        text = font.render("%s" % int(bpm), True, (255, 255, 255))
        screen.blit(text, [20, 10])  # 文字列の表示位置

        if show:
            pygame.draw.rect(screen, WHITE,(100,10,40,40))
        if sound_play:
            sound.play()

        pygame.display.update()




if __name__ == '__main__':
    main()