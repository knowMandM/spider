import pygame
import test

class MineGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 320))

    def main(self):
        while True:
            self.screen.fill((128,128,128))
            print(pygame.draw.rect(self.screen, (255, 0, 0), ((100,100),(100,100)) ))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                    # test.DifficultSelect().main()
            pygame.display.flip()

if __name__ == "__main__":
    MineGame().main()