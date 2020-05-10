import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WALL_SIZE = 10
STEP = 10


class BlockSprite(pygame.sprite.Sprite):

    def __init__self(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class BallSprite(pygame.sprite.Sprite):

    def __init__(self, fnm):
        super().__init__()
        self.image = pygame.image.load(fnm).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.center = [scrWidth/2, scrHeight/2]

        self.xStep, self.yStep = self.randomSteps()


    def randomSteps(self):
        x = STEP
        if random.random() > 0.5:
            x = -x
        y = STEP
        if random.random() > 0.5:
            y = -y
        return [x, y]


    def update(self):
        if pygame.sprite.spritecollideany(self, horizWalls):
            self.yStep = -self.yStep

        if pygame.sprite.spritecollideany(self, vertWalls):
            self.xStep = -self.xStep

        self.rect.x += self.xStep
        self.rect.y += self.yStep       
    
        
