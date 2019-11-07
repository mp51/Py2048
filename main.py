import curses
from game import Game

if __name__ == '__main__':
   def main(screen):
      curses.curs_set(0)
      game = Game(screen, 4)
      game.show_menu()

   curses.wrapper(main)