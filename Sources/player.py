
import sys
from queue import PriorityQueue
import support_function as spf
score = 0
def print_board(board):
    """In ma trận board một cách đẹp mắt."""
    print("score:"+ str(score))
    for row in board:
        # Nối các ký tự trong hàng, thêm khoảng trắng để dễ đọc
        print(' '.join(str(cell) for cell in row))
    print()  # In dòng trống để phân tách các lần in


def Player(board, list_check_point, direction=None):
    global score
    if spf.check_win(board, list_check_point):
        print("Found win")
        score = 0 
        return True
    start_state = spf.state(board, None, list_check_point)
    cur_pos = spf.find_position_player(start_state.board)
    list_can_move = spf.get_next_pos(start_state.board, cur_pos)
    new_board = board

    # If a direction is provided, process the move
    if direction:
        if direction == "UP":
            next_pos = [cur_pos[0] - 1, cur_pos[1]]
        elif direction == "DOWN":
            next_pos = [cur_pos[0] + 1, cur_pos[1]]
        elif direction == "LEFT":
            next_pos = [cur_pos[0], cur_pos[1] - 1]
        elif direction == "RIGHT":
            next_pos = [cur_pos[0], cur_pos[1] + 1]
        else:
            return new_board  # No valid direction, return unchanged board

        if check_map(list_can_move, next_pos) == 1:
            new_board = spf.move(start_state.board, next_pos, cur_pos, list_check_point)
            score += 1
            print("Board after move:")  # In trạng thái bảng sau mỗi di chuyển
            print_board(new_board)
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                print("Movement:" + str(score))
                score = 0
                return True
    return new_board

def check_map(list_can_move, move):
    isMove = 0
    for next_pos in list_can_move:
        if move[0] == next_pos[0] and move[1] == next_pos[1]:
            isMove = 1
    return isMove