import pygame
import time


class mygame:
    def __init__(self):
        pygame.init()

        size = width, height = 800, 800

        screen = pygame.display.set_mode(size)
        self.screen = screen
        #    screen.fill((145, 62, 228))

    def flash(self):
        color = (255, 255, 255)
        for i in range(8):
            if i % 2 == 0:
                fix = 100
            else:
                fix = 0
            for j in range(4):
                pygame.draw.rect(self.screen, color,
                                 pygame.Rect(i*100, j*200 + fix, 100, 100))

    def draw_point(self, path):
        for point in path:
            print('mypoint', point)
            pygame.draw.circle(self.screen, (255/2,
                                             255/2,
                                             255),
                               (50+100*point[0], 50+100*point[1]), 50)
        pygame.display.update()
        if len(mypath) == 49:
            print(mypath)
            exit()


game = mygame()
mypath = [(1, 4)]


def get_possible_point(mypath, current):
    x = current[0]
    y = current[1]
    v = (1, 2)
    poss = []
    final = []
    for var in range(2):
        for var2 in (1, -1):
            for var3 in (1, -1):
                poss.append((x + var2*v[var], y + var3*abs(v[var-1])))
    for point in poss:
        if point not in mypath and point[0] >= 0 and point[0] <= 6\
           and point[1] >= 0 and point[1] <= 6:
            final.append(point)
    return final


def visite(point, mypath):
    pygame.event.get()
    possible_point = get_possible_point(mypath, point)
    print(mypath[-1])
    if not possible_point:
        game.flash()
        mypath.pop()
        game.draw_point(mypath)
        return mypath
    else:
        for pt in possible_point:
            mypath.append(pt)
            game.flash()
            game.draw_point(mypath)
            mypath = visite(pt, mypath)
        mypath.pop()
        return mypath
#       game.flash()
#       mypath.pop()
#       game.draw_point(mypath)
#        return mypath


visite(mypath[0], mypath)
print(mypath)
