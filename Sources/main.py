import os

import numpy as np
import pygame

import astar
import player

TIME_OUT = 180


# path_board = os.getcwd() + '\Testcases'
# path_checkpoint = os.getcwd() + '\Checkpoints'

# Lấy thư mục gốc của project (TTNT_BTL)
base_dir = os.path.dirname(os.path.abspath(__file__))  

# Định nghĩa đường dẫn chính xác
path_board = os.path.join(base_dir, "..", "Testcases") 
path_checkpoint = os.path.join(base_dir, "..", "Checkpoints") 

def get_boards():
    os.chdir(path_board)  # chuyển thư mục làm việc
    list_boards = []  # Khởi tạo danh sách để lưu các ma trận (boards)
    for file in os.listdir():  # Duyệt qua các file trong thư mục
        if file.endswith(".txt"):  # Kiểm tra nếu file có phần mở rộng ".txt"
            #file_path = f"{path_board}\{file}"  # Tạo đường dẫn đầy đủ tới file
            file_path = os.path.join(path_board, file)
            board = get_board(file_path)  # Gọi hàm get_board để đọc nội dung file thành ma trận
            list_boards.append(board)
    return list_boards  # Trả về danh sách các ma trận


def get_check_points():
    os.chdir(path_checkpoint)  # đổi thư mục làm việc
    list_check_point = []
    for file in os.listdir():
        if file.endswith(".txt"):  # lấy ra tất cả các file txt
            #file_path = f"{path_checkpoint}\{file}"  # tạo đường dẫn đến file
            file_path = os.path.join(path_checkpoint, file)
            check_point = get_pair(file_path)
            list_check_point.append(check_point)
    return list_check_point


def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'


def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result


def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result  # trả về ma trận đã định dạng


def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result


maps = get_boards()
check_points = get_check_points()

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1500, 1100))
pygame.display.set_caption('Sokoban Tom & Jerry')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
assets_path = os.getcwd() + "\\..\\Assets"
os.chdir(assets_path)
person = pygame.image.load(os.getcwd() + '\\person.png')
person = pygame.transform.scale(person, (100, 100))
wall = pygame.transform.scale(pygame.image.load(os.getcwd() + '\\wall.webp'), (100, 100))
box0 = pygame.image.load(os.getcwd() + '\\box0.png')
box0 = pygame.transform.scale(box0, (95,95))
box1 = pygame.image.load(os.getcwd() + '\\box1.png')
box1 = pygame.transform.scale(box1, (95, 95))
target = pygame.transform.scale(pygame.image.load(os.getcwd() + '\\target.png'), (80, 80))
path = pygame.image.load(os.getcwd() + '\\path.png')
path = pygame.transform.scale(path, (100, 100))
arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png')
arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png')
init_background = pygame.transform.scale(pygame.image.load(os.getcwd() + '\\init_background.png'), (1500, 1100))
loading_background = pygame.transform.scale(pygame.image.load(os.getcwd() + '\\loading_background.png'), (1500, 1100))
found_background = pygame.transform.scale(pygame.image.load(os.getcwd() + '\\found_background.png'), (1500, 1100))
player_direction = "right"


def renderMap(board):
    width = len(board[0])
    height = len(board)
    #indent = (1000- width * 100) / 2.0
    indent = (1500- width * 100) / 5.0
    for i in range(height):
        for j in range(width):
            screen.blit(path, (j * 100 + indent, i * 100 + indent))
            if board[i][j] == '#':
                screen.blit(wall, (j * 100 + indent, i * 100 + indent))
            if board[i][j] == '$':
                screen.blit(box0, (j * 100 + indent, i * 100 + indent))
            if board[i][j] == '%':
                screen.blit(target, (j * 100 + indent, i * 100 + indent))
            #if board[i][j] == '@':
            #    screen.blit(person, (j * 100 + indent, i * 100 + indent))
            if board[i][j] == '@':
                if player_direction == "left":
                    flipped_person = pygame.transform.flip(person, True, False)
                    screen.blit(flipped_person, (j * 100 + indent, i * 100 + indent))
                else:
                    screen.blit(person, (j * 100 + indent, i * 100 + indent))
                

#def playerUpdateRender():
    


mapNumber = 0
algorithm = "Player"
sceneState = "init"
loading = False


def sokoban():
    running = True  # Biến điều khiển vòng lặp chính của trò chơi
    global sceneState, list_check_point  # Biến toàn cục
    global loading
    global algorithm
    global list_board
    global mapNumber
    stateLenght = 0  # Biến cục bộ lưu độ dài trạng thái
    currentState = 0  # Biến cục bộ lưu trạng thái hiện tại
    global list_board_win

    found = True  # Biến cục bộ để theo dõi trạng thái tìm thấy

    while running:  # Vòng lặp chính của trò chơi
        screen.blit(init_background, (0, 0))  # Vẽ nền ban đầu lên màn hình
        if sceneState == "init":
            initGame(maps[mapNumber])  # Khởi tạo trò chơi với bản đồ hiện tại
        if sceneState == "executing":
            list_check_point = check_points[mapNumber]  # Lấy điểm kiểm tra từ bản đồ
            # Chọn giữa người dùng chơi và máy chơi
            if algorithm == "Player":
                print("Player")
                list_board = maps[mapNumber]
            else:
                print("AStar")
                list_board = astar.AStart_Search(maps[mapNumber], list_check_point)

            if len(list_board) > 0:
                sceneState = "playing"
                stateLenght = len(list_board[0])
                currentState = 0
            else:
                sceneState = "end"
                found = False

        if sceneState == "loading":
            loadingGame()  # Hàm tải trò chơi
            sceneState = "executing"
        if sceneState == "end":
            if algorithm == "Player":
                foundGame(list_board) # Kết thúc trò chơi cho người chơi
            else:
                foundGame(list_board[0][stateLenght - 1]) # Kết thúc trò chơi cho AI

        if sceneState == "playing":
            clock.tick(4) # Điều chỉnh tốc độ trò chơi
            if algorithm == "Player":
                new_list_board = player.Player(list_board, list_check_point, pygame)
                # 🛑 Nếu sceneState bị đổi trong Player (vd: nhấn SPACE), thì dừng chơi
                if sceneState != "playing":
                    return  # hoặc break, tùy theo context bạn đặt đoạn này trong hàm nào

                list_board = new_list_board
                if np.all(list_board == True):
                    sceneState = "end"
                    list_board = list_board_win
                    found = True
                else:
                    renderMap(list_board)
                    list_board_win = list_board

            if algorithm == "AI":
                renderMap(list_board[0][currentState])
                currentState = currentState + 1
            if currentState == stateLenght:
                sceneState = "end"
                found = True
        for event in pygame.event.get(): # Xử lý các sự kiện người dùng
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and sceneState == "init":
                    if mapNumber < len(maps) - 1:
                        mapNumber = mapNumber + 1
                if event.key == pygame.K_LEFT and sceneState == "init":
                    if mapNumber > 0:
                        mapNumber = mapNumber - 1
                if event.key == pygame.K_RETURN:
                    if sceneState == "init":
                        sceneState = "loading"
                    if sceneState == "end":
                        sceneState = "init"
                # Nhấn phím SPACE để chuyển đổi thuật toán
                if event.key == pygame.K_SPACE and sceneState == "init":
                    if algorithm == "Player":
                        algorithm = "AI"
                    else:
                        algorithm = "Player"
                if event.key == pygame.K_SPACE and sceneState == "playing":
                    initGame(maps[mapNumber])
                    sceneState = "init"

        pygame.display.flip()
    pygame.quit()


def initGame(map):
    titleSize = pygame.font.Font('gameFont.ttf', 60)
    titleText = titleSize.render('Tom & Jerry - Sokoban', True, WHITE)
    titleRect = titleText.get_rect(center=(700, 70))
    screen.blit(titleText, titleRect)

    titleLevSize = pygame.font.Font('gameFont.ttf', 20)
    titleLevText = titleLevSize.render(str('Select level: [LEFT] or [RIGHT]'), True, WHITE)
    titleLevRect = titleLevText.get_rect(center=(1250, 200))  # căn chỉnh A star search
    screen.blit(titleLevText, titleLevRect)

    mapSize = pygame.font.Font('gameFont.ttf', 30)
    mapText = mapSize.render("Lv." + str(mapNumber + 1), True, WHITE)
    mapRect = mapText.get_rect(center=(1250, 250))
    screen.blit(mapText, mapRect)

    screen.blit(arrow_left, (1150, 238))
    screen.blit(arrow_right, (1330, 238))

    titleFunSize = pygame.font.Font('gameFont.ttf', 20)
    titleFunText = titleFunSize.render(str('Select game mode: [Space]'), True, WHITE)
    titleFunRect = titleFunText.get_rect(center=(1250, 440))  # căn chỉnh A star search
    screen.blit(titleFunText, titleFunRect)

    algorithmSize = pygame.font.Font('gameFont.ttf', 30)
    algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
    algorithmRect = algorithmText.get_rect(center=(1250, 470))  # căn chỉnh A star search

    screen.blit(algorithmText, algorithmRect)
    screen.blit(arrow_left, (1150, 460))
    screen.blit(arrow_right, (1330, 460))
    titleStartSize = pygame.font.Font('gameFont.ttf', 30)
    titleStartText = titleStartSize.render(str('Press Enter to start!!'), True, WHITE)
    titleStartRect = titleStartText.get_rect(center=(1250, 640))  # căn chỉnh A star search
    screen.blit(titleStartText, titleStartRect)
    renderMap(map)


def loadingGame():
    screen.blit(loading_background, (0, 0))
    fontLoading_1 = pygame.font.Font('gameFont.ttf', 40)
    text_1 = fontLoading_1.render('LOADING...', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(200, 1040))
    screen.blit(text_1, text_rect_1)


def foundGame(map):
    screen.blit(found_background, (0, 0))

    titleWSize = pygame.font.Font('gameFont.ttf', 60)
    titleWText = titleWSize.render('WELL DONE!!!', True, RED)
    titleWRect = titleWText.get_rect(center=(1200, 250))
   # screen.blit(titleWText, titleWRect)

    font_2 = pygame.font.Font('gameFont.ttf', 40)  # chỉnh phông chữ text_2
    text_2 = font_2.render('Press Enter to continue....', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(400, 1040))  # căn giữa
    screen.blit(text_2, text_rect_2)
   # renderMap(map)


def notfoundGame(notfound_background=None):
    screen.blit(notfound_background, (0, 0))
    font_2 = pygame.font.Font('gameFont.ttf', 20)
    text_2 = font_2.render('Press Enter to continue ;-;...', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(360, 640))
    screen.blit(text_2, text_rect_2)


def main():
    sokoban()


if __name__ == "__main__":
    main()
