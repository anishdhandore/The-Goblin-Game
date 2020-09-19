import pygame
pygame.init()

window = pygame.display.set_mode((500,480))
pygame.display.set_caption("Attackkk")
clock = pygame.time.Clock()

# images to define
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
backg = pygame.image.load("backg.jpg")
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.walkCount = 0
        self.standing = True
        self.left = False
        self.right = False
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        
    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if not(self.standing):
            if self.left:
                window.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

            elif self.right:
                window.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

        else:
            if self.left:
                window.blit(walkLeft[0], (self.x, self.y))
            else:
                window.blit(walkRight[0], (self.x, self.y))
                
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(window,(255,0,0), self.hitbox, 2)
        
    def hit(self, window):
        
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render("-1", 1, (255,0,0))
        window.blit(text, (230,200))
        pygame.display.update()
        
    
        pygame.time.delay(100)
            
        
        
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * self.facing   # facing gives the dir, whether + or -
        
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.vel = 3
        self.walkCount = 0
        self.hitbox = (self.x + 20, self.y , 29, 60)
        self.health = 50
        self.visibility = True # new
        
    def draw(self, window):
        self.move()
        if self.visibility:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                window.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

            else:
                window.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(window, (255,0,0), (self.hitbox[0], self.hitbox[1]-20,50,10))
            pygame.draw.rect(window, (0,128,0), (self.hitbox[0], self.hitbox[1]-20, 50 - (1 * (50-self.health)), 10))
            self.hitbox = (self.x + 20, self.y, 29, 60)
            #pygame.draw.rect(window, (255,0,0), self.hitbox, 2)

    def move(self):     # the enemy has only 1 path in x direction
        
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:   # if we have not reached the furthest right point
                self.x += self.vel                 # think like this : x se jyaada aage nahi jaa sakta
                
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
                
        else:
            if self.x - self.vel > self.path[0]:   # if we have not reached the furthest left point
                self.x += self.vel              # x se kam nahi ho sakta isliye x has to be greater
                
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
                
    def hit(self):
        
        if self.health > 0:
            self.health -= 1
        else:
            self.visibility = False
           
        print("it hit me")

def redraw_window():
    
    window.blit(backg, (0,0))
    
    font = pygame.font.SysFont("comicsans", 50)
    text = font.render("Score : " +str(score), 1, (255,255,255))   #(text,antialias,color)
    window.blit(text, (330,10))
    
    man.draw(window)
    goblin.draw(window)
    
    for bullet in bullets:
        bullet.draw(window)
    
    pygame.display.update()

# main loop
man = player(10,400,64,64)
goblin = enemy(50,400,64,64,380)
shootLoop = 0
score = 0

#sounds

music = pygame.mixer.music.load("MattyBraps - Let's Dance (feat. Ty Pittman).mp3")
pygame.mixer.music.play(-1)  # (-1) keeps the song on loop

bullets = []   # new

run = True

while run:
    clock.tick(27)
    
    # to check only one bullet hits
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    for event in pygame.event.get():   # to check for all events (clicking mouse, etc)
        if event.type == pygame.QUIT:
            
            run = False
    
    # collision between man and goblin
    if goblin.visibility:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:  # to ensure the bullet is inside above the bottom of rectangle and below the top of rectangle
                if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:  # to ensure the bullet is inside from the left of rectangle and right of rectangle

                    man.hit(window)
                    score -= 1
    else:
        score = 0
        
   
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        
        else:
            facing = 1
            
        if len(bullets) <= 5:
            bullets.append(projectile(round(man.x+man.width//2), round(man.y+man.height//2), 6, (0,0,0), facing))
           
            shootLoop = 1
    
    # collision between goblin and bullet
    for bullet in bullets: # new
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:  # to ensure the bullet is inside above the bottom of rectangle and below the top of rectangle
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:  # to ensure the bullet is inside from the left of rectangle and right of rectangle
                
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))     
        
        if bullet.x > 0 and bullet.x < 500:
            bullet.x += bullet.vel
            
        else:
            bullets.pop(bullets.index(bullet))
    
    
    if keys[pygame.K_LEFT] and man.x > man.vel:   # making sure the top left position of our character is greater than velocity
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False    # new
        
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel: #making sure top right corner of our char is less than screen width-char width
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
        
    else:
        man.left = False
        man.right = False
        man.walkCount = 0
        man.standing = True
        
        
    if not(man.isJump):  # checks if user is not jumping
        
         if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
        
    else:                          
        if man.jumpCount >= -10:
            neg = 1
            
            if man.jumpCount < 0:
                neg = -1
                
            man.y -= (man.jumpCount ** 2) * 0.5 * neg    # quadratic eqn, try to understand it. 
            man.jumpCount -= 1
            
        else :
            man.isJump = False
            man.jumpCount = 10
            

    redraw_window()
    
    
pygame.quit()