#Maxwell Chanzu
#SCT211-0722/2021
import csv
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
glutInit()
#Draw line with DDA Line Drawing Algorithm
def draw_line(x1, y1, x2, y2):
    #Calculate Change in X and Y
    dx = x2 - x1
    dy = y2 - y1
    # Determine the number of steps needed
    steps = max(abs(dx), abs(dy))
    # Calculate the increments for each step
    x_increment = dx / steps
    y_increment = dy / steps
    # Initialize the starting point
    x, y = x1, y1
    #Store Points in Array
    points = []

    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_increment
        y += y_increment

    return points
#Functions to Draw the Plot point and Axes for Cartesian Plane
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

def draw_axes():
    glColor3f(1, 1, 1)  # Set color to white
    glBegin(GL_LINES)
    glVertex2f(-10, 0)
    glVertex2f(10, 0)
    glVertex2f(0, -10)
    glVertex2f(0, 10)
    glEnd()
#Save to output csv file
def save_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['X', 'Y'])  # Write header
        csv_writer.writerows(data)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("DDA Line Drawing Algorithm")
    glOrtho(-11, 11, -11, 11, -1, 1)  # Set orthographic projection to control scale
    #Size of Pixels
    glPointSize(2)
    #Starting Point(x1,y1) to Ending Point(x2,y2)
    x1, y1 = 5, 1
    x2, y2 = 10, 3
    #Draw line
    points = draw_line(x1, y1, x2, y2)
    #Coordinates.csv 
    save_to_csv('coordinates.csv', points)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_axes()
        draw_numbers(-10,-10,10,10)
        glBegin(GL_POINTS)
        for point in points:
            plot_point(*point)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()

