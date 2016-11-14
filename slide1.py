
# coding: utf-8

# In[1]:


import pygame, sys, random
from pygame.locals import *


BOARDWIDTH = 5
BOARDHEIGHT = 5 
TILESIZE = 100
WINDOWWIDTH = 800
WINDOWHEIGHT = 650

BLANK = None



BGCOLOR = (30,144,255)
TILECOLOR = (  75,64,   7)
TEXTCOLOR =  (255, 255, 255)
BORDERCOLOR = (  255,  0, 0)
BASICFONTSIZE = 20


MESSAGECOLOR = (255, 255, 255)

leftmargin= int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
rightmargin = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global  displaymain, font_style, display_reset, draw_reset, display_new, draw_new

    pygame.init()
   
   
    displaymain = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Sliding_Puzzle Of Character')
   
    font_style = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    display_new,   draw_new   = create_text('New Game', (255,0,0), (243,243,34), WINDOWWIDTH - 120, WINDOWHEIGHT - 585)
    display_reset, draw_reset = create_text('Reset',  (255,0,0), (243,243,34), WINDOWWIDTH - 120, WINDOWHEIGHT - 550)
    
    

    playingboard, sequence_answer = newpuzzlefunction(100) #call function with argument of total slides
    answer = solved_puzzle()  # create sloved board
    sequence_move = [] 

    while True: # loop is execute while game is not exit
        move_direction = None # initial direction of the slide to move
        msg = 'Pess arrow keys to slide' 
        if playingboard == answer:
            msg = 'You Sloved This Puzzle'

        draw_playingboard(playingboard, msg)
        
        for event in pygame.event.get(QUIT):
            pygame.quit()
            sys.exit()
            
        for event in pygame.event.get(): # get the event which key is press by user
           
            if event.type == MOUSEBUTTONUP:
                posx, posy = position_click(playingboard, event.pos[0], event.pos[1])#get user click position
                if (posx, posy) == (None, None):
                       
                        if draw_reset.collidepoint(event.pos):
                            resetfunction(playingboard, sequence_move) # user is click on reset button
                            sequence_move = []
                        elif draw_new.collidepoint(event.pos):
                            playingboard, sequence_answer = newpuzzlefunction(100)# clicked on new game button
                            sequence_move = []


            elif event.type == KEYUP:
                    # check which key is press by user
                    if event.key in (K_LEFT,K_l) and movecheck(playingboard, LEFT):
                        move_direction = LEFT
                    elif event.key in (K_RIGHT,K_r) and movecheck(playingboard, RIGHT):
                        move_direction = RIGHT
                    elif event.key in (K_UP,K_u) and movecheck(playingboard, UP):
                        move_direction = UP
                    elif event.key in (K_DOWN,K_d) and movecheck(playingboard, DOWN):
                        move_direction = DOWN

        if move_direction:
            animation(playingboard, move_direction, 'Pess arrow keys to slide',1)#move the slide animation that user move slide
            makeMove(playingboard, move_direction) 
            sequence_move.append(move_direction) # Store which move is taken by user
        pygame.display.update()
        

def solved_puzzle():  # This Function Create initial 5 x 5 board with out random square
    
    counter2 = 1
    puzzle_board = []
    for x in range(BOARDWIDTH):
        board_column = []
        for y in range(BOARDHEIGHT):
            board_column.append(counter2)
            counter2 += BOARDWIDTH
        puzzle_board.append(board_column)
        counter2 -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    puzzle_board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK  # initial balnk position 
    return puzzle_board


def findblank(puzzle_board): # Find Blank square is where located at now 
   
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if puzzle_board[x][y] == BLANK:
                return (x, y)


def makeMove(puzzle_board, move_pos):# move the position of square based on user presskey
   
    blank_posx, blank_posy = findblank(puzzle_board)

    if move_pos == UP:
        puzzle_board[blank_posx][blank_posy], puzzle_board[blank_posx][blank_posy + 1] = puzzle_board[blank_posx][blank_posy + 1], puzzle_board[blank_posx][blank_posy]
    elif move_pos == DOWN:
        puzzle_board[blank_posx][blank_posy], puzzle_board[blank_posx][blank_posy - 1] = puzzle_board[blank_posx][blank_posy - 1], puzzle_board[blank_posx][blank_posy]
    elif move_pos == LEFT:
        puzzle_board[blank_posx][blank_posy], puzzle_board[blank_posx + 1][blank_posy] = puzzle_board[blank_posx + 1][blank_posy], puzzle_board[blank_posx][blank_posy]
    elif move_pos == RIGHT:
        puzzle_board[blank_posx][blank_posy], puzzle_board[blank_posx - 1][blank_posy] = puzzle_board[blank_posx - 1][blank_posy], puzzle_board[blank_posx][blank_posy]


def movecheck(puzzle_board, move_pos): #Check the move is valid or not valid
    blank_posx, blank_posy = findblank(puzzle_board)
    return (move_pos == UP and blank_posy != len(puzzle_board[0]) - 1) or            (move_pos == DOWN and blank_posy != 0) or            (move_pos == LEFT and blank_posx != len(puzzle_board) - 1) or            (move_pos == RIGHT and blank_posx != 0)


def generate_move_random(puzzle_board, position_lastmove=None): # generate random number for slide setting
   
    available_move = [UP, DOWN, LEFT, RIGHT]
    
    if position_lastmove == UP or not movecheck(puzzle_board, DOWN):
        available_move.remove(DOWN)
    if position_lastmove == DOWN or not movecheck(puzzle_board, UP):
        available_move.remove(UP)
    if position_lastmove == LEFT or not movecheck(puzzle_board, RIGHT):
        available_move.remove(RIGHT)
    if position_lastmove == RIGHT or not movecheck(puzzle_board, LEFT):
        available_move.remove(LEFT)

    return random.choice(available_move) # select random move  from remaining valid moves 


def lefttop_position_tile(tile_posx, tile_posy):
    tile_left = leftmargin + (tile_posx * TILESIZE) + (tile_posx -1)
    tile_top = rightmargin + (tile_posy * TILESIZE) + (tile_posy-1 )
    return (tile_left, tile_top)


def position_click(puzzle_board, x, y): # give the position that user is clicked
   
    for tile_posx in range(len(puzzle_board)):
        for tile_posy in range(len(puzzle_board[0])):
            tile_left, tile_top = lefttop_position_tile(tile_posx, tile_posy)
            tileRect = pygame.Rect(tile_left, tile_top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tile_posx, tile_posy)
    return (None, None)


def create_tile(tile_posx, tile_posy, number, x=0, y=0): # draw tile based on left top and TILESIZE
    
    tile_left, tile_top = lefttop_position_tile(tile_posx, tile_posy)
    pygame.draw.rect(displaymain, TILECOLOR, (tile_left + x, tile_top + y, TILESIZE, TILESIZE))
    textSurf = font_style.render(str(chr(number+64)), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = tile_left + int(TILESIZE / 2) + x, tile_top + int(TILESIZE / 2) + y
    displaymain.blit(textSurf, textRect)


def create_text(text, color, bgcolor, tile_top, tile_left):
    
    textSurf = font_style.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (tile_top, tile_left)
    return (textSurf, textRect)


def draw_playingboard(puzzle_board, msg): # draw reset and new gmae button and display message game is sloved or not also redraw board based on slide moved
    displaymain.fill(BGCOLOR)
    if msg:
        textSurf, textRect = create_text(msg, MESSAGECOLOR, BGCOLOR, 330,25)
        displaymain.blit(textSurf, textRect)

    for tile_posx in range(len(puzzle_board)):
        for tile_posy in range(len(puzzle_board[0])):
            if puzzle_board[tile_posx][tile_posy]:
                create_tile(tile_posx, tile_posy, puzzle_board[tile_posx][tile_posy])

    tile_left, tile_top = lefttop_position_tile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(displaymain, BORDERCOLOR, (tile_left - 5, tile_top - 5, width + 11, height + 11), 6)

    displaymain.blit(display_reset, draw_reset)
    displaymain.blit(display_new, draw_new)



def animation(puzzle_board, direction, msg, animationSpeed): 
   

    blank_posx, blank_posy = findblank(puzzle_board)
    if direction == UP:
        x_pos_move = blank_posx
        y_pos_move = blank_posy + 1
    elif direction == DOWN:
        x_pos_move = blank_posx
        y_pos_move = blank_posy - 1
    elif direction == LEFT:
        x_pos_move = blank_posx + 1
        y_pos_move = blank_posy
    elif direction == RIGHT:
        x_pos_move = blank_posx - 1
        y_pos_move = blank_posy

   
    draw_playingboard(puzzle_board, msg)
    baseSurf = displaymain.copy()
   
    moveLeft, moveTop = lefttop_position_tile(x_pos_move, y_pos_move)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
      
        
        displaymain.blit(baseSurf, (0, 0))
        if direction == UP:
            create_tile(x_pos_move, y_pos_move, puzzle_board[x_pos_move][y_pos_move], 0, -i)
        if direction == DOWN:
            create_tile(x_pos_move, y_pos_move, puzzle_board[x_pos_move][y_pos_move], 0, i)
        if direction == LEFT:
            create_tile(x_pos_move, y_pos_move, puzzle_board[x_pos_move][y_pos_move], -i, 0)
        if direction == RIGHT:
            create_tile(x_pos_move, y_pos_move, puzzle_board[x_pos_move][y_pos_move], i, 0)

        pygame.display.update()
        
       

def newpuzzlefunction(numSlides): #create new puzzle
    sequence = []
    puzzle_board = solved_puzzle()
   
    pygame.display.update()
    pygame.time.wait(0) 
    position_lastmove = None
    for i in range(numSlides):
        move_pos = generate_move_random(puzzle_board, position_lastmove)
        animation(puzzle_board, move_pos,"Wait New game is Generated",animationSpeed=int(100))
        makeMove(puzzle_board, move_pos)
        sequence.append(move_pos)
        position_lastmove = move_pos
    return (puzzle_board, sequence)


def resetfunction(puzzle_board, sequence_move):
   
    reset_sequence = sequence_move[:] 
    reset_sequence.reverse()

    for move_pos in reset_sequence:
        if move_pos == UP:
            reset_move_pos = DOWN
        elif move_pos == DOWN:
            reset_move_pos = UP
        elif move_pos == RIGHT:
            reset_move_pos = LEFT
        elif move_pos == LEFT:
            reset_move_pos = RIGHT
        animation(puzzle_board, reset_move_pos, 'Wait Reset The Moves', animationSpeed=int(10))
        makeMove(puzzle_board, reset_move_pos)


if __name__ == '__main__':
    main()

