import socket, pygame
from by_size import *
from checkers.constants import *
from checkers.game import Game

FPS = 60
OPEN_PIC = 'assets\Checkers entry.png'
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def extract_reply(reply):
    print(reply)
    return reply.split('~')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def playing(sock):
    play = True
    game = Game(WIN)
    clock = pygame.time.Clock()

    code = extract_reply(recv_by_size(sock))
    turn = None
    if code == 'FRST':
        turn = True
    else:
        turn = False
    while play:
        clock.tick(FPS)

        if game.winner() is not None:
            print(game.winner())
            return game.winner()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'EXIT'

            if event.type == pygame.MOUSEBUTTONDOWN and turn:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                send_with_size(sock, 'MOVE' + '~' + row + col)
                game.select(row, col)
                turn = not turn
            # if not turn:
            #     recv_by_size(s)

            else:
                recv_by_size(sock)
                # game.select(row, col)

        game.update()
    pass


def display_img(screen, img):
    to_show = pygame.image.load(img)
    screen.blit(to_show, (0, 0))
    pygame.display.flip()
    return to_show


def main():
    client_socket = socket.socket()
    try:
        client_socket.connect(('192.168.0.133', 4001))
        print("Connected!")
    except Exception as E:
        print(f'cant connect bc: {E}')
        return

    opening = display_img(WIN, OPEN_PIC)
    run = True
    result = ''
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or result == 'EXIT':
                send_with_size(client_socket, 'EXIT')
                client_socket.close()
                run = False
            else:
                send_with_size(client_socket, 'PLAY')
                response = recv_by_size(client_socket)
                is_game = extract_reply(response)
                while is_game[0] == 'WAIT':
                    response = recv_by_size(client_socket)
                    is_game = extract_reply(response)
                if is_game[0] == 'PLAY':
                    opening.fill(TRANSPARENT)
                    result = playing(client_socket)

    pygame.quit()


if __name__ == '__main__':
    main()