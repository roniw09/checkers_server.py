import socket, threading
from by_size import *

players = []
sockets = []
all_to_die = False
first = False
red_turn = True
no_winner = True
DIVIDER = '~'
IP_PORT = ('0.0.0.0', 4001)


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
        players[id - 1][1] = False
        players[op_id - 1][1] = False
        first = False
        if result == 'EXIT':
            return 'EXIT'
        if result == 'ERR1':
            return 'ERR1'
        return 'OOKK'
    if code == 'WAIT':
        return 'WAIT'
    if code == 'EXIT':
        return 'EXIT'
    if code == 'MOVE':
        return 'OMOV' + DIVIDER + fields[1] + DIVIDER + fields[2] + DIVIDER + fields[3] + DIVIDER + fields[4]
    return 'No action'


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
        white_data = recv_by_size(sock)
        print("recieved")
        if white_data == b'':
            return 'EXIT'
        if 'OVER' in white_data:
            red_turn = True
            return
        if not red_turn:
            while white_data == '':
                white_data = recv_by_size(sock)

            fields = white_data.split(DIVIDER)
            print("white " + fields[0])
            if fields[0] == 'OVER':
                return
            reply = reply_by_code(fields, sock, id)
            print(reply)
            if reply == 'EXIT':
                send_with_size(opponent, 'OPLT')
                return reply
            red_turn = True
            send_with_size(opponent, reply)
            send_with_size(sock, 'NOTU')
            print("sent w")


def red_player(sock, id, opponent, op_id):
    """
    red player loop
    :param sock: white player socket
    :param id: white player socket id
    :param opponent: red player socket
    :param op_id: red player socket id
    :return:
    """
    global red_turn, no_winner
    while no_winner:
        print("current red turn: " + str(red_turn))
        red_data = recv_by_size(sock)
        print("recieved")
        if red_data == b'':
            return 'EXIT'
        if 'OVER' in red_data:
            return
        if red_turn:
            while red_data == '':
                red_data = recv_by_size(sock)

            fields = red_data.split(DIVIDER)
            print("red " + fields[0])
            if fields[0] == 'OVER':
                red_turn = True
                return
            reply = reply_by_code(fields, sock, id)
            print("before exit check")
            if reply == 'EXIT':
                send_with_size(opponent, 'OPLT')
                return reply
            red_turn = False
            send_with_size(opponent, reply)
            send_with_size(sock, 'NOTU')
            print("sent w")


def handle_client(client, id, addr):
    global all_to_die
    """
    handle a client
    :param client: client socket
    :param id: client id
    :param addr: client address
    :return:
    """
    print(f'connected client number {id}')
    while not all_to_die:
        data = recv_by_size(client)
        if data == b'':
            print('client disconnected')
            return
        fields = data.split(DIVIDER)
        response = reply_by_code(fields, client, id)
        if response == 'ERR1':
            print('error: cant do move')
            return
        if response == 'EXIT':
            print('client disconnected')
            return
        send_with_size(client, response)

    client.close()


def main():
    """
    main loop
    :return: void
    """
    global players, all_to_die, play
    srv_sock = socket.socket()
    srv_sock.bind(IP_PORT)

    srv_sock.listen(7)
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
        if i > 7:
            print('\nMain thread: going down for maintenance')
            break

    all_to_die = True

    if all_to_die:
        for t in players:
            t[0].join()
    print('Main thread: waiting to all clients to die')

    srv_sock.close()
    print('Bye ..')


if __name__ == '__main__':
    main()
