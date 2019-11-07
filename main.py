import curses
from game import Game
from display import Display

if __name__ == '__main__':
   def main(screen):
      curses.curs_set(0)
      display = Display(screen)
      game = Game(4, display)
      game.show_menu()

   curses.wrapper(main)