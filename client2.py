import socket, pygame
from by_size import *
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, SERVER_IP, SERVER_PORT
from checkers.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def extract_reply(reply):
    print(reply)
    reply.split('~')
    return reply[0]


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def playing(game, sock):
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                send_with_size(sock, 'QUIT')
                return
            data = recv_by_size(sock)
            if data == 'TURN':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                game.update()

    pass


def main():
    client_socket = socket.socket()
    try:
        client_socket.connect(('127.0.0.1', 4001))
        print("Connected!")
    except Exception as E:
        print(f'cant connect bc: {E}')
        return

    run = True
    game = Game(WIN)
    while run:
        game.update()
        # if game.winner() is not None:
        #     print(game.winner())
        #     client_socket.close()
        #     run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                send_with_size(client_socket, 'EXIT')
                client_socket.close()
                run = False

            send_with_size(client_socket, 'PLAY')
            response = recv_by_size(client_socket)
            is_game = extract_reply(response)
            while is_game == 'WAIT':
                response = recv_by_size(client_socket)
                is_game = extract_reply(response)
            if is_game == 'PLAY':
                playing(game, client_socket)

    pygame.quit()


if __name__ == '__main__':
    main()
