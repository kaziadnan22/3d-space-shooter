from OpenGL.GL import *   #DONE
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_TIMES_ROMAN_24
import time
import random
import math


# Game flags
x_r,y_r,z_r = False,False,False
start_game = False
pause = False
game_control = False
end =False
wlc = True
over = False
fpview = False
scaling  = True
scaling2 = True
sheild = False
Bomb  = False
bonus_pos = None       
cube = False 

invisible = False  #Invisible function #DONE
invisible_on = 0

#arrays
enim = []
bullets = []
bombarr = []
e_bullets = []


#variables
time_1 = time.time()
time_2 = time_1
sheild_on = 0 
camera_pos = (0,5, 500)
fovY = 120  
p_x,p_y, p_z= 0, 0, 0
angle  = 0
bonus_s_time = 0   
bonus_e_time = 0 
Grid_leng= 90 #Done
enemy = 7
e_bullet_time = time.time()    
e_bullet_interval = 3.0              
e_bullet_speed = 0.5               

#game variables
life_r = 10
bullet_r = 40
score = 0
bomb_r = 10


def About_Space(): #Done
    global Grid_leng
    for k in range(10):
        Y_begin =  Grid_leng* 5 - k* Grid_leng
        for l in range(10):
            X_begin= Grid_leng *5 - l *Grid_leng
            glBegin(GL_QUADS)
            glColor3f(1,1, 1 )

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

    
    Text_Drawing(450 ,  280, "Press /m\ to go to the main menu", GLUT_BITMAP_TIMES_ROMAN_24)


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
    glColor3f( 1,1, 1 ) 
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
    global over, p_x,p_y, p_z,angle,x_r,y_r,z_r,scaling,sheild,invisible, invisible_on

    if (invisible):
        return
    
    glPushMatrix()
    glTranslatef(p_x, p_y, p_z)

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
         
    if (sheild):
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
    global p_x, p_y    #Done need to update the variables
    dx = p_x -x
    dy = p_y- y
    angle = math.atan2(dy , dx ) 
    angle_degrees = math.degrees(angle )
    return angle_degrees -90



def Creating_The_Enemies(e): #Done
    global scaling, p_x, p_y, p_z 
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
    enim.append(Enemies_Random_Position_Making())

def Bullets_Drawing(): #Done
    glColor3f(1, 0.5, 1)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet[0], bullet[1], bullet[2])
        glutSolidCube(10)
        glPopMatrix()


def Bomb_Drawing(): #DONE 
    glColor3f(0, 0, 1)  # blue
    for bombs in bombarr: 
        glPushMatrix()
        glTranslatef(bombs[0], bombs[1], bombs[2])
        glutSolidCube(20)
        glPopMatrix()

#bonus 
def Bonus_Drawing(): #Done
    global cube, bonus_pos
    if cube and bonus_pos:
        glPushMatrix()
        glColor3f(1, 0, 0)  
        glTranslatef(bonus_pos[0], bonus_pos[1], bonus_pos[2])
        glutSolidCube(40)
        glPopMatrix()




def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1200, 900) #Done
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"3D Space Shooting Game ") #dONE 
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()
    

if __name__ == "__main__":
    main()
