import random
import pygame
import math
import sys

"""Define some constrants for drawing the game window"""
# Set up the drawing window
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = (255, 236, 179)
# Hole properties
PIT_RADIUS = 100
PIT_COLOR = (115, 77, 38)
STONE_RADIUS = 20


"""Initialize variables for game logic"""
# Player properties
player_turn = 1
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0
if len(sys.argv) != 2 or sys.argv[1] not in ["human", "computer"]:
    print("Usage: python mancala.py [human|computer]")
    sys.exit()
player_2 = sys.argv[1]
COMPUTER_DELAY = 1000


"""Define constant for positions and font"""
# Board properties
USERS_X = 350
USER1_Y = 250
USER2_Y = 500
pygame.font.init()
FONT = pygame.font.SysFont(None, 40)
PLAYER_TURN_TEXT = FONT.render(f"Player {player_turn}'s turn", True, (0, 0, 0))


"""Initialize variables for game logic"""
# Stones
stones_pits = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]


"""Define some style properties"""
# Initialize the game
playing = True
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Mancala")
icon = pygame.image.load('mancala.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

def generate_random_color():
    """Generate a random color.

    Returns:
        tuple: A tuple containing three integers representing an RGB color.
    """
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def draw_stones_in_circle_pits():
    """Draw stones in the circular pits on the board. Also draw the number of stones under each pit."""
    for i in range(6):
        for j in range(2):
            pit_center_x = USERS_X + USER1_Y * i
            pit_center_y = USER1_Y if j == 0 else USER2_Y
            for k in range(stones_pits[j][i]):
                angle = random.uniform(0, 2 * math.pi)
                radius = random.uniform(0, PIT_RADIUS - STONE_RADIUS)
                stone_x = pit_center_x + int(radius * math.cos(angle))
                stone_y = pit_center_y + int(radius * math.sin(angle))
                pygame.draw.circle(screen, generate_random_color(), (stone_x, stone_y), STONE_RADIUS)

            number_text = FONT.render(str(stones_pits[j][i]), True, (0, 0, 0))
            if j == 0:
                screen.blit(number_text, (pit_center_x - 10, pit_center_y - 125 - 15))
            else:
                screen.blit(number_text, (pit_center_x - 10, pit_center_y + 125))

def draw_stones_in_rectangle_pits():
    """Draw stones in the rectangular (mancaka) pits on the board."""
    for i in range(1, 3):
        player_stones = PLAYER_1_SCORE if i == 1 else PLAYER_2_SCORE
        for j in range(player_stones):
            if i == 1:
                stone_x = random.randint(110, 190)
                stone_y = random.randint(USER1_Y - 10, USER1_Y + 270)
            else:
                stone_x = random.randint(100 + 10 + math.floor(6.6 * 250), 200 + math.floor(6.6 * 250) - 10)
                stone_y = random.randint(USER1_Y - 10, USER1_Y + 270)
            
            pygame.draw.circle(screen, generate_random_color(), (stone_x, stone_y), STONE_RADIUS)
            number_text = FONT.render(str(eval(f"PLAYER_{i}_SCORE")), True, (0, 0, 0))

def draw_game_window(captured_stones=0, winner=0):
    """Draw the game window with the current state of the board.

    Args:
        captured_stones (int, optional): Number of stones captured in the last move. Defaults to 0.
        winner (int, optional): The player number who won the game. Defaults to 0.
    """
    screen.fill(BACKGROUND_COLOR)
    # Draw the circle pits
    for i in range(6):
        pygame.draw.circle(screen, PIT_COLOR, (USERS_X + 250 * i, USER1_Y), PIT_RADIUS)
        pygame.draw.circle(screen, PIT_COLOR, (USERS_X + 250 * i, USER2_Y), PIT_RADIUS)
    # Draw the rectangle pits
    pygame.draw.rect(screen, PIT_COLOR, (100, USER1_Y - 20, 100, 300), PIT_RADIUS)
    pygame.draw.rect(screen, PIT_COLOR, (100 + 6.6 * 250, USER1_Y - 20, 100, 300), PIT_RADIUS)
    # Draw the stones
    draw_stones_in_circle_pits()
    draw_stones_in_rectangle_pits()
    if winner != 0:
        winner_text = FONT.render(f"Player {winner} won!", True, (0, 0, 0))
        screen.blit(winner_text, (750, 50))
    else:
        # Draw the player turn text
        player_clicked_text = FONT.render(f"Player {player_turn} turn", True, (0, 0, 0))
        if player_turn == 1:
            screen.blit(player_clicked_text, (50, 50))
        else:
            screen.blit(player_clicked_text, (1600, 50))

    # Draw the player scores
    player_1_score_text = FONT.render(f"Player 1 score: {PLAYER_1_SCORE}", True, (0, 0, 0))
    player_2_score_text = FONT.render(f"Player 2 score: {PLAYER_2_SCORE}", True, (0, 0, 0))
    screen.blit(player_1_score_text, (50, 700))
    screen.blit(player_2_score_text, (1600, 700))

    if captured_stones != 0:
        captured_stones_text = FONT.render(f"Player {3 - player_turn} captured {captured_stones} stones", True, (0, 0, 0))
        screen.blit(captured_stones_text, (750, 700))

    # Draw player's stones in the pits
    pygame.display.flip()

def pit_chosen(i, j):
    """Handle the logic when a pit is chosen by a player.

    Args:
        i (int): Row index of the chosen pit.
        j (int): Column index of the chosen pit.

    Returns:
        int: Number of stones captured in the move.
    """
    global PLAYER_1_SCORE
    global PLAYER_2_SCORE
    global player_turn
    global stones_pits
    stones_captured = 0
    no_of_stones = stones_pits[i][j]
    stones_pits[i][j] = 0
    k = 0
    last_stone_in_mancala = True
    while k < no_of_stones:
        if i == 0:
            j -= 1
        else:
            j += 1
        
        if j == -1:
            i = 1
            j = 0
            if player_turn == 1:
                PLAYER_1_SCORE += 1
                k += 1
                last_stone_in_mancala = True
        elif j == 6:
            i = 0
            j = 5
            if player_turn == 2:
                PLAYER_2_SCORE += 1
                k += 1
                last_stone_in_mancala = True

        if k < no_of_stones:
            stones_pits[i][j] += 1
            k += 1
            last_stone_in_mancala = False

# Check if the last stone was placed in an previous empty pit
    if i + 1 == player_turn and stones_pits[i][j] == 1 and stones_pits[1 - i][j] != 0:
        if i == 0:
            stones_captured = stones_pits[1][j] + stones_pits[0][j]
            PLAYER_1_SCORE += stones_pits[1][j] + stones_pits[0][j]
            stones_pits[0][j] = 0
            stones_pits[1][j] = 0
        else:
            stones_captured = stones_pits[1][j] + stones_pits[0][j]
            PLAYER_2_SCORE += stones_pits[0][j] + stones_pits[1][j]
            stones_pits[0][j] = 0
            stones_pits[1][j] = 0   
    if stones_captured != 0:
        print(f"Player {player_turn} captured {stones_captured} stones. Last positions: {i} {j}")
    if last_stone_in_mancala:
        player_turn = 3 - player_turn
     
    return stones_captured

def check_if_game_over():
    """Check if the game is over.

    Returns:
        bool: True if the game is over, False otherwise.
    """
    global stones_pits
    if sum(stones_pits[0]) == 0 or sum(stones_pits[1]) == 0:
        return True
    return False

def make_a_turn(i, j):
    """Make a turn for the current player.

    Args:
        i (int): Row index of the chosen pit.
        j (int): Column index of the chosen pit.

    Returns:
        int: The player number whose turn it is next.
    """
    global player_turn 
    global PLAYER_1_SCORE
    global PLAYER_2_SCORE
    global stones_pits
    if stones_pits[i][j] == 0:
        return player_turn
    
    captured_stones = pit_chosen(i, j)
    player_turn = 3 - player_turn
    if check_if_game_over():
        PLAYER_1_SCORE += sum(stones_pits[0])
        PLAYER_2_SCORE += sum(stones_pits[1])

        stones_pits = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

        winner = 1 if PLAYER_1_SCORE > PLAYER_2_SCORE else 2
        draw_game_window(captured_stones, winner)
        player_turn = 0
        return 0
    draw_game_window(captured_stones)
    return player_turn


"""Main game loop"""
draw_game_window()
while playing:
    if player_2 != "human" and player_turn == 2:
        computer_start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - computer_start_time < COMPUTER_DELAY:
            pass
        j = random.choice([i for i in range(0,6) if stones_pits[1][i] != 0])
        make_a_turn(1, j)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            is_pit_clicked = [j for i in range(6) for j in range(1, 3) if math.sqrt((pos[0] - (USERS_X + 250 * i))**2 + (pos[1] - (USER1_Y if j == 1 else USER2_Y))**2) <= PIT_RADIUS]
            if len(is_pit_clicked) == 0:
                is_pit_clicked = 0
            else:
                is_pit_clicked = is_pit_clicked[0]

            if is_pit_clicked != 0:
                print(is_pit_clicked)
                if player_turn == is_pit_clicked:
                    i = is_pit_clicked - 1
                    j = [i for i in range(6) for j in range(1, 3) if math.sqrt((pos[0] - (USERS_X + 250 * i))**2 + (pos[1] - (USER1_Y if j == 1 else USER2_Y))**2) <= PIT_RADIUS][0]
                    if player_turn == make_a_turn(i, j):
                        player_clicked_text = FONT.render(f"Please select a pit with stones.", True, (0, 0, 0))
                        screen.blit(player_clicked_text, (900, 50))
                        pygame.display.update()
                else:
                    pygame.display.update((300, 50, 1300, 100))
                    player_clicked_text = FONT.render(f"Please click on one of yours pits", True, (0, 0, 0))
                    screen.blit(player_clicked_text, (300, 50))
                    pygame.display.update()

# clock.tick(10)
# Flip the display
# pygame.time.wait(1000)

# pygame.quit()



