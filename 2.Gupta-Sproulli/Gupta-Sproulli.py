import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
glutInit()
def clip_line(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    def get_region(x, y):
        region = 0
        if x < xmin:
            region |= 1  # left
        elif x > xmax:
            region |= 2  # right
        if y < ymin:
            region |= 4  # bottom
        elif y > ymax:
            region |= 8  # top
        return region

    # Get region codes for the two endpoints
    region_code0 = get_region(x0, y0)
    region_code1 = get_region(x1, y1)

    while True:
        # Both points inside the window, accept the line
        if not (region_code0 | region_code1):
            return x0, y0, x1, y1

        # Both points outside the same side, reject the line
        if region_code0 & region_code1:
            return None

        # Pick the outside point and calculate intersection with the window
        if region_code0:
            x, y = x0, y0
            region_code = region_code0
        else:
            x, y = x1, y1
            region_code = region_code1

        # Calculate intersection with the window
        if region_code & 1:  # left
            x = xmin
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
        elif region_code & 2:  # right
            x = xmax
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
        elif region_code & 4:  # bottom
            y = ymin
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
        elif region_code & 8:  # top
            y = ymax
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)

        # Update the outside point and its region code
        if region_code == region_code0:
            x0, y0 = x, y
            region_code0 = get_region(x0, y0)
        else:
            x1, y1 = x, y
            region_code1 = get_region(x1, y1)


def draw_line(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    # Clip the line using the Gupta-Sproull algorithm
    clipped_line = clip_line(x0, y0, x1, y1, xmin, ymin, xmax, ymax)
    
    # If the line is entirely outside the window, clipped_line will be None
    if clipped_line:
        # Update the line endpoints with the clipped values
        x0, y0, x1, y1 = clipped_line

    # Begin drawing the line using OpenGL
    glBegin(GL_LINES)
    
    # Specify the two endpoints of the line
    glVertex2f(x0, y0)
    glVertex2f(x1, y1)
    
    # End the drawing
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

#Define Cartesian Plane
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
    #initialise pygame and set dimensions for display window
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Gupta-Sproulli Algorithm")
    glOrtho(-10, 10, -10, 10, -1, 1)  # Set orthographic projection

    glPointSize(2)

    x0, y0 = 4, 3
    x1, y1 = 12, -5

    xmin, ymin, xmax, ymax = -5, -5, 5, 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #Draw axes and line
        draw_axes()
        draw_line(x0, y0, x1, y1, xmin, ymin, xmax, ymax)
        draw_numbers(-10,-10,10,10)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
