from termcolor import colored
import time, random

def init_board(board_size):
    """
    Initialize the board to white zero.
    The board (row, col, weight, color)
    """
    board = [[["0", "white"] for i in range(int(board_size))] for j in range(int(board_size))]
    return board

def init_users_hand(board_size):
    """
    Initialize players' hand according to the board size.
    """
    if board_size == "4":
        return([[2, 3, 5, 8, 13] for i in range(2)])
    elif board_size == "6":
        return([[2, 2, 3, 3, 5, 5, 8, 8, 8, 13, 13] for i in range(2)])

def init_score():
    """
    Initialize players' score to 0.([User, AI])
    """
    return [0, 0]

def show_hand(users_hand):
    """
    Show current hand of players.
    """
    text1 = colored("[AI_0 chess pieces]", "white", "on_green")
    text2 = colored("[AI_1 chess pieces]", "white", "on_yellow")
    print(text1 + ": " + str(users_hand[0]))
    print(text2 + ": " + str(users_hand[1]))

def show_board(board_size, board):
    """
    Show current board.
    """
    for row in range(int(board_size)):
        row_str = ""
        for col in range(int(board_size)):
            row_str += colored("{:>3}".format(board[row][col][0]), board[row][col][1])
        print(row_str)

def check_board(board_size, board, score):
    """
    Check every none zero or none X cell if their value exceed 15.
    Return the board and score after checked.
    """
    marked_cell = []
    for row in range(int(board_size)):
        for col in range(int(board_size)):
            if board[row][col][0] == "0" or board[row][col][0] == "X":
                continue
            value = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if row + i < 0 or row + i >= int(board_size) or \
                        col + j < 0 or col + j >= int(board_size): 
                        pass
                    else:
                        if board[row + i][col + j][0] != "X":
                            value += int(board[row + i][col + j][0])
            if value > 15:
                if board[row][col][1] == "green":
                    score[0] -= int(board[row][col][0])
                elif board[row][col][1] == "yellow":
                    score[1] -= int(board[row][col][0])
                marked_cell.append([row, col])
    for cell in marked_cell:
        board[cell[0]][cell[1]][0] = "X"
        board[cell[0]][cell[1]][1] = "red"
    return board, score

def toy_AI(board_size, board, AI_hand):
    """
    Always use the smallest card and always pick the first cell.
    """
    for row in range(int(board_size)):
        for col in range(int(board_size)):
            if board[row][col][0] == "0":
                weight = AI_hand[0]
                return row, col, weight  

def marked(board_size, board, row, col):
    """
    Check if the index value bigger than 15.
    Return True if the cell is marked.
    """
    value = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if board[row][col][0] == "0" or board[row][col][0] == "X":
                continue
            else:
                value += int(board[row][col][0])
    if value > 15:
        return True

def random_select(board_size, board, AI_hand):
    row = random.randrange(int(board_size))
    col = random.randrange(int(board_size))
    card = AI_hand[random.randrange(len(AI_hand))]
    while board[row][col][0] != "0":
        row = random.randrange(int(board_size))
        col = random.randrange(int(board_size))
    return row, col, card

def greedy_AI_0(board_size, board, AI_hand):
    """
    Pick the highest value cell and card to play.
    Return picked row, col and the card.
    """
    max_cell = []
    max_score = 0
    for row in range(int(board_size)):
        for col in range(int(board_size)):
            if board[row][col][0] != "0" :
                continue
            for card in set(AI_hand):
                board[row][col] = [str(card), "green"]
                score = card # Center value
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if board[row][col][0] == "0" or board[row][col][0] == "X":
                            continue
                        else:
                            if row + i < 0 or row + i >= int(board_size) or \
                                col + j < 0 or col + j >= int(board_size): 
                                pass
                            else:
                                if marked(board_size, board, row + i, col + j):
                                    if board[row+i][col+j][1] == "yellow": 
                                        score += int(board[row+i][col+j][0])
                                    elif board[row+i][col+j][1] == "green": 
                                        score -= int(board[row+i][col+j][0])
                board[row][col] = ["0", "white"]
                if score > max_score:
                    max_score = score
                    max_cell = [row, col, card]
    if max_cell == []:
        # row, col, weight = toy_AI(board_size, board, AI_hand)
        row, col, weight = random_select(board_size, board, AI_hand)
        return row, col, weight
    return max_cell[0], max_cell[1], max_cell[2]

def greedy_AI_1(board_size, board, AI_hand):
    """
    Pick the highest value cell and card to play.
    Return picked row, col and the card.
    """
    max_cell = []
    max_score = 0
    for row in range(int(board_size)):
        for col in range(int(board_size)):
            if board[row][col][0] != "0" :
                continue
            for card in set(AI_hand):
                board[row][col] = [str(card), "yellow"]
                score = card # Center value
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if board[row][col][0] == "0" or board[row][col][0] == "X":
                            continue
                        else:
                            if row + i < 0 or row + i >= int(board_size) or \
                                col + j < 0 or col + j >= int(board_size): 
                                pass
                            else:
                                if marked(board_size, board, row + i, col + j):
                                    if board[row+i][col+j][1] == "green": # If marked cell is user's -> Plus
                                        score += int(board[row+i][col+j][0])
                                    elif board[row+i][col+j][1] == "yellow": # If marked cell is AI's -> Minus
                                        score -= int(board[row+i][col+j][0])
                board[row][col] = ["0", "white"]
                if score > max_score:
                    max_score = score
                    max_cell = [row, col, card]
    if max_cell == []:
        # row, col, weight = toy_AI(board_size, board, AI_hand)
        row, col, weight = random_select(board_size, board, AI_hand)
        return row, col, weight
    return max_cell[0], max_cell[1], max_cell[2]


def game():
    first_user = input("User First?(0/1) ") # 0:User 1:Computer
    board_size = input("Board Size?(4 or 6) ")
    if (first_user != "0" and first_user != "1") or (board_size != "4" and board_size != "6"):
        print("Please input legal number.")
        exit()
    users_hand = init_users_hand(board_size)
    board = init_board(board_size)
    score = init_score() # score[0] = User's score score[1] = AI's score
    show_board(board_size, board)
    show_hand(users_hand)
    turn = int(first_user)
    while users_hand[0] != [] or users_hand[1] != []:
        if turn == 1:
            row, col, weight = greedy_AI_0(board_size, board, users_hand[0])
            text = colored("[AI_1]: ", "white", "on_green")
            print(text+ " (" + str(row) + ", " + str(col) + ", " + str(weight) + ")") 
            board[row][col] = [str(weight), "green"]
            users_hand[0].remove(weight)
            score[0] += weight
            board, score = check_board(board_size, board, score)
            show_board(board_size, board)
            show_hand(users_hand)
            turn = 0
        else:
            # Computer's turn
            # row, col, weight = toy_AI(board_size, board, users_hand[1])
            row, col, weight = greedy_AI_1(board_size, board, users_hand[1])
            text = colored("[AI_2]: ", "white", "on_yellow")
            print(text+ " (" + str(row) + ", " + str(col) + ", " + str(weight) + ")") 
            board[row][col] = [str(weight), "yellow"]
            users_hand[1].remove(weight)
            score[1] += weight
            board, score = check_board(board_size, board, score)
            show_board(board_size, board)
            show_hand(users_hand)
            turn = 1
    if score[0] > score[1]:
        print("AI_0 Win.")
    elif score[0] < score[1]:
        print("AI_1 Win.")
    else:
        print("Draw.")

if __name__ == "__main__":
    game()
