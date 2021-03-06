import pygame
import math

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RAINBOW = [(94, 189, 62), (255, 185, 0), (247, 130, 0), (226, 56, 56), (151, 57, 153), (0, 156, 223)]

# Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    velocity = 7

    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.mousePosition = pygame.mouse.get_pos()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        # If the mouse is within window and it moved from previous position
        # If the mouse hasn't moved, player can still be moved with keyboard with the mouse within the window
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
    speed = 4.0
    direction = 45.0

    def __init__(self, color, diameter, x, y):
        super().__init__()
        self.diameter = diameter
        self.radius = int(diameter / 2) - 1
        self.image = pygame.Surface([self.diameter, self.diameter])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.wallEffect = pygame.mixer.Sound("./lib/wall.wav")
        
    def changeDirection(self, plane, deflect):
        # If ball hit the player, use deflect coeficient
        if deflect != 0:
            self.direction = (360 - deflect) % 360
        # If the plane hit is horizontal
        elif plane == 'h':
            self.direction = (180 - self.direction) % 360
        # If the plane hit is vertical
        elif plane == 'v':
            self.direction = (360 - self.direction) % 360

    # Function updates the ball coordinates, changes the ball direction when wall is hit
    # If the ball hits the bottom wall, function returns True to indicate the end of the game.
    # Otherwise returns false.
    def update(self):
        radDirection = math.radians(self.direction)
        self.rect.x += round(self.speed * math.sin(radDirection))
        self.rect.y -= round(self.speed * math.cos(radDirection))

        if self.rect.x <= 0:
            self.rect.x = 1
            self.wallEffect.play()
            self.changeDirection('v', 0)
        if self.rect.x + self.diameter >= SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - self.diameter - 1
            self.wallEffect.play()
            self.changeDirection('v', 0)
        if self.rect.y <= 0:
            self.rect.y = 1
            self.wallEffect.play()
            self.changeDirection('h', 0)
        if self.rect.y + self.diameter >= SCREEN_HEIGHT:
            return True
        
        return False

class MenuItem():
    def __init__(self, text, color, font, y):
        self.title = text
        self.font = font
        self.text = self.font.render(self.title, True, color)
        self.color = color
        self.rect = self.text.get_rect()
        self.rect.x = SCREEN_WIDTH/2 - self.rect.width/2
        self.rect.y = y
        self.highlightedByMouse = False

    def mouseOver(self, mousePosition):
        if self.rect.collidepoint(mousePosition):
            self.color = RAINBOW[1]
            self.highlightedByMouse = True
        else:
            self.color = WHITE
            self.highlightedByMouse = False
        self.text = self.font.render(self.title, True, self.color)

    def blit(self, screen):
        screen.blit(self.text, self.rect)

    def select(self):
        self.color = RAINBOW[1]
        self.text = self.font.render(self.title, True, self.color)

    def unselect(self):
        self.color = WHITE
        self.text = self.font.render(self.title, True, self.color)
        
def isMouseOverMenu(menuItems):
    for item in menuItems:
        if item.highlightedByMouse:
            return True
    return False

def handleEnterInMenu(showContinue, selectedItem):
    if (showContinue and selectedItem == 1) or (not showContinue and selectedItem == 0):
        return True
    elif showContinue and selectedItem == 0:
        return False
    elif (showContinue and selectedItem == 2) or (not showContinue and selectedItem == 1):
        pygame.quit()
        quit()

# Function represents menu screen. 
# If showContinue is true, game has been paused and the option to continue it will show.
# The title argument contains string, that will show as a caption of the menu screen.
def menu(rowHeight, showContinue, title):
    titleFont = pygame.font.Font("./lib/Code_Pro_Demo.ttf", 114)
    menuItemFont = pygame.font.Font("./lib/Code_Pro_Demo.ttf", 50)
    
    menuTitle = MenuItem(title, BLACK, titleFont, 120)
    menuItems = []
    selectedItem = None

    if showContinue:
        menuItems.append(MenuItem("Continue", WHITE, menuItemFont, 300+len(menuItems)*70))
    menuItems.append(MenuItem("New Game", WHITE, menuItemFont, 300+len(menuItems)*70))
    menuItems.append(MenuItem("Quit", WHITE, menuItemFont, 300+len(menuItems)*70))
    menuLen = len(menuItems)

    while True:
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Mouse controls in menu
            if event.type == pygame.MOUSEBUTTONUP:
                if menuItems[menuLen-2].rect.collidepoint(mousePos):
                    return True
                if showContinue and menuItems[0].rect.collidepoint(mousePos):
                    return False
                if menuItems[menuLen-1].rect.collidepoint(mousePos):
                    pygame.quit()
                    quit()
            # Keyboard controls in menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if selectedItem == None:
                        selectedItem = 0
                    else:
                        selectedItem = (selectedItem + 1) % menuLen
                if event.key == pygame.K_UP:
                    if selectedItem == None:
                        selectedItem = menuLen - 1
                    else:
                        selectedItem = (selectedItem - 1) % menuLen
                if (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN) and selectedItem != None:
                    return handleEnterInMenu(showContinue, selectedItem)

        # Highlight menu item if mouse is over it
        for item in menuItems:
            item.mouseOver(mousePos)
        # If mouse is over item in menu, delete the selection that was made by keyboard
        if isMouseOverMenu(menuItems):
            selectedItem = None
        # If mouse is not over any item, and something is selected by keyboard, highlight it
        if selectedItem != None:
            for i in range(menuLen):
                if i == selectedItem:
                    menuItems[i].select()
                else:
                    menuItems[i].unselect()
        
        screen.fill(BLACK)
        # Draw the rainbow across screen
        for row in range(6):
            pygame.draw.rect(screen, RAINBOW[row], [0, 100 + row * rowHeight, SCREEN_WIDTH, rowHeight])
        # Draw the title
        menuTitle.blit(screen)
        # Draw each menu item
        for item in menuItems:
            item.blit(screen)
        pygame.display.flip()
        clock.tick(15)

# Function decides, whether to bounce vertically or horizontally when ball hits the block/s
def bounceDirection(ball, hitBlocks):
    if len(hitBlocks) > 1:
        checkRow = hitBlocks[0].rect.y
        for h in hitBlocks:
            if checkRow != h.rect.y:
                return 'v'
    else:
        block = hitBlocks[0].rect
        # Margin of error represents the pixel offset, that is still acceptable to determine
        # which side of the block was hit by the ball
        marginOfError = ball.speed + ball.speed/2
        if abs(ball.rect.right-block.left) < marginOfError:
            return 'v'
        if abs(ball.rect.left-block.right) < marginOfError:
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
    
    # Init of all the sound effects
    blockEffects = {
        RAINBOW[5]: pygame.mixer.Sound('./lib/block1.wav'),
        RAINBOW[4]: pygame.mixer.Sound('./lib/block2.wav'),
        RAINBOW[3]: pygame.mixer.Sound('./lib/block3.wav'),
        RAINBOW[2]: pygame.mixer.Sound('./lib/block4.wav'),
        RAINBOW[1]: pygame.mixer.Sound('./lib/block5.wav'),
        RAINBOW[0]: pygame.mixer.Sound('./lib/block6.wav'),
    }
    playerEffect = pygame.mixer.Sound('./lib/player.wav')

    # Pause button
    pauseButton = pygame.image.load("./lib/pause-16.png")
    pauseRect = pauseButton.get_rect()
    pauseRect.x, pauseRect.y = SCREEN_WIDTH - pauseRect.width - 5, 5

    titleText = "Breakout"
    resetNewGame = False
    # Loop alternating the menu and new game
    # If resetNewGame is true, don't show the menu
    while resetNewGame or menu(blockHeight, False, titleText):
        # Init all objects - player, ball, blocks and all the sprite groups
        titleText = "Breakout"
        resetNewGame = False
        allSprites = pygame.sprite.Group()
        blockSprites = pygame.sprite.Group()
        ballSprites = pygame.sprite.Group()

        player = Player(WHITE, 120, 15, SCREEN_WIDTH/2, SCREEN_HEIGHT - 2*15)
        allSprites.add(player)

        ball = Ball(WHITE, 15, SCREEN_WIDTH/2, SCREEN_HEIGHT-15-2*player.height)
        ballSprites.add(ball)
        allSprites.add(ball)

        for row in range(6):
            for col in range(10):
                block = Block(RAINBOW[row], blockWidth, blockHeight, col * blockWidth, 100 + row * blockHeight)
                allSprites.add(block)
                blockSprites.add(block)

        # Main game loop
        run = True
        while run:
            for event in pygame.event.get():
                # Quitting on window close
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Pausing the game
                if event.type == pygame.MOUSEBUTTONUP:
                    if pauseRect.collidepoint(pygame.mouse.get_pos()):
                        resetNewGame = menu(blockHeight, True, titleText)
                        run = not resetNewGame
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        resetNewGame = menu(blockHeight, True, titleText)
                        run = not resetNewGame

            # Player controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.moveLeft()
            elif keys[pygame.K_RIGHT]:
                player.moveRight()
            else:
                player.moveMouse()

            # Collision detection between player and ball
            if pygame.sprite.spritecollide(player, ballSprites, False):
                if abs(player.rect.top - ball.rect.bottom) < ball.speed:
                    playerEffect.play()
                    deflect = (player.rect.left + player.width/2) - (ball.rect.left + ball.diameter/2)
                    ball.changeDirection('h', deflect)
            # Collision detection between ball and blocks
            hitBlocks = pygame.sprite.spritecollide(ball, blockSprites, True)
            if len(hitBlocks) > 0:
                blockEffects[hitBlocks[0].color].play()
                ball.changeDirection(bounceDirection(ball, hitBlocks), 0)

            # End game when all blocks have been hit
            if len(blockSprites) == 0:
                run = False
                titleText = "You Win"
            # End game when ball hits the bottom of the screen
            if ball.update():
                run = False
                titleText = "You Lose"
            
            screen.fill(BLACK)
            screen.blit(pauseButton, pauseRect)
            allSprites.draw(screen)
            pygame.display.flip()
            clock.tick(100)
