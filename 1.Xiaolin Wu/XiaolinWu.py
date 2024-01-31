#Maxwell Chanzu
#SCT211-0722/2021
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
glutInit()
class LineDrawer:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.calculate_line()

    def calculate_line(self):
        # Clear existing points
        self.points = []

        # Calculate differences and check for steepness
        dx = abs(self.x2 - self.x1)
        dy = abs(self.y2 - self.y1)
        steep = dy > dx

        # If steep, swap x and y coordinates
        if steep:
            self.x1, self.y1 = self.y1, self.x1
            self.x2, self.y2 = self.y2, self.x2

        # Ensure x1 is less than x2
        if self.x1 > self.x2:
            self.x1, self.x2 = self.x2, self.x1
            self.y1, self.y2 = self.y2, self.y1

        # Recalculate differences and gradient
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        gradient = dy / dx if dx != 0 else 1

        # Initialize variables for the first endpoint
        xend = round(self.x1)
        yend = self.y1 + gradient * (xend - self.x1)
        xgap = 1 - self.fractional_part(self.x1 + 0.5)
        xpxl1 = xend
        ypxl1 = int(yend)

        # Add the first two points for antialiasing
        self.add_point(xpxl1, ypxl1, 1 - self.fractional_part(yend) * xgap)
        self.add_point(xpxl1, ypxl1 + 1, self.fractional_part(yend) * xgap)

        intery = yend + gradient

        # Initialize variables for the second endpoint
        xend = round(self.x2)
        yend = self.y2 + gradient * (xend - self.x2)
        xgap = self.fractional_part(self.x2 + 0.5)
        xpxl2 = xend
        ypxl2 = int(yend)

        # Add the next two points for antialiasing
        self.add_point(xpxl2, ypxl2, 1 - self.fractional_part(yend) * xgap)
        self.add_point(xpxl2, ypxl2 + 1, self.fractional_part(yend) * xgap)
    
        # Continue adding points along the line
        if steep:
            for x in range(int(xpxl1) + 1, int(xpxl2)):
                self.add_point(int(intery), x, 1 - self.fractional_part(intery))
                self.add_point(int(intery) + 1, x, self.fractional_part(intery))
                intery += gradient
        else:
            for x in range(int(xpxl1) + 1, int(xpxl2)):
                self.add_point(x, int(intery), 1 - self.fractional_part(intery))
                self.add_point(x, int(intery) + 1, self.fractional_part(intery))
                intery += gradient


    def add_point(self, x, y, brightness):
        brightness = max(0, min(brightness, 1))
        self.points.append((x, y, brightness))

    def fractional_part(self, value):
        return value - int(value)

    def draw(self):
        glColor3f(1, 1, 1)  # Set color to white
        glBegin(GL_POINTS)
        for x, y, brightness in self.points:
            glVertex2f(x, y)
        glEnd()

def draw_axes():
    glColor3f(1, 1, 1)  # Set color to white
    glBegin(GL_LINES)
    glVertex2f(-10, 0)
    glVertex2f(10, 0)
    glVertex2f(0, -10)
    glVertex2f(0, 10)
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

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Xiaolin Wu Algorithm")
    glOrtho(-10, 20, -20, 20, -1, 1)

    glPointSize(2)

    line_drawer = LineDrawer(9, 6, 14, 3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_axes()
        draw_numbers(-10,-10,10,10)
        line_drawer.draw()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()

