import pygame,sys,random


pygame.mixer.pre_init(44100, 16,2,4096)
pygame.init()
clock = pygame.time.Clock()
screenHeight = 600
screenWidth = 900
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("~DeadZone~")
background = pygame.image.load("background.jpg")
pygame.mouse.set_visible(False)

pygame.mixer.music.load("creepy.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture,scorefont):
        super().__init__()
        self.image = pygame.image.load(picture)
        self.image = pygame.transform.scale(self.image,(60,60))
        self.rect = self.image.get_rect()
        self.gun = pygame.mixer.Sound("loud-pistol-shot.mp3")
        self.gun.set_volume(0.5)
        self.font = pygame.font.Font(scorefont,32)
        self.score = 0
        self.scorecard = self.font.render(str(self.score), True, (255,255,255), None)
    def shooting(self):
        self.gun.play()
        self.hit = pygame.sprite.spritecollide(crosshair,zombies,True)
        for self.sprite in self.hit:
            self.score+=1
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.scorecard = self.font.render(str(self.score), True, (255,255,255), None)
        screen.blit(self.scorecard,(50,50))



    

crosshair = Crosshair("crosshair.png", "FFFFORWA.TTF")

crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)
class Zombie(pygame.sprite.Sprite):
    def __init__(self,x,y) -> None:
        super().__init__()
        self.image = pygame.image.load("zombie.png")
        self.speed = [random.randrange(0,5),random.randrange(0,5)]
        self.image = pygame.transform.scale(self.image, (64,100))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.left < 0 or self.rect.right > screenWidth:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > screenHeight:
            self.speed[1] = -self.speed[1]
        
zombies = pygame.sprite.Group()
for i in range(20):
    zombie = Zombie(random.randrange(100,screenWidth-100), random.randrange(200,screenHeight-100))
    zombies.add(zombie)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shooting()



    pygame.display.flip()
    screen.blit(background,(0,0))
    zombies.draw(screen)
    crosshair_group.draw(screen)




    crosshair_group.update()
    zombies.update()
    clock.tick(60)
