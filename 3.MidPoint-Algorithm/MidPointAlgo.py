#Maxwell Chanzu
#SCT211-0722/2021
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math
glutInit()
#Plot points for circle
def plot_circle_points(xc, yc, x, y):
    glVertex2f(xc + x, yc + y)
    glVertex2f(xc - x, yc + y)
    glVertex2f(xc + x, yc - y)
    glVertex2f(xc - x, yc - y)
    glVertex2f(xc + y, yc + x)
    glVertex2f(xc - y, yc + x)
    glVertex2f(xc + y, yc - x)
    glVertex2f(xc - y, yc - x)
#Draw Circle with Midpoint Algorithm
def draw_circle(xc, yc, radius):
    # Initialize the starting point on the circle
    x, y = radius, 0
    
    # Initial decision parameter
    p = 1 - radius

    # Start drawing points using OpenGL
    glBegin(GL_POINTS)

    # Iterate until the x-coordinate becomes less than or equal to y-coordinate
    while x > y:
        # Plot points for the current circle using symmetry
        plot_circle_points(xc, yc, x, y)

        # Update coordinates and decision parameter based on the algorithm rules
        if p <= 0:
            y += 1
            p += 2*y + 1
        else:
            x -= 1
            y += 1
            p += 2*(y - x) + 1

    # End drawing points
    glEnd()
def draw_numbers(xmin, ymin, xmax, ymax):
    glColor3f(1, 1, 1)  # Set color to white

    # Draw numbers on the X-axis
    for i in range(int(xmin), int(xmax) + 1):
        render_text(str(i), i, -0.5)

    # Draw numbers on the Y-axis
    for i in range(int(ymin), int(ymax) + 1):
        render_text(str(i), -0.5, i)

def render_text(text, x, y):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

#Draw line from starting point to ending point
def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()
#Draw Axes for Cartesian Plane
def draw_axes():
    glColor3f(1, 1, 1)  # Set color to white
    glBegin(GL_LINES)
    glVertex2f(-10, 0)
    glVertex2f(10, 0)
    glVertex2f(0, -10)
    glVertex2f(0, 10)
    glEnd()
#Main function
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("MidPoint Algorithm")
    
    glOrtho(-10, 10, -10, 10, -1, 1)  # Set orthographic projection

    glPointSize(2)

    xc, yc = 0, 0
    radius = 5

    x1, y1 = -4, 3
    x2, y2 = 5, -2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_axes()
        draw_numbers(-10,-10,10,10)
        draw_circle(xc, yc, radius)
        draw_line(x1, y1, x2, y2)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()


