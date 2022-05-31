import socket, pygame
import time
from by_size import *
from checkers.constants import *
from checkers.game import Game

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
DIVIDER = '~'
IP_PORT = ('192.168.0.195', 4001)


def extract_reply(reply):
    """
   return the response fields
   :param reply: server response
   :return: a list with the response fields
   """
    print(reply)
    return reply.split('~')


def check_winner(game):
    if game.winner() is not None:
        print(game.winner())
        if game.winner() == RED:
            return True, 'RED'
        elif game.winner() == WHITE:
            return True, 'WHITE'
    return False, 'BLANC'


def get_row_col_from_mouse(pos):
    """
   calc in which row and column the mouse is in
   :param pos: current mouse position (a tuple with x and y)
   :return: the row and the column
   """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def playing(sock, mode):
    """
   the game itself
   :param sock: client sock
   :return: not finished, but suppose to return who won
   """
    play = True
    game = Game(WIN)

    turn = None
    if mode == 'RED':
        pic = display_img(WIN, RED_START)
        turn = True
        time.sleep(2)
    else:
        pic = display_img(WIN, WHITE_START)
        turn = False
        time.sleep(2)
    WIN.fill(TRANSPARENT)

    while play:
        pygame.display.update()
        pos_str = ''
        row_col = []
        fields = []

        is_winner, color = check_winner(game)
        if is_winner:
            return color

        while turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'EXIT'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    row_col.append(row)
                    row_col.append(col)
                    status, end_xy = game.select(row, col)
                    print("here")
                    if end_xy != (0, 0):
                        print("!!!!!!!!!!!!!!ENTER")
                        end_row, end_col = end_xy
                        pos_str = str(row_col[0]) + DIVIDER + str(row_col[1]) + DIVIDER + str(end_row) + DIVIDER + str(
                            end_col)
                        print(f"!!!!!!!!!!!!! POS STR: {pos_str}")
                game.update()
                if len(pos_str) > 0:
                    send_with_size(sock, 'MOVE' + DIVIDER + pos_str)
                    data = recv_by_size(sock)
                    print(data)
                    if data == '':
                        return 'EXIT'
                    fields = data.split(DIVIDER)
                    if fields[0] == 'NOTU':
                        turn = False

        is_winner, color = check_winner(game)
        if is_winner:
            return color

        while not turn:
            game.update()
            print("entered not turn")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'EXIT'
            data = recv_by_size(sock)
            fields = data.split(DIVIDER)
            if fields[0] == 'OPLT':
                return 'OPLT'
            if fields[0] == 'OMOV':
                start_x, start_y = int(fields[1]), int(fields[2])
                end_x, end_y = int(fields[3]), int(fields[4])
                game.select(start_x, start_y)
                game.update()
                game.select(end_x, end_y)
                game.update()
                turn = True


def display_img(screen, img):
    """
   display an image onto screen
   :param screen: the screen
   :param img: the image path
   :return: image itself
   """
    to_show = pygame.image.load(img)
    screen.blit(to_show, (0, 0))
    pygame.display.flip()
    return to_show


def main():
    """
   main loop
   :return: void
   """
    client_socket = socket.socket()
    try:
        client_socket.connect(IP_PORT)
        print("Connected!")
        run = True
        result = ''
        while run:
            pic = display_img(WIN, OPEN_PIC)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or result == 'EXIT':
                    send_with_size(client_socket, 'EXIT')
                    client_socket.close()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 147 < x < 653 and 375 < y < 524:
                        send_with_size(client_socket, 'PLAY')
                        response = recv_by_size(client_socket)
                        is_game = extract_reply(response)
                        while is_game[0] == 'WAIT':
                            response = recv_by_size(client_socket)
                            is_game = extract_reply(response)
                        if is_game[0] == 'COLR':
                            pic.fill(TRANSPARENT)
                            result = playing(client_socket, is_game[1])
                            WIN.fill(TRANSPARENT)
                            if result == 'RED':
                                pic = display_img(WIN, RED_WON)
                            if result == 'WHITE':
                                pic = display_img(WIN, WHITE_WON)
                            if result == 'EXIT':
                                WIN.fill(TRANSPARENT)
                                send_with_size(client_socket, 'EXIT')
                                run = False
                                break
                            send_with_size(client_socket, 'OVER')
                            data = recv_by_size(client_socket)
                            if data != 'OOKK':
                                run = False
                                print("ERRO")
                                break
                            time.sleep(5)

        client_socket.close()
    except Exception as E:
        print(f'cant connect bc: {E}')
        return
    pygame.quit()


if __name__ == '__main__':
    main()
