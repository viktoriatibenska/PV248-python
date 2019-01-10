# TODO: end game
# TODO: continue in menu
# TODO: change of direction according to where the ball hit the paddle

import pygame
import pygame.gfxdraw
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RAINBOW = [(94, 189, 62), (255, 185, 0), (247, 130, 0), (226, 56, 56), (151, 57, 153), (0, 156, 223)]

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, velocity):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.mousePosition = pygame.mouse.get_pos()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity

    def moveRight(self):
        if self.rect.x + self.velocity + self.width <= SCREEN_WIDTH:
            self.rect.x += self.velocity
        else:
            self.rect.x = SCREEN_WIDTH - self.width

    def moveLeft(self):
        if self.rect.x - self.velocity >= 0:
            self.rect.x -= self.velocity
        else:
            self.rect.x = 0

    def moveMouse(self):
        currentMousePosition = pygame.mouse.get_pos()

        if pygame.mouse.get_focused() != 0 and currentMousePosition != self.mousePosition:
            self.mousePosition = currentMousePosition
            self.rect.x = self.mousePosition[0] - self.width / 2
            if self.rect.x < 0:
                self.rect.x = 0
            if self.rect.x + self.width > SCREEN_WIDTH:
                self.rect.x = SCREEN_WIDTH - self.width

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color

class Ball(pygame.sprite.Sprite):
    speed = 6.0
    direction = 45.0

    def __init__(self, color, diameter, x, y):
        super().__init__()
        self.diameter = diameter
        self.radius = int(diameter / 2) - 1
        self.image = pygame.Surface([self.diameter, self.diameter], pygame.SRCALPHA)
        self.image.fill(color)
        # pygame.gfxdraw.filled_circle(self.image, x, y, self.radius, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.wallEffect = pygame.mixer.Sound("./lib/wall.wav")
        
    def changeDirection(self, plane):
        # If the plane hit is horizontal
        if plane == 'h':
            self.direction = (180 - self.direction) % 360
        # If the plane hit is vertical
        elif plane == 'v':
            self.direction = (360 - self.direction) % 360

    def update(self):
        radDirection = math.radians(self.direction)
        self.rect.x += self.speed * math.sin(radDirection)
        self.rect.y -= self.speed * math.cos(radDirection)

        if self.rect.x <= 0:
            self.wallEffect.play()
            self.changeDirection('v')
        if self.rect.x + self.diameter >= SCREEN_WIDTH:
            self.wallEffect.play()
            self.changeDirection('v')
        if self.rect.y <= 0:
            self.wallEffect.play()
            self.changeDirection('h')
        if self.rect.y + self.diameter >= SCREEN_HEIGHT:
            self.changeDirection('h')


def menu(rowHeight):
    titleFont = pygame.font.Font("./lib/Code_Pro_Demo.ttf", 114)
    menuItemFont = pygame.font.Font("./lib/Code_Pro_Demo.ttf", 50)
    titleText = titleFont.render("Breakout", True, BLACK)
    titlePos = titleText.get_rect(centerx=SCREEN_WIDTH/2)
    titlePos.top = 120

    playText = menuItemFont.render("New Game", True, WHITE)
    playRect = playText.get_rect()
    playRect.x, playRect.y = SCREEN_WIDTH/2 - playRect.width/2, 300
    
    quitText = menuItemFont.render("Quit", True, WHITE)
    quitRect = quitText.get_rect()
    quitRect.x, quitRect.y = SCREEN_WIDTH/2 - quitRect.width/2, 370

    menu = True
    while menu:
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if playRect.collidepoint(mousePos):
                    menu = False
                if quitRect.collidepoint(mousePos):
                    pygame.quit()
                    quit()
        
        playColor, quitColor = WHITE, WHITE
        if playRect.collidepoint(mousePos):
            playColor = RAINBOW[1]
        if quitRect.collidepoint(mousePos):
            quitColor = RAINBOW[1]
        playText = menuItemFont.render("New Game", True, playColor)
        quitText = menuItemFont.render("Quit", True, quitColor)

        screen.fill(BLACK)
        for row in range(6):
            pygame.draw.rect(screen, RAINBOW[row], [0, 100 + row * rowHeight, SCREEN_WIDTH, rowHeight])
        screen.blit(titleText, titlePos)
        screen.blit(playText, playRect)
        screen.blit(quitText, quitRect)
        pygame.display.flip()
        clock.tick(15)

def bounceDirection(ball, hitBlocks):
    if len(hitBlocks) > 1:
        checkRow = hitBlocks[0].rect.y
        for h in hitBlocks:
            if checkRow != h.rect.y:
                return 'v'
    else:
        block = hitBlocks[0].rect
        if abs(ball.rect.right-block.left) < ball.speed:
            print("Left contact", ball.rect.right, block.left)
            return 'v'
        if abs(ball.rect.left-block.right) < ball.speed:
            print("Right contact", ball.rect.left, block.right)
            return 'v'


    return 'h'

if __name__ == "__main__":
    blockWidth = 80
    blockHeight = 20

    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    # Create screen and clock
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    pygame.display.set_caption("Breakout")
    
    blockEffects = {
        RAINBOW[5]: pygame.mixer.Sound('./lib/block1.wav'),
        RAINBOW[4]: pygame.mixer.Sound('./lib/block2.wav'),
        RAINBOW[3]: pygame.mixer.Sound('./lib/block3.wav'),
        RAINBOW[2]: pygame.mixer.Sound('./lib/block4.wav'),
        RAINBOW[1]: pygame.mixer.Sound('./lib/block5.wav'),
        RAINBOW[0]: pygame.mixer.Sound('./lib/block6.wav'),
    }

    # Start menu
    menu(blockHeight)

    # Pause button
    pauseButton = pygame.image.load("./lib/pause-16.png")
    pauseRect = pauseButton.get_rect()
    pauseRect.x, pauseRect.y = SCREEN_WIDTH - pauseRect.width - 5, 5

    allSprites = pygame.sprite.Group()
    blockSprites = pygame.sprite.Group()

    # Create player
    player = Player(WHITE, 120, 15, SCREEN_WIDTH/2, SCREEN_HEIGHT - 2*15, 10)
    allSprites.add(player)
    playerEffect = pygame.mixer.Sound('./lib/player.wav')

    ball = Ball(WHITE, 15, SCREEN_WIDTH/2, SCREEN_HEIGHT-15-2*player.height)
    ballSprites = pygame.sprite.Group()
    ballSprites.add(ball)
    allSprites.add(ball)

    # Create blocks
    for row in range(6):
        for col in range(10):
            block = Block(RAINBOW[row], blockWidth, blockHeight, col * blockWidth, 100 + row * blockHeight)
            allSprites.add(block)
            blockSprites.add(block)

    run = True
    while run:
        for event in pygame.event.get():
            # Quitting on window close
            if event.type == pygame.QUIT:
                run = False
            # Pausing the game
            if event.type == pygame.MOUSEBUTTONUP:
                if pauseRect.collidepoint(pygame.mouse.get_pos()):
                    menu(blockHeight)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu(blockHeight)

        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.moveLeft()
        elif keys[pygame.K_RIGHT]:
            player.moveRight()
        else:
            player.moveMouse()

        if pygame.sprite.spritecollide(player, ballSprites, False):
            if abs(player.rect.top - ball.rect.bottom) < ball.speed:
                playerEffect.play()
                ball.changeDirection('h')

        hitBlocks = pygame.sprite.spritecollide(ball, blockSprites, True)
        if len(hitBlocks) > 0:
            blockEffects[hitBlocks[0].color].play()
            ball.changeDirection(bounceDirection(ball, hitBlocks))

        allSprites.update()
        screen.fill(BLACK)
        screen.blit(pauseButton, pauseRect)
        allSprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
