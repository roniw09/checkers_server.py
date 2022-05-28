import socket, threading
from by_size import *

players = []
sockets = []
all_to_die = False
first = False
red_turn = True
white_turn = False
no_winner = True
DIVIDER = '~'


def reply_by_code(fields, sock, id):
    """
    return the reply by request
    :param fields: request fields
    :param sock: client socket
    :param id: client id
    :return: suited reply
    """
    global players, first
    code = fields[0]
    op_id = 0
    if code == 'PLAY':
        result = ''
        players[id - 1][1] = True
        opponent = None
        while opponent is None:
            for i in range(len(players)):
                if (i != id - 1) and players[i][1]:
                    opponent = sockets[i]
                    op_id = i + 1
                    break
        if first:
            send_with_size(sock, 'COLR' + DIVIDER + 'WHITE')
            result = white_player(sock, id, opponent, op_id)
        else:
            first = True
            send_with_size(sock, 'COLR' + DIVIDER + 'RED')
            result = red_player(sock, id, opponent, op_id)
        return result
    if code == 'WAIT':
        return 'WAIT'
    if code == 'EXIT':
        return 'EXIT'
    if code == 'MOVE':
        return 'OMOV' + DIVIDER + fields[1] + DIVIDER + fields[2] + DIVIDER + fields[3] + DIVIDER + fields[4]


def white_player(sock, id, opponent, op_id):
    """
    white player loop
    :param sock: white player socket
    :param id: white player socket id
    :param opponent: red player socket
    :param op_id: red player socket id
    :return:
    """
    global red_turn, no_winner
    while no_winner:
        print("current red turn: " + str(red_turn))
        while not red_turn:
            print(white_data)
            print("entered w")
            white_data = recv_by_size(sock)
            print("recieved")
            if white_data == b'':
                return 'EXIT'
            while white_data == '':
                print("in")
                white_data = recv_by_size(sock)
            fields = white_data.split(DIVIDER)
            print("white " + fields[0])
            reply = reply_by_code(fields, sock, id)
            print(reply)
            if reply == 'EXIT':
                return reply
            if reply == 'RWIN':
                return 'RWIN'
            print("entered")
            send_with_size(opponent, reply)
            send_with_size(sock, 'NOTU')
            print("sent w")
            red_turn = True
        print("current red turn: " + str(red_turn))
        while red_turn:
            white_data = recv_by_size(sock, id)
            if white_data == 'EXIT':
                return 'EXIT'


#    global red_turn, no_winner
#    while no_winner:
#        while not red_turn:
#            white_data = recv_by_size(sock)
#            if white_data == b'':
#                return 'EXIT'
#            while white_data == '':
#                print("in")
#                white_data = recv_by_size(sock)
#                print("out")
#            fields = white_data.split(DIVIDER)
#            print(fields[0], fields[1])
#            reply = reply_by_code(fields, sock, id)
#            if reply == 'EXIT':
#                return reply
#            if reply == 'RWIN':
#                return 'RWIN'
#            send_with_size(opponent, reply)
#            send_with_size(sock, 'NOTU')
#            red_turn = True
#        while red_turn:
#            white_data = recv_by_size(sock, id)
#            if white_data == 'EXIT':
#                return 'EXIT'
#        red_turn = False


def red_player(sock, id, opponent, op_id):
    """
    red player loop
    :param sock: red player socket
    :param id: red player socket id
    :param opponent: white player socket
    :param op_id: white player socket id
    :return:
    """
    global red_turn, no_winner

    while no_winner:
        while red_turn:
            red_data = recv_by_size(sock)
            if red_data == b'':
                return 'EXIT'
            while red_data == '':
                red_data = recv_by_size(sock)
            fields = red_data.split(DIVIDER)
            print(fields[0])
            reply = reply_by_code(fields, sock, id)
            print(reply)
            if reply == 'EXIT':
                return reply
            if reply == 'RWIN':
                return 'RWIN'
            print("entered")
            send_with_size(opponent, reply)
            send_with_size(sock, 'NOTU')
            print("sent r")
            red_turn = False
        while not red_turn:
            red_data = recv_by_size(sock, id)
            if red_data == 'EXIT':
                return 'EXIT'


def handle_client(client, id, addr):
    """
    handle a client
    :param client: client socket
    :param id: client id
    :param addr: client address
    :return:
    """
    print(f'connected client number {id}')
    if not all_to_die:
        data = recv_by_size(client)
        if data == b'':
            print('client disconnected')
            return
        fields = data.split(DIVIDER)
        response = reply_by_code(fields, client, id)
        if response == 'EXIT':
            print('client disconnected')
            return
        if response == 'PLAY':
            return
        send_with_size(client, response)


def main():
    """
    main loop
    :return: void
    """
    global players, all_to_die, play
    srv_sock = socket.socket()
    srv_sock.bind(('0.0.0.0', 4001))  # 192.168.5.249

    srv_sock.listen(2)
    i = 1
    print('\nMain thread: before accepting ...')
    while True:
        cli_sock, addr = srv_sock.accept()
        sockets.append(cli_sock)
        print(sockets)
        t = threading.Thread(target=handle_client, args=(cli_sock, i, addr))
        t.start()
        i += 1
        players.append([t, False])
        if i > 3:  # for tests change it to 4
            print('\nMain thread: going down for maintenance')
            break

    if all_to_die:
        for t in players:
            t[0].join()
    print('Main thread: waiting to all clients to die')

    srv_sock.close()
    print('Bye ..')


if __name__ == '__main__':
    main()
