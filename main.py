"""
Program of a 3 missionaries and 3 cannibals problem programmed
using the pygame module.
"""

import sys
import pygame
from pygame.locals import *

pygame.init()
WINDOW = pygame.display.set_mode((1000, 800))
ARENA = WINDOW.get_rect()

missionary_1 = {"file": "missionary.png"}
missionary_2 = {"file": "missionary.png"}
missionary_3 = {"file": "missionary.png"}
cannibal_1 = {"file": "cannibal.png"}
cannibal_2 = {"file": "cannibal.png"}
cannibal_3 = {"file": "cannibal.png"}

boat_image = pygame.image.load("boat.png")
boat = boat_image.get_rect()
boat.center = (300, 400)

actors = [missionary_1, missionary_2, missionary_3, cannibal_1, cannibal_2,
          cannibal_3]
actors_starting_pos = [""] * 6
for i, actor in enumerate(actors):
    actor["surf"] = pygame.image.load(actor["file"])
    actor["rect"] = actor["surf"].get_rect()
    actor["rect"].midleft = (0, (i + 1) * ARENA.height / 7)
    actors_starting_pos[i] = actor["rect"].center

GAME_GRAPH = {
    "left":
        {
            "mmmccc-": {"m": "mmccc-m", "mm": "mccc-mm", "mc": "mmcc-mc",
                        "c": "mmmcc-c", "cc": "mmmc-cc"},
            "mmmcc-c": {"m": "mmcc-mc", "mm": "mcc-mmc", "mc": "mmc-mcc",
                        "c": "mmmc-cc", "cc": "mmm-ccc"},
            "mmmc-cc": {"m": "mmc-mcc", "mm": "mc-mmcc", "mc": "mm-mccc",
                        "c": "mmm-ccc"},
            "mmm-ccc": {"m": "mm-mccc", "mm": "m-mmccc"},
            "mmccc-m": "failure",
            "mmcc-mc": {"m": "mcc-mmc", "mm": "cc-mmmc", "mc": "mc-mmcc",
                        "c": "mmc-mcc", "cc": "mm-mccc"},
            "mmc-mcc": "failure",
            "mm-mccc": "failure",
            "mccc-mm": "failure",
            "mcc-mmc": "failure",
            "mc-mmcc": {"m": "c-mmmcc", "mc": "-mmmccc", "c": "c-mmccc"},
            "m-mmccc": "failure",
            "ccc-mmm": {"c": "cc-mmmc", "cc": "c-mmmcc"},
            "cc-mmmc": {"c": "c-mmmcc", "cc": "-mmmccc"},
            "c-mmmcc": {"c": "mmmcc-c"},
        },
    "right":
        {
            "mmmcc-c": {"c": "mmmccc-"},
            "mmmc-cc": {"c": "mmmcc-c", "cc": "mmmccc-"},
            "mmm-ccc": {"c": "mmmc-cc", "cc": "mmmcc-c"},
            "mmccc-m": "failure",
            "mmcc-mc": {"m": "mmmcc-c", "mc": "mmmccc-", "c": "mmccc-m"},
            "mmc-mcc": "failure",
            "mm-mccc": "failure",
            "mccc-mm": "failure",
            "mcc-mmc": "failure",
            "mc-mmcc": {"m": "mmc-mcc", "mm": "mmmc-cc", "mc": "mmcc-mc",
                        "c": "mcc-mmc", "cc": "mccc-mm"},
            "m-mmccc": "failure",
            "ccc-mmm": {"m": "mccc-mm", "mm": "mmccc-m"},
            "cc-mmmc": {"m": "mcc-mmc", "mm": "mmcc-mc", "mc": "mccc-mm",
                        "c": "ccc-mmm"},
            "c-mmmcc": {"m": "mc-mmcc", "mm": "mmc-mcc", "mc": "mcc-mmc",
                        "c": "cc-mmmc", "cc": "ccc-mmm"},
            "-mmmccc": "success"
        }
}

# starting game state
game_state = "mmmccc-"

# starting mouse state
clicking = False
which = 100
moving = False

# starting  passengers state
passengers = [9, 9]

# starting boat side
boat_side = "left"

# BACKGROUND image in game
BACKGROUND = pygame.image.load("background.png")
BACKGROUND_RECT = BACKGROUND.get_rect()

# BACKGROUND image in menu
BACKGROUND_MENU = pygame.image.load("background_menu.png")
BACKGROUND_MENU_RECT = BACKGROUND_MENU.get_rect()

# font declaration
MY_FONT = pygame.font.Font('freesansbold.ttf', 48)

# starting state of variables checking is we are in menu or game
menu = True
game_is_on = False

# starting move count
move_count = 0

fpsClock = pygame.time.Clock()


def boat_move(who, side):
    """
    function moving the boat and its passengers
    to the other side.

    parameter who - list of all passengers
    parameter side - side on which the boat is on
    returns true if the boat was moved and false if it hasn't
    """
    global actors, actors_starting_pos, boat_image, boat, WINDOW
    done = False
    if side == "left":
        boat.center = (1000 - boat.centerx, 400)
        boat_image = pygame.transform.flip(boat_image, True, False)
        for char in who:
            if char != 9:
                actors[char]["rect"].center = (
                    1000 - actors_starting_pos[char][0],
                    actors_starting_pos[char][1])
                actors[char]["surf"] = pygame.transform.flip(
                    actors[char]["surf"], True, False)
                actors_starting_pos[char] = actors[char]["rect"].center
    elif side == "right":
        boat.center = (1000 - boat.centerx, 400)
        boat_image = pygame.transform.flip(boat_image, True, False)
        for char in who:
            if char != 9:
                actors[char]["rect"].center = (
                    1000 - actors_starting_pos[char][0],
                    actors_starting_pos[char][1])
                actors[char]["surf"] = pygame.transform.flip(
                    actors[char]["surf"], True, False)
                actors_starting_pos[char] = actors[char]["rect"].center
    return done


def back_to_start(who):
    """
    function putting character at its starting position.

    parameter who - the chosen character
    """
    actor["rect"].center = (actors_starting_pos[actors.index(who)][0],
                            actors_starting_pos[actors.index(who)][1])


def move_to_boat(who, boat_f, who_on_boat, code):
    """
    function moving chosen character to boat if its not taken.

    parameter who - the chosen character
    parameter boat_f - boat
    parameter who_on_boat - list of characters on boat. (9 if none on chosen
    position)
    returns true if the boat was full and false if it was not.
    """
    if who_on_boat[0] == 9:
        who.center = (boat_f.centerx - 50, boat_f.centery - 26)
        return False
    elif who_on_boat[1] == 9 and who_on_boat[0] != code:
        who.center = (boat_f.centerx + 40, boat_f.centery - 26)
        return False
    return True


def get_boat_state(state):
    """
    Function returning who is currently on the boat.

    parameter state - list of people on boat, 9 if no one on chosen spot.
    """
    if state[0] == 9:
        if state[1] <= 2:
            return "m"
        elif state[1] > 2:
            return "c"
    elif state[1] == 9:
        if state[0] <= 2:
            return "m"
        elif state[0] > 2:
            return "c"
    elif state[0] <= 2 and state[1] <= 2:
        return "mm"
    elif state[0] > 2 and state[1] > 2:
        return "cc"
    elif state[0] > 2 and state[1] <= 2:
        return "mc"
    elif state[0] <= 2 and state[1] > 2:
        return "mc"


def failure():
    """
    Function printing fail screen after loosing.
    """
    WINDOW.fill(pygame.Color("red"))
    my_font_failure = pygame.font.Font('freesansbold.ttf', 200)
    msg = my_font_failure.render("Failure", True, (0, 0, 0))
    msg_box = msg.get_rect()
    msg_box.center = ARENA.center
    WINDOW.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)


def success():
    """
    Function printing success screen after winning.
    """
    WINDOW.fill(pygame.Color("green"))
    my_font_success = pygame.font.Font('freesansbold.ttf', 200)
    msg = my_font_success.render("Success!", True, (255, 255, 255))
    msg_box = msg.get_rect()
    msg_box.center = ARENA.center
    WINDOW.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)


def event_handler():
    """
    Function taking care of users input and handling moving characters
    by dragging them with mouse.
    It also counts moves and sets the side the boat is on.
    """
    global boat_side, moving, which, game_state, GAME_GRAPH, passengers, \
        move_count
    for event_1 in pygame.event.get():
        if event_1.type == QUIT:
            pygame.quit()
            sys.exit()
        if event_1.type == MOUSEBUTTONDOWN:
            for x in range(6):
                if actors[x]["rect"].collidepoint(event_1.pos):
                    moving = True
                    which = x
        elif event_1.type == MOUSEBUTTONUP:
            moving = False
            which = 100
        elif event_1.type == MOUSEMOTION and moving:
            actors[which]["rect"].move_ip(event_1.rel)
        if event_1.type == pygame.KEYDOWN:
            if event_1.key == pygame.K_SPACE:
                if passengers[0] != 9 or passengers[1] != 9:
                    move_count += 1
                    boat_move(passengers, boat_side)
                    key = get_boat_state(passengers)
                    game_state = GAME_GRAPH[boat_side][game_state][key]
                    if boat_side == "left":
                        boat_side = "right"
                    elif boat_side == "right":
                        boat_side = "left"


def passengers_position_handler():
    """
    Function moving characters either to starting position,
    to boat or leaving them on the spot based on current boat status
    and where they are left.
    """
    for character in actors:
        if 100 < character["rect"].centerx < 900:
            is_full = move_to_boat(character["rect"], boat, passengers,
                                   actors.index(character))
            if not is_full:
                if passengers[0] == 9:
                    passengers[0] = actors.index(character)
                elif passengers[1] == 9 and passengers[0] \
                        != actors.index(character):
                    passengers[1] = actors.index(character)
            if passengers[0] != 9 and passengers[1] != 9 and \
                    passengers[0] != actors.index(character) and \
                    passengers[1] != actors.index(character):
                back_to_start(character)
            elif boat_side == "left" and \
                    actors_starting_pos[actors.index(character)][0] > 500:
                back_to_start(character)
            elif boat_side == "right" and \
                    actors_starting_pos[actors.index(character)][0] < 500:
                back_to_start(character)
        if character["rect"].centerx < 100 or character["rect"].centerx > 900:
            if passengers[0] == actors.index(character):
                passengers[0] = 9
            if passengers[1] == actors.index(character):
                passengers[1] = 9


def displaying_objects_game():
    """
    Function displaying all the characters and
    move count and background while the game is on.
    """
    move_count_txt = str(move_count)
    move_count_msg = MY_FONT.render(move_count_txt, True, (0, 0, 0))
    move_count_msg_box = move_count_msg.get_rect()
    move_count_msg_box.center = (ARENA.centerx, 100)
    WINDOW.blit(BACKGROUND, BACKGROUND_RECT)
    WINDOW.blit(move_count_msg, move_count_msg_box)
    for character in actors:
        WINDOW.blit(character["surf"], character["rect"])
    WINDOW.blit(boat_image, boat)


def menu_handler():
    """
    Function handling menu display and
    taking users input.
    """
    global menu, game_is_on
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                menu = False
                game_is_on = True
    WINDOW.blit(BACKGROUND_MENU, BACKGROUND_MENU_RECT)


def main():
    global menu, game_is_on, clicking
    while True:
        if menu:
            menu_handler()
        if game_is_on:
            if GAME_GRAPH[boat_side][game_state] == "failure":
                failure()
                pygame.time.wait(1000)
                sys.exit()
            elif GAME_GRAPH[boat_side][game_state] == "success":
                success()
                pygame.time.wait(1000)
                sys.exit()

            clicking = False

            event_handler()

            if not moving:
                passengers_position_handler()

            displaying_objects_game()

        pygame.display.flip()
        fpsClock.tick(120)


if __name__ == "__main__":
    main()
