import socket, pygame
from by_size import *
from checkers.constants import *
from checkers.game import Game

FPS = 60
OPEN_PIC = 'assets\Checkers entry.png'
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
DIVIDER = '~'


def extract_reply(reply):
   """
  return the response fields
  :param reply: server response
  :return: a list with the response fields
  """
   print(reply)
   return reply.split('~')


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
   clock = pygame.time.Clock()
   print('here1')
   if mode == 'RED':
       turn = True
   else:
       turn = False
   clock.tick(FPS)

   while play:
       if game.winner() is not None:
           print(game.winner())
           return game.winner()

       while turn:
           game.update()

           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   return 'EXIT'
               print('here3')
               if event.type == pygame.MOUSEBUTTONDOWN:
                   pos = pygame.mouse.get_pos()
                   row, col = get_row_col_from_mouse(pos)
                   goto_x, goto_y = game.select(row, col)
                   send_with_size(sock, 'MOVE' + DIVIDER + str(row) + DIVIDER + str(col) + DIVIDER + str(goto_x) + DIVIDER + str(goto_y))
                   print('here4')
                   data = recv_by_size(sock)
                   if data == '':
                       return 'EXIT'
                   fields = data.split(DIVIDER)
                   if fields[0] == 'NOTU':
                       turn = False
           while not turn:
               game.update()

               for event in pygame.event.get():
                   if event.type == pygame.QUIT:
                       return 'EXIT'
               data = recv_by_size(sock)
               if data == '':
                   return 'EXIT'
               fields = data.split(DIVIDER)
               if fields[0] == 'WAIT':
                   send_with_size(sock, 'WAIT')
                   data = recv_by_size(sock)
               if fields[0] == 'OMOV':
                   start_x, start_y = fields[1], fields[2]
                   end_x, end_y = fields[3], fields[4]
                   game.select(start_x, start_y)
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
               if is_game[0] == 'COLR':
                   opening.fill(TRANSPARENT)
                   result = playing(client_socket, is_game[1])

   pygame.quit()


if __name__ == '__main__':
   main()


