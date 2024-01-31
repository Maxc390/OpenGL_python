#MAXWELL CHANZU
#SCT211-0722/2021

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
glutInit()
#Draw line with Midpoint Line Drawing Algorithm
def draw_line(x1, y1, x2, y2):
    # Calculate the differences between the coordinates
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Check if the line is steep (slope > 1)
    slope = dy > dx

    # If the line is steep, swap x and y coordinates
    if slope:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Ensure x1 is always less than x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    # Recalculate differences after potential swaps
    dx = x2 - x1
    dy = abs(y2 - y1)

    # Initial decision parameter for the algorithm
    decision = 2 * dy - dx
    y = y1

    # Start drawing points using OpenGL
    glBegin(GL_POINTS)
    
    # Iterate through each x-coordinate from x1 to x2
    for x in range(x1, x2 + 1):
        # Plot the point with potential swapping based on the slope
        plot_point(x if not slope else y, y if not slope else x)
        

        # Update the decision parameter and y-coordinate
        if decision >= 0:
            y += 1 if y1 < y2 else -1
            decision -= 2 * dx
        decision += 2 * dy
        
    # End drawing points
    glEnd()

#define plot point 
def plot_point(x, y):
    glColor3f(1, 1, 1)  # Set color to white
    glVertex2f(x, y)
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

#Draw Cartesian Plane
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
    pygame.display.set_caption("MidPoint LineDrawing Algorithm")
    glOrtho(-10, 10, -10, 10, -1, 1)  # Set scale
    #Size of pointpixels
    glPointSize(2)

    x1, y1 = 0, 2
    x2, y2 = -5, 4

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_axes()
        draw_numbers(-10,-10,10,10)
        draw_line(x1, y1, x2, y2)
        
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()

