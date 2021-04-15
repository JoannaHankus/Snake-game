import random
import pygame

pygame.init()

crash_sound = pygame.mixer.Sound("Wood_Hit_Metal_Crash.wav")
apple_sound = pygame.mixer.Sound("Hair_Ripping.wav")
pygame.mixer.music.load("Jazz_Me_Blues.wav")

bg = pygame.image.load("bg.png")
image_surf_1 = pygame.image.load("snaked1.png")
image_surf_2 = pygame.image.load("snaked2.png")

intro_image = pygame.image.load("intro.png")
apple_surf = pygame.image.load("apple.png")
whole_surf = pygame.image.load("block.png")
headleft = pygame.image.load("headleft.png")
headright = pygame.image.load("headright.png")
headdown = pygame.image.load("headdown.png")
headup = pygame.image.load("headup.png")

bgLvl2 = pygame.image.load("bgLvl2.png")
bgLvl3 = pygame.image.load("bgLvl3.png")
bgLvl4 = pygame.image.load("bgLvl4.png")

ScreenWidth = 560
ScreenHeight = 400
bsize = 20


lvl = 1
nxtLvl= False

black = (0, 0, 0)
white = (255, 255, 255)
red = (212, 0, 0)
green = (63, 203, 45)
yellow = (220, 212, 0)

bright_red = (255, 0, 0)
bright_green = (73, 235, 52)
bright_yellow= (253, 244, 2)

win = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption('SNAKE')

clock = pygame.time.Clock()
pause = True



class Snake:
    x = [0]
    y = [0]
    left = False
    right = True
    up = False
    down = False
    step = 20



    def __init__(self, length):
        self.length = length

        self.dirx = 1
        self.diry = 0
        self.left = 0
        self.right = 1
        self.up = 0
        self.down = 0

        for i in range(0, 2000):
            self.x.append(0)
            self.y.append(0)

    def update(self):


        # update previous positions
            for i in range(self.length, 0, -abs(1)):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            if self.dirx == 1 and self.diry == 0:
                self.x[0] = self.x[0] + self.step
            elif self.dirx == -1 and self.diry == 0:
                self.x[0] = self.x[0] - self.step
            elif self.dirx == 0 and self.diry == -1:
                self.y[0] = self.y[0] - self.step
            elif self.dirx == 0 and self.diry == 1:
                self.y[0] = self.y[0] + self.step

            # transposition after boundcrossing
            if lvl != 2:
                if self.dirx == 1 and self.x[0] >= ScreenWidth:
                    self.x[0] = 0
                elif self.dirx == -1 and self.x[0] < 0:
                    self.x[0] = ScreenWidth
                elif self.dirx == 0 and self.y[0] < 0:
                    self.y[0] = ScreenHeight
                elif self.dirx == 0 and self.y[0] >= ScreenHeight:
                    self.y[0] = 0



    def move(self):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            # for key in keys:
            if keys[pygame.K_RIGHT]:
                self.dirx = 1
                self.diry = 0
                self.right = True
                self.left = False
                self.up = False
                self.down = False

            elif keys[pygame.K_LEFT]:
                self.dirx = -1
                self.diry = 0
                self.right = False
                self.left = True
                self.up = False
                self.down = False

            elif keys[pygame.K_UP]:
                self.dirx = 0
                self.diry = -1
                self.right = False
                self.left = False
                self.up = True
                self.down = False

            elif keys[pygame.K_DOWN]:
                self.dirx = 0
                self.diry = 1
                self.right = False
                self.left = False
                self.up = False
                self.down = True

            elif keys[pygame.K_p]:
                pause = True
                paused()

    def draw(self, win, image1, image2):
        for i in range(1, self.length, 2):
            win.blit(image1, (self.x[i], self.y[i]))
        for i in range(2, self.length, 2):
            win.blit(image2, (self.x[i], self.y[i]))


    def drawHead(self, win):
        global headleft, headright, headup, headdown
        if self.left:
            win.blit(headleft, (self.x[0], self.y[0]))
        elif self.right:
            win.blit(headright, (self.x[0], self.y[0]))
        elif self.up:
            win.blit(headup, (self.x[0], self.y[0]))
        elif self.down:
            win.blit(headdown, (self.x[0], self.y[0]))


class Apple:
    #global ScreenHeight, ScreenWidth

    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x*20
        self.y = y* 20

    def draw(self, win, image):
        win.blit(image, (self.x, self.y))


def redrawWindow(win):
    global bg, apple_surf, image_surf_1, image_surf_2,  snake, apple, whole, nxtLvl, lvl, bgLvl2, bgLvl3, bgLvl4
    if lvl == 2:
        win.blit(bgLvl2, (0, 0))
    elif lvl == 3:
        win.blit(bgLvl3, (0, 0))
    elif lvl == 4:
        win.blit(bgLvl4, (0, 0))

    else:
        win.blit(bg, (0, 0))
    snake.drawHead(win)

    snake.draw(win, image_surf_1, image_surf_2 )
    apple.draw(win, apple_surf)
    if nxtLvl:
        whole.draw(win, whole_surf)
    pygame.display.update()



def isCollision(x1, y1, x2, y2, size_x, size_y):
    if x1 >= x2 and x1 < x2 + size_x:
        if y1 >= y2 and y1 < y2 + size_y:
            return True

    return False

def collision(score):


    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    largeText = pygame.font.Font('freesansbold.ttf', 78)
    TextSurf, TextRect = give_me_txt("GAME OVER", largeText)
    TextRect.center = ((ScreenWidth / 2), ((ScreenHeight / 2)-60))
    win.blit(TextSurf, TextRect)


    myFont = pygame.font.Font('freesansbold.ttf', 48)
    LabelSurf, LabelRect = give_me_txt("Your score is:", myFont)
    LabelRect.center = ((ScreenWidth/2), (ScreenHeight/2))
    win.blit(LabelSurf, LabelRect)

    ScoreSurf, ScoreRect = give_me_txt(str(score), myFont)
    ScoreRect.center = ((ScreenWidth/2), ((ScreenHeight/2)+54))
    win.blit(ScoreSurf, ScoreRect)




    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



        button("Play Again", 90, 280, 120, 50, green, bright_green, main)
        button("QUIT!", 370, 280, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def give_me_txt(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:

        pygame.draw.rect(win, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(win, ic, (x, y, w, h))


    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = give_me_txt(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    win.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()

def helper():
    global helping
    helping = True
    text = pygame.font.Font('freesansbold.ttf', 20)

    while helping:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.blit(bg, (0, 0))
        TextSurf1, TextRect1 = give_me_txt("Kieruj wężem za pomocą strzałek!", text)
        TextSurf2, TextRect2 = give_me_txt("Zbieraj jedzenie najeżdżając na nie!", text)
        TextSurf3, TextRect3 = give_me_txt("Nie zderz się z przeszkodami ani z samym sobą!", text)
        TextSurf4, TextRect4 = give_me_txt("Przechodz na kolejne poziomy przez portale!", text)
        TextSurf5, TextRect5 = give_me_txt("Za każdy poziom otrzymasz punkty premii!", text)

        TextRect1.center = ((ScreenWidth / 2), ((ScreenHeight / 2) - 150))
        TextRect2.center = ((ScreenWidth / 2), ((ScreenHeight / 2) - 100))
        TextRect3.center = ((ScreenWidth / 2), ((ScreenHeight / 2) - 50))
        TextRect4.center = ((ScreenWidth / 2), ((ScreenHeight / 2) + 0))
        TextRect5.center = ((ScreenWidth / 2), ((ScreenHeight / 2) + 50))

        win.blit(TextSurf1, TextRect1)
        win.blit(TextSurf2, TextRect2)
        win.blit(TextSurf3, TextRect3)
        win.blit(TextSurf4, TextRect4)
        win.blit(TextSurf5, TextRect5)


        button("GO!", 90, 280, 100, 50, green, bright_green, main)
        button("QUIT!", 370, 280, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def paused():
    global pause
    pause = True
    pygame.mixer.music.pause()

    largeText = pygame.font.Font('freesansbold.ttf', 95)
    TextSurf, TextRect = give_me_txt("PAUSED", largeText)
    TextRect.center = ((ScreenWidth / 2), ((ScreenHeight / 2)-30))
    win.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()




        button("continue", 90, 250, 100, 50, green, bright_green, unpause)
        button("QUIT!", 370, 250, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.blit(intro_image, (0,0))

        button("GO!",90, 280, 100, 50, green, bright_green, main)
        button("HELP", 230, 280, 100, 50, yellow, bright_yellow, helper)
        button("QUIT!", 370, 280, 100, 50, red, bright_red, quitgame)



        pygame.display.update()
        clock.tick(15)

def level4():


    global lvl, nxtLvl
    nxtLvl = False
    lvl = 4
    list = [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18]
    score = snake.length - 3 + 5 + 8
    bonus = 10
    score = score + bonus

    if apple.x == 0 or apple.x == ScreenWidth - bsize or apple.y == 0 or apple.y == ScreenHeight-20:

        if apple.y == 3 or apple.y == 9 or apple.y == 16:
            apple.x = random.randint(1, 27) * bsize
            apple.y = random.choice(list) * bsize
        else:
            apple.x = random.randint(1, 26) * bsize
            apple.y = random.randint(1, 18) * bsize



    run4 = True

    while run4:
        pygame.time.delay(100)
        clock.tick(50)

        snake.move()
        snake.update()



        if isCollision(snake.x[0], snake.y[0], apple.x, apple.y, bsize, bsize):
            pygame.mixer.Sound.play(apple_sound)
            apple.x = random.randint(1, 26) * bsize
            apple.y = random.choice(list) * bsize
            snake.length = snake.length + 1
            score = score + 1

        if isCollision(snake.x[0], snake.y[0], 0, 0, ScreenWidth, bsize):
            collision(score)

        if isCollision(snake.x[0], snake.y[0], 0, 0, bsize, ScreenHeight):
            collision(score)
        if isCollision(snake.x[0], snake.y[0], 0, ScreenHeight-bsize, ScreenWidth, bsize):
            collision(score)
        if isCollision(snake.x[0], snake.y[0], ScreenWidth-bsize, 0, bsize, ScreenHeight):
            collision(score)


        if isCollision(snake.x[0], snake.y[0], 4 * bsize, 3 * bsize, 20 * bsize, bsize):
            collision(score)

        if isCollision(snake.x[0], snake.y[0], 4 * bsize, 9 * bsize, 20 * bsize, bsize):
            collision(score)
        if isCollision(snake.x[0], snake.y[0], 4 * bsize, 16 * bsize, 20 * bsize, bsize):
            collision(score)


        for i in range(2, snake.length):
            if isCollision(snake.x[0], snake.y[0], snake.x[i], snake.y[i], bsize, bsize):

                collision(score)

        redrawWindow(win)


def level3():


    global lvl, nxtLvl
    nxtLvl = False
    lvl = 3
    list = [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19]

    bonus = 8
    score = snake.length - 3 + 5
    score = score + bonus

    if apple.y == 3 or apple.y == 9 or apple.y == 16:
        apple.x = random.randint(1, 27) * bsize
        apple.y = random.choice(list) * bsize

    run3 = True

    while run3:
        pygame.time.delay(100)
        clock.tick(50)

        snake.move()
        snake.update()


        if isCollision(snake.x[0], snake.y[0], apple.x, apple.y, bsize, bsize):
            pygame.mixer.Sound.play(apple_sound)
            apple.x = random.randint(1, 27) * bsize
            apple.y = random.choice(list) * bsize
            snake.length = snake.length + 1
            score = score + 1

        if isCollision(snake.x[0], snake.y[0], 2*bsize, 3*bsize, 24*bsize, bsize):
            collision(score)

        if isCollision(snake.x[0], snake.y[0], 2*bsize, 9*bsize,24*bsize, bsize):
            collision(score)
        if isCollision(snake.x[0], snake.y[0], 2*bsize, 16*bsize, 24*bsize, bsize):
            collision(score)


        for i in range(2, snake.length):
            if isCollision(snake.x[0], snake.y[0], snake.x[i], snake.y[i], bsize, bsize):
                collision(score)

        redrawWindow(win)

        if score > 20:
            nxtLvl = True
        if isCollision(snake.x[0], snake.y[0], whole.x, whole.y, bsize, bsize):
            level4()



def level2():


    global lvl, nxtLvl
    nxtLvl = False
    lvl = 2
    bonus = 5
    score = snake.length - 3
    score = score + bonus

    if apple.x == 0 or apple.x == ScreenWidth - bsize or apple.y == 0 or apple.y == ScreenHeight-20:
        apple.x = random.randint(1, 26) * bsize
        apple.y = random.randint(1, 18) * bsize



    run2 = True

    while run2:
        pygame.time.delay(100)
        clock.tick(50)

        snake.move()
        snake.update()



        if isCollision(snake.x[0], snake.y[0], apple.x, apple.y, bsize, bsize):
            pygame.mixer.Sound.play(apple_sound)
            apple.x = random.randint(1, 26) * bsize
            apple.y = random.randint(1, 18) * bsize
            snake.length = snake.length + 1
            score = score + 1

        if isCollision(snake.x[0], snake.y[0], 0, 0, ScreenWidth, bsize):
            collision(score)

        if isCollision(snake.x[0], snake.y[0], 0, 0, bsize, ScreenHeight):
            collision(score)
        if isCollision(snake.x[0], snake.y[0], 0, ScreenHeight-bsize, ScreenWidth, bsize):
            collision(score)
        if isCollision(snake.x[0], snake.y[0], ScreenWidth-bsize, 0, bsize, ScreenHeight):
            collision(score)


        for i in range(2, snake.length):
            if isCollision(snake.x[0], snake.y[0], snake.x[i], snake.y[i], bsize, bsize):

                collision(score)

        redrawWindow(win)

        if score> 10:
            nxtLvl = True
        if isCollision(snake.x[0], snake.y[0], whole.x, whole.y, bsize, bsize):
            level3()



def main():
    global bg, apple_surf, image_surf, ScreenHeight, ScreenWidth, snake, apple, whole, headleft, headright, headup, headdown
    global lvl, nxtLvl
    nxtLvl = False
    lvl = 1
    score = 0
    global pause

    pygame.mixer.music.play(-1)

    length = 3
    snake = Snake(length)
    apple = Apple(3, 4)
    whole = Apple(10, 5)

    run = True

    while run:
        pygame.time.delay(100)
        clock.tick(50)

        snake.move()
        snake.update()

        if isCollision(snake.x[0], snake.y[0], apple.x, apple.y, bsize, bsize):
            pygame.mixer.Sound.play(apple_sound)
            apple.x = random.randint(1, 27) * bsize
            apple.y = random.randint(1, 19) * bsize
            snake.length = snake.length + 1
            score = score + 1



        if snake.length > 3:
            for i in range(2, snake.length):
                if isCollision(snake.x[0], snake.y[0], snake.x[i], snake.y[i], bsize, bsize):
                    collision(score)

        redrawWindow(win)

        if score> 1:
            nxtLvl = True

        if isCollision(snake.x[0], snake.y[0], whole.x, whole.y, bsize, bsize):
            level2()


game_intro()
main()
pygame.quit()
quit()
