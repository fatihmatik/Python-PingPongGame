import os
import time
import msvcrt
import random


def draw_board():
    print("-" * (width+2))
    for line in board:
        print("|" + "".join(line) + "|")
    print("-" * (width+2))
    print(f"\t      {scoreRight}::{scoreLeft}" )


def move_pad(direction, pad, x):
    # move UP
    # if the pad is NOT going to collide with the cellar.
    if direction == "up":
        if pad != 0:
            board[pad+paddleLen-1][x] = " "
            board[pad-1][x] = "|"
            pad -= 1
            return pad
    
    # move DOWN
    elif direction == "down":
        if pad != height-paddleLen:
            board[pad][x] = " "
            board[pad+paddleLen][x] = "|"
            pad += 1
            return pad

    return pad


def move_ball():
    global ballx, bally, balldx, balldy

    #hits the ceiling
    if bally == 0 or bally == height-1:
        balldy *= -1
    
    #hits the paddle
    #left pad
    if (ballx == 1) and  pad1_y <= bally <= (pad1_y + paddleLen - 1):
        balldx *= -1
    #right pad
    elif (ballx == width-1) and pad2_y <= bally <= (pad2_y + paddleLen - 1):
        balldx *= -1
    
    #scores
    if ballx == 0:
        board[bally][ballx] = " "
        board[centerY][centerX] = "*"
        ballx = centerX
        bally = centerY
        balldx = random.choice([1,-1])
        balldy = random.choice([1,-1])
        return "right"
    elif ballx == width:
        board[bally][ballx] = " "
        board[centerY][centerX] = "*"
        ballx = centerX
        bally = centerY
        balldx = random.choice([1,-1])
        balldy = random.choice([1,-1])
        return "left"
    
    # Updating the screen w/ ball
    board[bally][ballx] = " "
    ballx += balldx
    bally += balldy
    board[bally][ballx] = "*"


if __name__ == "__main__":
    width = 30
    height = 15
    centerX = width // 2
    centerY = height // 2
    board = [[" "] * (width+1) for itr in range(0,height+1,1)]

    scoreRight = 0
    scoreLeft = 0
    ballx = centerX ; 10
    bally = centerY ; 5
    balldx = random.choice([1,-1]) # x axis speed
    balldy = random.choice([1,-1]) # y axis speed
    paddleLen = 3
    
    # pad1 for left side player; pad2 for right side player
    pad1_y = (height-paddleLen)//2
    pad2_y = (height-paddleLen)//2

    # Setting the ball up
    board[bally][ballx] = "*"
    
    # Getting the padders in place
    for itr in range(0,paddleLen,1):
        board[itr+pad1_y][0] = "|" ; 4,5,6
    for itr in range(0,paddleLen,1):
        board[itr+pad2_y][width-1] = "|" ; 4,5,6

    while True:

        draw_board()

        score = move_ball()
        if score == "right":
            scoreLeft += 1
        elif score == "left":
            scoreRight += 1
        score = " "

        time.sleep(0.05) # duration of every game frame in seconds.
        
        os.system('cls')

        if msvcrt.kbhit():
            key = msvcrt.getch().decode("utf-8").lower()
            # for the right pad
            if key == "w": # move up
                pad1_y = move_pad("up", pad1_y, 0)
            elif key == "s": # move down
                pad1_y = move_pad("down", pad1_y, 0)
            # for the left pad
            elif key == "o": # move up
                pad2_y = move_pad("up", pad2_y, width-1)
            elif key == "l": # move down
                pad2_y = move_pad("down", pad2_y, width-1)
        