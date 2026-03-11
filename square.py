from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
import numpy as np

# Window size
width = 600
height = 600

# Square properties
rect_x = -1.0
rect_y = 0.0
rect_size = 0.2
speed = 0.01

# Frame storage
frames = []
frame_count = 0
max_frames = 120   # about 2 seconds animation

def init():
    glClearColor(0,0,0,1)
    gluOrtho2D(-1,1,-1,1)

def capture_frame():
    global frame_count
    
    data = glReadPixels(0,0,width,height,GL_RGB,GL_UNSIGNED_BYTE)
    frame = np.frombuffer(data,dtype=np.uint8).reshape(height,width,3)
    frame = np.flip(frame,0)
    
    image = Image.fromarray(frame)
    frames.append(image)
    
    frame_count += 1

def draw():
    global rect_x
    
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0,0.7,1.0)

    glBegin(GL_QUADS)
    glVertex2f(rect_x, rect_y-rect_size)
    glVertex2f(rect_x+rect_size, rect_y-rect_size)
    glVertex2f(rect_x+rect_size, rect_y+rect_size)
    glVertex2f(rect_x, rect_y+rect_size)
    glEnd()

    capture_frame()

    glutSwapBuffers()

def update(value):
    global rect_x
    
    rect_x += speed
    
    if rect_x > 1.0:
        rect_x = -1.0 - rect_size

    if frame_count >= max_frames:
        print("Saving GIF...")
        frames[0].save(
            "animation.gif",
            save_all=True,
            append_images=frames[1:],
            duration=16,
            loop=0
        )
        print("GIF saved as animation.gif")
        glutLeaveMainLoop()
        return

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width,height)
    glutCreateWindow(b"OpenGL GIF Animation")

    init()

    glutDisplayFunc(draw)
    glutTimerFunc(0, update, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
