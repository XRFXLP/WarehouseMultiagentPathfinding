from os import system 
from time import sleep
from itertools import product
from copy import deepcopy
from helper import main, table, blocks
def setup():
    size(700, 700)
    background(255)
    # for i in range(0, 700, 50):
    #     for j in range(0, 700, 50):
    #         rect(i, j, 50, 50)


        
Q = main(table, 14, 14, blocks)
visited = set()
def draw():
    background(255)
    # for i in range(0, 700, 50):
    #     for j in range(0, 700, 50):
    #         fill(255)
    #         rect(i, j, 50, 50)
    for i, j in blocks:
        fill(110)
        rect(i*50, j*50, 50, 50)
    
    for p in table:
        z = [('END', (255, 0, 0)),      #E
             ('PICK', (0, 255, 0)),      #P
             ('DEP', (0, 0,  255))]     #D
        for (t,q), r in zip(z, p[1:]):
            if r in visited:
                continue
            fill(*q)
            rect(r[0]*50, r[1]*50, 50, 50)
            fill(0)
            stroke(0)
            text(t, r[0]*50 + 10, r[1]*50 + 25)

            
    if not Q:
        noLoop()
        return
    a = Q.pop(0)
    for i, j in a:
        fill(0)
        ellipse(50*i + 25, 50*j + 25, 40, 10)
        fill(255)
        ellipse(50*i + 32, 50 * j + 25, 5, 5)
        ellipse(50*i + 18, 50 * j + 25, 5, 5)
        visited.add((i, j))
    sleep(0.1)
