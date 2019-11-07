import curses

class Menu:
   def __init__(self):
      self.items = ['Play', 'Scoreboard', 'Exit']
      self.current_row_idx = 0

   def choose(self, screen_input, display):
      while True:
         display.print_menu(self)
         key = screen_input.getch()

         if key == curses.KEY_UP and self.current_row_idx > 0:
            self.current_row_idx -= 1
         elif key == curses.KEY_DOWN and self.current_row_idx < len(self.items)-1:
            self.current_row_idx += 1
         elif key == curses.KEY_ENTER or key in [10, 13]:
            return self.items[self.current_row_idx]