from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_TIMES_ROMAN_24
import time
import random
import math


##############
# Game flags #
##############
x_r, y_r, z_r = False, False, False
game_start = False
pause = False
game_control = False
end =False
welcome = True
game_over = False
fpov = False
scaling  = True
scaling2 = True # scaling of stars
shield = False
Bomb  = False
bonus_position = None       
bonus_cube = False 

is_invisible = False
invisible_start_time = 0


##########
# arrays #
##########
enemy_list = []
bullets = []
bomb_arr = []
enemy_bullets = []


#############
# variables #
#############
time_1 = time.time()
time_2 = time_1
shield_start_time = 0 
camera_position = (0,5, 500)
fovY = 120  
player_x,player_y, player_z= 0, 0, 0
angle = 0
bonus_start_time = 0   
bonus_end_time = 0 
Grid_leng= 90 #Done
enemy = 5
enemy_bullet_time = time.time()    
enemy_bullet_interval = 3.0              
enemy_bullet_speed = 0.5               


##################
# game variables #
##################
player_remaining_life = 10
remaining_bullet = 40
score = 0
remaining_bomb = 10




###########################
# Function implementation #
###########################

def About_Space(): #Done
    global Grid_leng
    for k in range(10):
        Y_begin =  Grid_leng* 5 - k* Grid_leng
        for l in range(10):
            X_begin= Grid_leng *5 - l *Grid_leng
            glBegin(GL_QUADS)
            glColor3f(1, 1, 1)

            glVertex3f( X_begin, Y_begin,0)
            glVertex3f(X_begin -Grid_leng, Y_begin, 0 )
            glVertex3f( X_begin- Grid_leng, Y_begin- Grid_leng, 0)
            glVertex3f(X_begin, Y_begin -Grid_leng, 0 )
            glEnd()


def Star_Implementing_for_Space(): #DONE
    global scaling2
    for x in range (-600, 601,200): 
        for y in range ( -600, 601, 200): 
            if not scaling2: #Scaling here is for twinkling eeffectt
                glPointSize(2)
                glColor3f(0,0, 0 ) 
            else:
                glPointSize(3.5 )
                glColor3f(1, 1,1 ) 
                 
            glBegin(GL_POINTS)
            glVertex3f( x , y ,2 ) 
            glEnd()

def Border_of_Space(): #Done
    global Grid_leng
    ht = 7

    glBegin(GL_QUADS)

    glColor3f(1, 1, 1)
    glVertex3f(540, -540, 0)
    glVertex3f(540,  540, 0)
    glVertex3f(540,  540, ht)
    glVertex3f(540, -540, ht)

    glColor3f(1, 1, 1)
    glVertex3f(-540, -540, 0)
    glVertex3f(-540,  540, 0)
    glVertex3f(-540,  540, ht)
    glVertex3f(-540, -540, ht)

    glColor3f(1, 1, 1)
    glVertex3f(-540, 540, 0)
    glVertex3f( 540, 540, 0)
    glVertex3f( 540, 540, ht)
    glVertex3f(-540, 540, ht)

    glColor3f(1, 1, 1)
    glVertex3f(-540, -540, 0)
    glVertex3f( 540, -540, 0)
    glVertex3f( 540, -540, ht)
    glVertex3f(-540, -540, ht)

    glEnd()


def Text_Drawing(x,y, text,font= GLUT_BITMAP_TIMES_ROMAN_24):  #Done
    glColor3f(1, 0,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0,1290 ,0, 725) 
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y )
    for charac in text:
        glutBitmapCharacter(font,ord(charac))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)

    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def Controlling_Directory(): #Done

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0,1290 ,0, 725)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    Text_Drawing(440 ,  600, "[ Game Control Directory ]", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  580, "a - Left", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  560, "d - Right", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  540, "w - Up", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  520, "s - Down", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  500, "h - Shield Activation", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  480, "Mouse left - Fire the bullet", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  460, "Mouse Right - Bomb Throwing", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  440, "f - First Person View", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  420, "x - rotate in x axis", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  400, "y - rotate in y axis", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  380, "l - load extra bullet", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  360, "z - rotate in z axis", GLUT_BITMAP_TIMES_ROMAN_24)
    Text_Drawing(500 ,  340, "i - Invisible", GLUT_BITMAP_TIMES_ROMAN_24)
    
    Text_Drawing(450 ,  280, "Press (m) to go to the main menu", GLUT_BITMAP_TIMES_ROMAN_24)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def Begin_The_Game(): #Done

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0,1290 ,0, 725)
  
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    Box_X, Box_Y = 520 , 380 #horizontal and vertical position 
    Box_Width, Box_Height =320 , 65
    glColor3f( 1, 1, 1) 
    glLineWidth(3.5)
    glBegin(GL_LINES)
    glVertex2f(Box_X, Box_Y )
    glVertex2f( Box_X +Box_Width,Box_Y )
    glVertex2f(Box_X+ Box_Width, Box_Y +Box_Height )
    glVertex2f( Box_X, Box_Y +Box_Height )
    glVertex2f(Box_X, Box_Y )
    glVertex2f( Box_X, Box_Y+ Box_Height )
    glVertex2f( Box_X +Box_Width, Box_Y )
    glVertex2f( Box_X + Box_Width,Box_Y + Box_Height )
    glEnd()

    Text_Drawing(Box_X +100, Box_Y +25,"Start The Game", GLUT_BITMAP_TIMES_ROMAN_24 )
    Text_Drawing(Box_X +15 , Box_Y - 25, "Welcome to Space Shooting Game!", GLUT_BITMAP_TIMES_ROMAN_24 )
    Text_Drawing(Box_X+ 105, Box_Y-50,"Press [g] to Start", GLUT_BITMAP_TIMES_ROMAN_24 )
    Text_Drawing(Box_X +65, Box_Y - 80, "Press [c] to see the Controls", GLUT_BITMAP_TIMES_ROMAN_24 )
    Text_Drawing(Box_X+ 75, Box_Y -200,  "Press [q] to Quit Game", GLUT_BITMAP_TIMES_ROMAN_24 )

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def SpaceShip_For_Fighters(): #Done
    global game_over, player_x,player_y, player_z,angle,x_r,y_r,z_r,scaling,shield,is_invisible, invisible_start_time

    if (is_invisible):
        return
    
    glPushMatrix()
    glTranslatef(player_x, player_y, player_z)

    if x_r:
        glRotatef(angle, 1, 0, 0)
    elif z_r:
        glRotatef(angle, 0, 1, 0)
    else:
        glRotatef(angle, 0, 0, 1)


    if not (scaling):
        glScalef (.8, .8, 1)
    else:
        glScalef (.9, .9, 1)
         
    if (shield):
        gluSphere(gluNewQuadric(), 100, 21, 21)


    # Body Of The spaceShip
    glPushMatrix()
    glColor3f(1,0, 0 )
    glScalef (1.2, 1.2, .6 )
    glutSolidCube(65)
    glPopMatrix()

    glPushMatrix()  #Black body
    glColor3f(0.2, 0.2, 0.2 )
    glScalef (1.1, 1.4,.6 )
    glutSolidCube(28)
    glPopMatrix()  


    glPushMatrix()
    glTranslatef(-44, 6, 6)
    glRotatef(-90, 1,0, 0)
    glColor3f(0, 1, 0) 
    gluCylinder(gluNewQuadric(), 12, 14, 58, 12, 12)
    glPopMatrix()


    glPushMatrix()  
    glTranslatef(44, 6,6 )
    glRotatef(-90, 1, 0,0)
    glColor3f(0, 1, 0)
    gluCylinder(gluNewQuadric(), 12, 14, 58, 12, 12)
    glPopMatrix()

    glPushMatrix()  #Nose
    glTranslatef(0, -95, 5)
    glRotatef(-90,1, 0, 0)
    glColor3f(1, 0.9,1)
    gluCylinder(gluNewQuadric(), 4, 14, 58, 12, 12)
    glPopMatrix()

    glPopMatrix()



def Rotation_Angle_For_Enemy(x ,y ):   #DONE Direction Vector from an Enemy to Player
    global player_x, player_y    #Done need to update the variables
    dx = player_x -x
    dy = player_y- y
    angle = math.atan2(dy , dx ) 
    angle_degrees = math.degrees(angle )
    return angle_degrees -90



def Creating_The_Enemies(e): #Done
    global scaling, player_x, player_y, player_z 
    x,y,z = e[0],e[1],e[2]

    ang = Rotation_Angle_For_Enemy(x,y)

    glPushMatrix()
    glTranslatef(x, y, z)

    if not scaling: 
        glScalef (.9, .9, .9)
         
    else:
        glScalef (1.0 , 1.0, 1.0)
         
    glRotatef(ang,0,0,1)

    glColor3f(1, .8, .6) #color_body
    glTranslatef(0, 0, 0)
    glutSolidCube(40)
    
    #Canon 
    glColor3f(1,0,1)
    glTranslatef(0, 0, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 12, 4, 44, 12, 12)
    glPopMatrix()

def Enemies_Random_Position_Making(): #DONE
    global Grid_leng,enemy
    min = int(12*Grid_leng /2) #to check if pos crosses boundary
    while True:
        x, y = random.randint (-(min-55),(min-55)),-500
        if abs(x) >150 or abs(y)> 150 : 
            break
    return [x, y, 0,2 ]

#Assigning X and Y Pos of Enemies
for k in range(enemy):
    enemy_list.append(Enemies_Random_Position_Making())

def Bullets_Drawing(): #Done
    glColor3f(1, 0.5, 1)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet[0], bullet[1], bullet[2])
        glutSolidCube(10)
        glPopMatrix()


def Bomb_Drawing(): #DONE 
    glColor3f(0, 0, 1)  # blue
    for bombs in bomb_arr: 
        glPushMatrix()
        glTranslatef(bombs[0], bombs[1], bombs[2])
        glutSolidCube(20)
        glPopMatrix()

#bonus 
def Bonus_Drawing(): #Done
    global bonus_cube, bonus_position
    if bonus_cube and bonus_position:
        glPushMatrix()
        glColor3f(1, 0, 0)  
        glTranslatef(bonus_position[0], bonus_position[1], bonus_position[2])
        glutSolidCube(40)
        glPopMatrix()


def Draw_Enemy_Bullets(): #Done
    glColor3f(1.0, 0.5, 0.0)
    for i in enemy_bullets:
        glPushMatrix()
        glTranslatef(i[0], i[1],i[2])
        glutSolidSphere(5, 10, 10)
        glPopMatrix()


def Generate_Random_Bonus_Shape():  #Done
    global bonus_position, bonus_start_time, bonus_cube, bonus_end_time

    current_time = time.time()
    if ((not bonus_cube) and (current_time - bonus_start_time >= 20)): # generate bonus after 20 seconds
        bonus_position = [random.randint(-50, 50), random.randint(-50, 500), 0]
        bonus_cube = True
        bonus_start_time = current_time
        bonus_end_time = current_time

    if ((bonus_cube) and (current_time - bonus_end_time >= 10)):    # visibility of bonus cube = 10 seconds
        bonus_cube = False
        bonus_position = None


def Collect_Bonus():    #Done
    global bonus_cube, bonus_position, remaining_bomb, player_remaining_life, remaining_bullet

    if (bonus_cube and bonus_position):
        if ((abs(player_x - bonus_position[0]) < 35) and (abs(player_y - bonus_position[1]) < 35)):
            remaining_bomb = 25
            player_remaining_life = 12
            remaining_bullet = 50
            print('Bonus Collected!')
            bonus_cube = False
            bonus_position = None


def Invisible_Mode(): #Done
    global is_invisible, invisible_start_time
    is_invisible = True
    invisible_start_time = time.time()
    print("Invisibility Activated")



#assign enemy bullets direction
def Enemy_Bullet_Firing(enemy_x, enemy_y, enemy_z): #Done
    global player_x, player_y, player_z, enemy_bullets, game_over
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    dz = player_z - enemy_z
    length = math.sqrt(dx**2 + dy**2 + dz**2)   # Euclidean distance
    if (length == 0):
        return
    dx /= length
    dy /= length
    dz /= length
    bullet = [enemy_x, enemy_y,enemy_z,dx,dy,dz]
    enemy_bullets.append(bullet)


def Player_Bullet_Firing(): #Done
    global bullets, remaining_bullet, game_over, player_remaining_life, shield, pause
    for bullet_pos in bullets:
        bullet_pos[0] = bullet_pos[0] + bullet_pos[3] * 5
        bullet_pos[1] = bullet_pos[1] + bullet_pos[4] * 5
        bullet_pos[3] = bullet_pos[3] + bullet_pos[5] * 5
    if (shield):    # If shield is enabled, bullet count reduces, but doesn't hurt enemy or player itself
        pos = 100
    else:
        pos = 540
    bullet_remains = 0
    while (bullet_remains < len(bullets)):
        pos_x, pos_y = bullets[bullet_remains][0], bullets[bullet_remains][1]
        if ((abs(pos_x) >= pos) or (abs(pos_y) >= pos)):
            bullets.pop(bullet_remains)
            if (pause == False):
                remaining_bullet -= 1   
        else:
            bullet_remains += 1

    if (player_remaining_life == 0):
        game_over = True
        enemy_list.clear()


def Ship_Collision():   # Done
    global bullets, game_over, player_y, player_x, score, player_remaining_life, remaining_bullet, shield, is_invisible, invisible_start_time
    for y in enemy_list:
        dx = player_x - y[0]
        dy = player_y - y[1]
        distance = math.sqrt(dx**2 + dy**2) # calculating enemy distance using Eucledian distance formula

        if (distance > 1):
            y[1] += (dy / distance) * 0.1

    if (not game_over):
        for y in enemy_list:
            if (abs(player_x - y[0]) < 100 and abs(player_y - y[1]) < 100):
                if (player_remaining_life > 0):
                    if (shield == False):
                        player_remaining_life = player_remaining_life - 1
                    else:
                        score = score + 1
                    enemy_list.remove(y)
                    enemy_list.append(Enemies_Random_Position_Making()) # enemy respawn as soon as one enemy dies
                else:
                    game_over = True
                    enemy_list.clear()
            break
    if (is_invisible):
        return



def Destroy_Enemy_Ship():   # Done
    global bullets, score, enemy_list, player_remaining_life, game_over

    a = [] # bullets to be removed
    b = [] # updated enemies

    for y in enemy_list:
        is_bullet_fired = False
        for t in bullets:
            bx, by = t[0], t[1] # bullet position
            ex, ey = y[0], y[1] # enemy position
            if (abs(bx - ex) < 30 and abs(by - ey) < 30):   # detect collision
                if (y[3] == 0): # enemy health: 3 hit to destroy an enemy ship
                    is_bullet_fired = True
                    score = score + 1
                    a.append(t)
                    break
                else:
                    y[3] -= 1
                    a.append(t)

        if (is_bullet_fired == True):
            b.append(Enemies_Random_Position_Making())  # enemy ship respawn
        else:
            b.append(y)

    for e in a:
        if (e in bullets):
            bullets.remove(e)   # remove the used bullets
    enemy_list[:] = b   # updating enemy list


def Bomb_Shooting():    # Done
    global bomb_arr, enemy_list, score
    for b in bomb_arr:
        b[0] += b[3] * 8    # bomb position along x-axis
        b[1] += b[4] * 8    # bomb position along y-axis
        b[2] += b[5] * 0.5  # bomb position along z-axis

    bomb_remaining = 0
    while (bomb_remaining < len(bomb_arr)):
        pos_x, pos_y = bomb_arr[bomb_remaining][0], bomb_arr[bomb_remaining][1]
        if (abs(pos_x) >= 540 or abs(pos_y) >= 540):
            bomb_arr.pop(bomb_remaining)
        else:
            bomb_remaining += 1

    temp_enemy_list = []    # new list for temporarily stroing 
    for e in enemy_list:
        hit = False
        for b in bomb_arr:
            if (abs(b[0] - e[0]) < 30 and abs(b[1] - e[1]) < 30):   # score increases if bomb hits enemy ship
                score += 1
                hit = True
                break
        if (not hit):
            temp_enemy_list.append(e)
        else:
            temp_enemy_list.append(Enemies_Random_Position_Making())
    enemy_list[:] = temp_enemy_list # remaining enemies' locations are appended in the previous enemy list


def Enemy_Bullet_Movement():   # Done
    global enemy_bullets, enemy_bullet_speed
    new_list = []
    # changing relative position of enemy's bullet with respect to the player's position
    for t in enemy_bullets:
        t[0] += t[3] * enemy_bullet_speed
        t[1] += t[4] * enemy_bullet_speed
        t[2] += t[5] * enemy_bullet_speed

        if (abs(t[0]) < 540 and abs(t[1]) < 540):   # removes the bullets that go outside the boundary
            new_list.append(t)
    enemy_bullets[:] = new_list # store the valid bullets


def Enemy_Bullet_Hits_Player(): # Done
    global enemy_bullets, player_x, player_y, player_remaining_life, shield, game_over
    for i in enemy_bullets[:]:
        dx = i[0] - player_x    # distance of bullet and player along x-axis
        dy = i[1] - player_y
        if (dx*dx + dy*dy) < (30 ** 2): # collision detection
            if (not shield):
                player_remaining_life = player_remaining_life -  1/3  # 3 hit = 1 life loss for player's remaining life
            enemy_bullets.remove(i)
            if (player_remaining_life <= 0):
                game_over = True
    if (is_invisible):
        return


def Keyboard_Listener(key, x, y):   # Done
    global welcome, game_start, game_over, x_r, y_r, z_r, fpov, shield, Bomb, game_control, is_invisible, invisible_start_time
    global player_x, player_y, angle, score, remaining_bullet, player_remaining_life, enemy, shield_start_time, pause,remaining_bomb

    if (pause == False):
        if (key == b'i' and not game_over):   
            if (not is_invisible):  # Toggle Invisibility mode
                Invisible_Mode()    

        if (key == b'w' and not game_over):
            if (player_y > -480):
                player_y -= 8
            
        elif (key == b's' and not game_over):
            if player_y < 480:
                player_y += 8
        
        elif (key == b'x' and not game_over):
            x_r = True
            angle += 6
            y_r, z_r = False, False

        elif (key == b'y' and not game_over):
            y_r = True
            angle += 6
            x_r, z_r = False, False

        elif (key == b'z' and not game_over):
            z_r = True
            angle += 6
            y_r, x_r = False, False

        elif (key == b'd' and not game_over):
            if (player_x > -500):
                player_x -= 8
        
        elif (key == b'a' and not game_over):
            if (player_x < 500):
                player_x += 8
        
        if (key == b'g' and welcome):
            welcome = False
            game_control = False
            game_start = True
            game_over = False
            bullets.clear()
            enemy_list.clear()

            for l in range(enemy):
                e = Enemies_Random_Position_Making()
                enemy_list.append(e)

            score = 0
            remaining_bullet = 40
            remaining_bomb = 20
            player_remaining_life = 10
            shield = False
            Bomb = False
            player_x, player_y = 0, 0
            angle = 0
            print("Game Begins!")
            glutPostRedisplay()

        if (key == b'c' and welcome):
            game_control = True
            welcome = False

        if (key == b'q' and welcome):
            print(f'Game Over! Score = {score}')
            glutLeaveMainLoop()
            
        if (key == b'm' and game_start == False):
            game_control = False
            welcome = True

        elif (key == b'm' and game_over == True):
            game_control = False
            welcome = True
            game_over = False
            game_start = False
            
        elif (key == b'f'):
            fpov = not (fpov)
            print('First Person View Is On')

        elif (key == b'h' and not game_over):
            if (not shield and score >= 3): # Score must be at least 3 to use shield
                shield_start_time = time.time()
                score -= 3  # Use shield for 3 scores
                shield = True
                print('Shield activated!')
            else:
                print('Age 3 ta re maira lo!')

        if (key == b'l' and not game_over): # load bullets using 2 scores
            if (remaining_bullet < 20):
                score -= 2
                remaining_bullet = 20
            else:
                print('Bullet is loaded already!')
        
        if (key == b'r'and game_over): #restart
            bullets.clear()
            enemy_list.clear()
            for l in range(enemy):
                e = Enemies_Random_Position_Making()
                enemy_list.append(e)
                
            score = 0
            remaining_bullet = 40
            player_remaining_life = 10
            remaining_bomb = 20
            game_over = False
            shield = False
            Bomb  = False
            print("Game restarted!")
                
            glutPostRedisplay()

    if (key == b' ' and not game_over): # press space to toggle between pause and playing game
            pause = not pause


def Special_Key_Listener(key, x, y):    # Done
    global camera_position, player_z, is_invisible, invisible_start_time
    x, y, z = camera_position
    if (key == GLUT_KEY_LEFT):  # keyboard left key to shrink player spaceship size
        if (player_z > -450):
            player_z -= 6
    elif (key == GLUT_KEY_RIGHT):   # keyboard left key to expand player spaceship size
        if (player_z < 450):
            player_z += 6
    elif (key == GLUT_KEY_UP):  # keyboard up key to change camera postition perspective
        if (y < 550):
            y += 6
    elif (key == GLUT_KEY_DOWN):  # keyboard down key to change camera postition perspective
        if (y > 5):
            y -= 5
    camera_position = (x, y, z)


def Mouse_Listener(button, state, x, y):    # Done
    global player_x, player_y, angle, bullets, game_over, Bomb, bomb_arr, remaining_bomb, pause

    if (button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over and pause == False):    # Firing "bullet" using mouse left key
            Bomb = False
            rad = math.radians(angle)
            dir_x = math.sin(rad)
            dir_y = -math.cos(rad)
            cannon_offset = 90  # bullet starts 90 units from the canon
            bx = player_x + cannon_offset * dir_x   # moves the bullet forward along the ship's facing direction along x-axis
            by = player_y + cannon_offset * dir_y   # moves the bullet forward along the ship's facing direction along y-axis
            bz = 10 
            bullets.append([bx, by, bz, dir_x, dir_y, 0])   # appends fired bullet's position into the 'bullets' array

    elif (button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not game_over):    # Firing "bomb" using mouse right key
            if (remaining_bomb > 0 and pause == False):
                Bomb = True
                remaining_bomb -= 1
                for y in enemy_list:
                    dx = y[0] - player_x - 10
                    dy = y[1] - player_y + 30
                    dz = y[2] - 5
                    dist = math.sqrt(dx**2 + dy**2+5**2)
                    if (dist == 0): 
                        continue
                    bomb_arr.append([player_x, player_y, 5, dx / dist, dy / dist, dz/dist]) # appends fired bomb's position into the 'bomb_arr' array
            else:
                print('No Bomb Remaining')

    glutPostRedisplay()


def setupCamera():  # Done
    global fpov, player_x, player_y

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if (fpov):
        camera_x = player_x
        camera_y = player_y + 20   
        camera_z = 70     

        look_x = player_x
        look_y = player_y
        look_z = 40

        gluLookAt(camera_x, camera_y, camera_z, look_x, look_y, look_z, 0, 0, 1)  
    else:
        x, y, z = camera_position
        gluLookAt(player_x, y, z, player_x, 0, 0, 0, 0, 1)


def Idle(): # Done
    global scaling, scaling2, time_1, time_2, shield, shield_start_time, Bomb, pause, enemy_bullet_interval, enemy_bullet_time, game_over, is_invisible, invisible_start_time

    if (pause == False and game_over == False):
        Ship_Collision()
        if (Bomb == False):
            Player_Bullet_Firing() 
        else:
            Bomb_Shooting()
        Destroy_Enemy_Ship()

        if (game_over == False):
            Generate_Random_Bonus_Shape()
            Collect_Bonus()

        cur_time = time.time()
        if (cur_time - enemy_bullet_time >= enemy_bullet_interval):
            for i in enemy_list:
                Enemy_Bullet_Firing(i[0], i[1], i[2])
            enemy_bullet_time = cur_time

        Enemy_Bullet_Movement()
        Enemy_Bullet_Hits_Player()

        ftime = time.time()
        if (ftime - time_1 >= .7):
            scaling = not scaling
            time_1 = ftime
        
        if (ftime - time_2 >= .4):
            scaling2 = not scaling2
            time_2 = ftime

        if (shield and (time.time() - shield_start_time >= 7)): # shield lasts for 7 seconds after activating
            shield = False

        if (is_invisible and (time.time() - invisible_start_time >= 5)):    # Invisibility lasts for 5 seconds
            is_invisible = False

    glutPostRedisplay()


def showScreen():   # Done
    global game_start, welcome, game_over, player_remaining_life, remaining_bullet, score, Bomb, remaining_bullet, pause

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glClearColor(.1,.2,.3,.5)	
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
      
    glViewport(0, 0, 1000, 800)
    setupCamera()
   
    if (welcome):
        Begin_The_Game()
    elif (game_control):
        Controlling_Directory()  
    else:
        Star_Implementing_for_Space()
        SpaceShip_For_Fighters()
        if (game_over == False):
            Bonus_Drawing()
            if (Bomb == False and remaining_bullet > 0):
                Bullets_Drawing()   # bullet firing
            else:
                Bomb_Drawing()
            for i in enemy_list:
                Creating_The_Enemies(i)
            Draw_Enemy_Bullets()
            Text_Drawing(10, 690, f"Remainig Life: {int(player_remaining_life)*'*'}", GLUT_BITMAP_TIMES_ROMAN_24)
            Text_Drawing(1110, 690, f"Score : {score} ", GLUT_BITMAP_TIMES_ROMAN_24)
            Text_Drawing(10, 670, f"Remainig Bullets: {max(remaining_bullet,0)} ", GLUT_BITMAP_TIMES_ROMAN_24)
            Text_Drawing(10, 650, f"Remainig Bombs: {remaining_bomb} ", GLUT_BITMAP_TIMES_ROMAN_24)
            if (pause):
                Text_Drawing(410, 650, f"Game Paused! Press 'Space' to resume.", GLUT_BITMAP_TIMES_ROMAN_24)

        else:
            Text_Drawing(450, 690, f"Khatam, Tata, Bye Bye! Score = {score}.",GLUT_BITMAP_TIMES_ROMAN_24)
            Text_Drawing(480, 660, f'Press <r> to Restart Game',GLUT_BITMAP_TIMES_ROMAN_24)
            Text_Drawing(490, 630, f'Press <m> to Quit Game',GLUT_BITMAP_TIMES_ROMAN_24)

    glutSwapBuffers()



############################
# Main entry point of game #
############################

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1200, 900)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"3D Space Shooting Game")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(Keyboard_Listener)
    glutSpecialFunc(Special_Key_Listener)
    glutMouseFunc(Mouse_Listener)
    glutIdleFunc(Idle)
    glutMainLoop()
    

if __name__ == "__main__":
    main()