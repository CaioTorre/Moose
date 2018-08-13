import numpy as np
import imageio
import sys
import argvParser as parser

vb = parser.exists(sys.argv, '--verbose')

def log(msg):
    if vb: print(msg)

def tabb(n, msg):
    t = ''
    for i in range(n): t += '|'
    return t + msg

def translateDirection(x, y, d):
    if d == 0: return x, y-1
    if d == 1: return x+1, y
    if d == 2: return x, y+1
    return x-1, y
    
def handHolding(maze, cx, cy, d, ex, ey, tabbing):
    #if tabbing < 40:
    if maze[cy][cx]:
        log(tabb(tabbing, 'At ' + str(cx) + ',' + str(cy) + ' - d=' + str(d)))
        if cx == ex and cy == ey: 
            log(tabb(tabbing,'Arrived!'))
            return [[cx, cy]]
        
        td = (d + 1) % 4
        tx, ty = translateDirection(cx, cy, td)
        attempt = handHolding(maze, tx, ty, td, ex, ey, tabbing + 1)
        if attempt: 
            attempt.append([cx, cy])
            return attempt
            
        log(tabb(tabbing, 'Turning right failed...'))
        tx, ty = translateDirection(cx, cy, d)
        attempt = handHolding(maze, tx, ty, d, ex, ey, tabbing + 1)
        if attempt:
            attempt.append([cx, cy])
            return attempt
            
        log(tabb(tabbing, 'Going straight failed...'))
        td = (d - 1) % 4
        tx, ty = translateDirection(cx, cy, td)
        attempt = handHolding(maze, tx, ty, td, ex, ey, tabbing + 1)
        if attempt:
            attempt.append([cx, cy])
            return attempt
        
        log(tabb(tabbing, 'Dead end!'))
        return None
    log(tabb(tabbing,'Hit a wall!'))
    return None

def findStartAndEnd(maze)
    mazeX = maze.shape[0]
    mazeY = maze.shape[1]

    xs = 0
    ys = 0

    dc = 0
    while xs < maze.shape[0] and not maze[ys][xs]: log('XS=' + str(xs) + ' - col=' + str(maze[xs][ys])); xs +=1 
    if xs >= maze.shape[0]: #Not on top
        log('Starting point was not on top...')
        #xs = maze.shape[0]
        xs -= 1
        while ys < maze.shape[1] and not maze[ys][xs]: ys +=1
        if ys >= maze.shape[1]: #Not on right side either
            log('Starting point was not on right...')
            ys -= 1
            while xs >= 0 and not maze[ys][xs]: xs -=1
            if xs <= 0: #Not on bottom either
                while ys >= 0 and not maze[ys][xs]: ys -=1
                if ys <= 0:
                    log('Couldnt find starting point!')
                    exit()
                else: #Starting point was on left side
                    dc = 3
            else: #Starting point was on bottom
                dc = 2
        else: #Starting point was on right side
            dc = 1
    else: #Starting point was on top
        dc = 0

    entry_d = (dc + 1) % 4
    log('Found starting = ' + str(xs) + ',' + str(ys) + '; d=' + ['top','right','bottom','left'][dc])
    xe, ye = xs, ys    

    if dc == 0:
        xe += 1
        while xe < maze.shape[0] and not maze[ye][xe]: xe += 1
        if xe <= maze.shape[0] - 1: dc = -1#Found on top
        else: dc = 1; xe -= 1
    if dc == 1:
        ye += 1
        while ye < maze.shape[1] and not maze[ye][xe]: ye += 1
        if ye <= maze.shape[1] - 1: dc = -1
        else: dc = 2; ye -= 1
    if dc == 2:
        xe -= 1
        while xe >= 0 and not maze[ye][xe]: xe -= 1
        if xe > 0: dc = -1
        else: dc = 3
    if dc == 3:
        ye -= 1
        while ye >= 0 and not maze[ye][xe]: ye -= 1
        if ye > 1 - 1: dc = -1
        else: dc = 4
    if dc == 4:
        log('Couldnt find exit point!')
        exit()
        
    log('Found ending = ' + str(xe) + ',' + str(ye))
    return xs, ys, entry_d, xe, ye
    
#xe = 60
#ye = 67

xs, ys, entry_d, xe, ye = findStartAndEnd
path = handHolding(maze,xs,ys,entry_d,xe,ye,0)
img_out = np.zeros([mazeX,mazeY,4])
img_out[:,:,3] = 255
log('Drawing path... ' + str(mazeX) + 'x' + str(mazeY))
for x in range(mazeX):
    for y in range(mazeY):
        if maze[x][y]:
            img_out[x,y,0:3] = 255
        else:
            img_out[x,y,0:3] = 0
log('Created base...')

r = 255
b = 0
step = max(255 / len(path),0)
log('Found step='+str(step))        
for pos in path:
    log('Colouring ' + repr(pos) + ' - r=' + str(r))
    img_out[pos[1],pos[0],0] = r
    img_out[pos[1],pos[0],2] = b
    if r > 1:
        r -= step
        b += step
            
imageio.imwrite(image_path[:-4] + '_solved.png',np.uint8(img_out))
log('path='+repr(path))
