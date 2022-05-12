
import sys
import random
from Button import Button
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# play and loop the music
pygame.mixer.music.load("Assets/music1.wav")
pygame.mixer.music.play(-1)

fps = 60
fpsClock = pygame.time.Clock()

# screen and window
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong but it's made with python and probably eats your cpu alive because it's python")

# paddles
paddle_width, paddle_height = 20, 80
ball_width, ball_height = 20, 20

x_offset = 20
xpos1, xpos2 = x_offset, screen.get_width() - x_offset - paddle_width  # sets the player in the middle of the screen
ypos1 = screen.get_height()/2 - (paddle_height / 2)
ypos2 = screen.get_height()/2 - (paddle_height / 2)

paddle_speed = 2.5

# ball
xposball = screen.get_width() / 2
yposball = screen.get_height() / 2

ball_speed = 4
xvelocity_ball = 1
yvelocity_ball = 0
ball_bounce_modifier = 0.025

# GUI
font = pygame.font.SysFont(None, 64)
GREEN = (117, 255, 152)
ORANGE = (255, 193, 117)
RED = (255, 126, 117)
BLUE = (117, 181, 255)


# points
player1_points, player2_points = 0, 0
winning_point_amount = 5

#game settings
do_rainbowball = False


gaming = False
running_mainmenu = True
running_optionsmenu = False

def rainbow_color(value):
    step = (value // 256) % 6
    pos = value % 256

    if step == 0:
        return (255, pos, 0)
    if step == 1:
        return (255-pos, 255, 0)
    if step == 2:
        return (0, 255, pos)
    if step == 3:
        return (0, 255-pos, 255)
    if step == 4:
        return (pos, 0, 255)
    if step == 5:
        return (255, 0, 255-pos)

def score(player):
    global player1_points
    global player2_points

    global xposball
    global yposball

    global ypos1
    global ypos2

    global xvelocity_ball
    global yvelocity_ball

    xposball = screen.get_width() / 2
    yposball = screen.get_height() / 2

    ypos1 = screen.get_height() / 2 - (paddle_height / 2)
    ypos2 = screen.get_height() / 2 - (paddle_height / 2)

    xvelocity_ball = 0
    yvelocity_ball = 0

    rect_ball = Rect(xposball, yposball, ball_width, ball_height)
    pygame.draw.rect(screen, (255, 255, 255), rect_ball)  # draw ball

    if player == "player1":
        player1_points += 1
        print("player 1 scored!")
        xvelocity_ball = 1
    else:
        player2_points += 1
        print("player 2 scored!")
        xvelocity_ball = -1
    yvelocity_ball = 0


def fade_in_black(width, height):
    fade = pygame.Surface((width,height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(15)


def fade_in_text(surface, pos, endgame):
    global running_mainmenu

    for alpha in range(0, 300):
        surface.set_alpha(alpha)
        screen.blit(surface, pos)
        pygame.display.update()
        pygame.time.delay(15)
    if endgame:
        open_main_menu()

def open_win_screen(player):
    global gaming
    gaming = False
    fade_in_black(screen.get_width(),screen.get_height())

    font = pygame.font.SysFont(None, 150)
    if player == 1:
        text = font.render("Player 1 won", True, RED)
        fade_in_text(text, (0,0), True)
    if player == 2:
        text = font.render("Player 2 won", True, BLUE)
        fade_in_text(text, (0,0), True)

def open_controls_screen():
    smallfont = pygame.font.SysFont(None, 30)

    global running_mainmenu

    running_mainmenu = False
    screen.fill((0, 0, 0))
    running_controlsscreen = True
    while running_controlsscreen:
        text = smallfont.render("Player 1: Z or W is up, S is down", True, RED)
        screen.blit(text, (screen.get_width()/2- text.get_width()/2, screen.get_height()/2))
        text = smallfont.render("Player 2: Arrow key up to move up, arrow key down to move down", True, BLUE)
        screen.blit(text, (screen.get_width()/2- text.get_width()/2, screen.get_height() / 2 + 30))

        text = smallfont.render("Press any key to go back", True, (255,255,255))
        screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, screen.get_height() - 30))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running_mainmenu = True
                running_controlsscreen = False
        pygame.display.flip()
        fpsClock.tick(60)
# Game loop
def play():
    global player1_points
    global player2_points
    #variables
    global xposball
    global yposball

    global ypos1
    global ypos2

    global xvelocity_ball
    global yvelocity_ball

    global running_mainmenu
    global running_optionsmenu

    running_optionsmenu = False
    running_mainmenu = False
    gaming = True

    ballcolor = (255, 255, 255)
    rainbow_color_value = 0

    player1_points = 0
    player2_points = 0


    while gaming:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # Update.

        #drawing the scoretext

        scoretext1 = font.render(f"{player1_points}", True, (255, 126, 117))
        scoretext2 = font.render(" | ", True, (255, 255, 255))
        scoretext3 = font.render(f"{player2_points}", True, (117, 181, 255))

        scoretext_width = scoretext1.get_width() + scoretext2.get_width() + scoretext3.get_width()

        y_scoretext_offset = 10
        screen.blit(scoretext1, (screen.get_width()/2 - scoretext_width/2, y_scoretext_offset))
        screen.blit(scoretext2, (screen.get_width()/2 - scoretext_width/2 + scoretext1.get_width(), y_scoretext_offset))
        screen.blit(scoretext3,
                    (screen.get_width() / 2 - scoretext_width / 2 + scoretext1.get_width() + scoretext2.get_width(),
                     y_scoretext_offset))

        if do_rainbowball:
            rainbow_color_value = (rainbow_color_value + 1) % (256 * 6)
            ballcolor = rainbow_color(rainbow_color_value)

        # checking if keys are being held down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] or  keys[pygame.K_w]:
            ypos1 -= 1 * paddle_speed
        if keys[pygame.K_s]:
            ypos1 += 1 * paddle_speed
        if keys[pygame.K_UP]:
            ypos2 -= 1 * paddle_speed
        if keys[pygame.K_DOWN]:
            ypos2 += 1 * paddle_speed

        #moving the ball
        xposball += xvelocity_ball * ball_speed
        yposball += yvelocity_ball * ball_speed

        # getting the players and ball coordinates, used for drawing later
        rect1 = Rect(xpos1, ypos1, paddle_width, paddle_height)
        rect2 = Rect(xpos2, ypos2, paddle_width, paddle_height)
        rect_ball = Rect(xposball, yposball, ball_width, ball_height)

        #calculations used to make collision checking easier
        y1center = ypos1 + paddle_height/2
        y2center = ypos2 + paddle_height/2

        distance_ball_y1center = yposball - y1center
        distance_ball_y2center = yposball - y2center

        # checking if the ball collides with the players
        collide = rect_ball.colliderect(rect1)
        if collide:
            yvelocity_ball = distance_ball_y1center * ball_bounce_modifier
            xvelocity_ball *= -1
        collide = rect_ball.colliderect(rect2)
        if collide:
            yvelocity_ball = distance_ball_y2center * ball_bounce_modifier
            xvelocity_ball *= -1

        # checking if the ball bounces on the top and bottom borders
        if yposball < 0 or yposball + ball_height > screen.get_height():
            yvelocity_ball *= -1
        # checking if a player scores
        if xposball > screen.get_width():
            score("player1")
        if xposball + ball_width < 0:
            score("player2")

        #check if anyone has won
        if player1_points == winning_point_amount:
            open_win_screen(1)
            break
        if player2_points == winning_point_amount:
            open_win_screen(2)
            break


        # Draw.
        pygame.draw.rect(screen, (255, 255, 255), rect1) # draw player 1
        pygame.draw.rect(screen, (255, 255, 255), rect2)  # draw player 2
        pygame.draw.rect(screen, ballcolor, rect_ball)  # draw ball

        pygame.display.flip()
        fpsClock.tick(fps)

def open_options_menu():
    global running_mainmenu, winning_point_amount
    global gaming

    global do_rainbowball

    running_optionsmenu = True
    running_mainmenu = False
    gaming = False

    BTN_RAINBOWBALL = Button(None, (screen.get_width()/4, 40), "RAINBOWBALL", pygame.font.SysFont(None, 45), GREEN, (255, 126, 117))
    BTN_5PTS = Button(None, (BTN_RAINBOWBALL.x_pos, BTN_RAINBOWBALL.y_pos+40), "5PTS to win",
                      pygame.font.SysFont(None, 45), GREEN, GREEN)
    BTN_10PTS = Button(None, (BTN_RAINBOWBALL.x_pos, BTN_RAINBOWBALL.y_pos + 80), "10PTS to win",
                      pygame.font.SysFont(None, 45), RED, RED)
    BTN_15PTS = Button(None, (BTN_RAINBOWBALL.x_pos, BTN_RAINBOWBALL.y_pos + 120), "15PTS to win",
                       pygame.font.SysFont(None, 45), RED, RED)
    BTN_INFPTS = Button(None, (BTN_RAINBOWBALL.x_pos, BTN_RAINBOWBALL.y_pos + 160), "ENDLESS",
                       pygame.font.SysFont(None, 45), RED, RED)
    playtext = pygame.font.SysFont(None, 45).render("Press any key to start playing.", True, (255, 255, 255))

    while running_optionsmenu:
        delta_time = fpsClock.tick(fps) / 1000.0
        screen.fill((0, 0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_RAINBOWBALL.checkForInput(menu_mouse_pos):
                    do_rainbowball = not do_rainbowball
                if BTN_5PTS.checkForInput(menu_mouse_pos):
                    winning_point_amount = 5
                if BTN_10PTS.checkForInput(menu_mouse_pos):
                    winning_point_amount = 10
                if BTN_15PTS.checkForInput(menu_mouse_pos):
                    winning_point_amount = 15
                if BTN_INFPTS.checkForInput(menu_mouse_pos):
                    winning_point_amount = -1

            if event.type == pygame.KEYDOWN:
                play()
        # update
        if do_rainbowball:
            BTN_RAINBOWBALL.base_color = GREEN
            BTN_RAINBOWBALL.hovering_color = GREEN
            BTN_RAINBOWBALL.text_input = "RAINBOWBALL (ON)"
        else:
            BTN_RAINBOWBALL.base_color = RED
            BTN_RAINBOWBALL.hovering_color = RED
            BTN_RAINBOWBALL.text_input = "RAINBOWBALL (OFF) ;-;"

        if winning_point_amount == 5:
            BTN_5PTS.base_color = GREEN
            BTN_5PTS.hovering_color = GREEN

            for button in [BTN_15PTS, BTN_10PTS, BTN_INFPTS]:
                button.base_color = RED
                button.hovering_color = RED

        if winning_point_amount == 10:
            BTN_10PTS.base_color = GREEN
            BTN_10PTS.hovering_color = GREEN

            for button in [BTN_15PTS, BTN_5PTS, BTN_INFPTS]:
                button.base_color = RED
                button.hovering_color = RED

        if winning_point_amount == 15:
            BTN_15PTS.base_color = GREEN
            BTN_15PTS.hovering_color = GREEN

            for button in [BTN_5PTS, BTN_10PTS, BTN_INFPTS]:
                button.base_color = RED
                button.hovering_color = RED

        if winning_point_amount == -1:
            BTN_INFPTS.base_color = GREEN
            BTN_INFPTS.hovering_color = GREEN

            for button in [BTN_5PTS, BTN_10PTS, BTN_15PTS]:
                button.base_color = RED
                button.hovering_color = RED

        for button in [BTN_RAINBOWBALL, BTN_5PTS, BTN_10PTS, BTN_15PTS, BTN_INFPTS]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        # draw
        screen.blit(playtext, playtext.get_rect(center=(screen.get_width()/2, screen.get_height()*4/5)))

        pygame.display.flip()

def open_main_menu():
    global gaming

    gaming = False
    running_mainmenu = True

    while running_mainmenu:
        screen.fill((0, 0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(None, (screen.get_width() / 2, screen.get_height() / 3), "PLAY",
                             pygame.font.SysFont(None, 120), (255, 255, 255), (117, 255, 152))
        QUIT_BUTTON = Button(None, (screen.get_width() / 2, screen.get_height() / 3 + screen.get_height() / 3 - 35), "QUIT",
                             pygame.font.SysFont(None, 120), (255, 255, 255), (117, 255, 152))
        CONTROLS_BUTTON = Button(None, (screen.get_width() / 2, screen.get_height() - 60), "CONTROLS",
                             pygame.font.SysFont(None, 80), (255, 255, 255), (117, 255, 152))


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(menu_mouse_pos):
                    open_options_menu()
                if QUIT_BUTTON.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if CONTROLS_BUTTON.checkForInput(menu_mouse_pos):
                    open_controls_screen()
        # update

        for button in [QUIT_BUTTON, PLAY_BUTTON, CONTROLS_BUTTON]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        # draw

        pygame.display.flip()
        fpsClock.tick(fps)

open_main_menu()