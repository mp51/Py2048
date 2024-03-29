import curses
from curses import textpad
import math

class Display:
   def __init__(self, screen, box_width=10, box_height=4):
      self.screen = screen
      self.box_width = box_width
      self.box_height = box_height

      # Init colors
      curses.start_color()
      curses.use_default_colors()
      for i in range(0, curses.COLORS):
         curses.init_pair(i, curses.COLOR_BLACK, 255-i)

   def get_input(self):
      return self.screen.getch()

   def print_menu(self, menu):
      self.screen.clear()
      h, w = self.screen.getmaxyx()

      for idx, row in enumerate(menu.items):
         x = w//2 - len(row)//2
         y = h//2 - len(menu.items)//2 + idx

         if idx == menu.current_row_idx:
            self.screen.attron(curses.color_pair(1))
            self.screen.addstr(y, x, row)
            self.screen.attroff(curses.color_pair(1))
         else:
            self.screen.addstr(y, x, row)

      self.screen.refresh()


   def print_grid(self, numbers):
      self.screen.clear()
      sh, sw = self.screen.getmaxyx()
      y_offset = sh//2 - len(numbers)*self.box_height // 2
      x_offset = sw//2 - len(numbers)*self.box_width // 2

      for i, row in enumerate(numbers):
         for j, number in enumerate(row):
            # Rectangle border
            y_pos = y_offset + i*self.box_height
            x_pos = x_offset + j*self.box_width
            textpad.rectangle(self.screen, 
                              y_pos, x_pos, 
                              y_pos+self.box_height, x_pos+self.box_width)

            if number:
               # Color box
               color = int(math.log(number, 2))
               for row in range(self.box_height - 1):
                  filler = ' ' * (self.box_width-2)
                  self.screen.addstr(y_pos+row+1, x_pos+1, filler, curses.color_pair(color))
                  self.screen.refresh()

               # Number text
               num_text = str(number)
               y_pos += self.box_height//2
               x_pos += self.box_width//2 - len(num_text)
               self.screen.addstr(y_pos, x_pos, num_text, curses.color_pair(color))

      self.screen.refresh()

   def print_score(self, score):
      score_text = f'Score: {score}'
      _, sw = self.screen.getmaxyx()
      self.screen.addstr(1, sw//2 - len(score_text)//2, score_text)
      self.screen.refresh()

   def print_scoreboard(self, scores):
      self.screen.clear()
      sh, sw = self.screen.getmaxyx()
      count = len(scores)
      for row, score in enumerate(scores):
         score_text = f'{row+1}:\t\t{score}'
         self.screen.addstr(sh//2 - count//2 + row, int(sw/2.5), score_text)

   def print_message(self, message, clear=False):
      if clear:
         self.screen.clear()
      sh, sw = self.screen.getmaxyx()
      self.screen.addstr(sh//2, sw//2 - len(message)//2, message)
