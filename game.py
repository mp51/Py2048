import random
import curses

from display import Display
from menu import Menu
from scoreboard import ScoreBoard


class Game:
   generated_numbers = [2, 4]
   def __init__(self, size, display):
      self.size = size
      self.menu = Menu()
      self.display = display
      self.scoreboard = ScoreBoard('scores')
      self.numbers = []
      self.score = 0

   def show_menu(self):
      while True:
         entry_selected = self.menu.choose(self.display)

         if entry_selected == self.menu.items[0]: # Play
            self.play()
         elif entry_selected == self.menu.items[1]: # Scoreboard
            self.display.print_scoreboard(self.scoreboard.high_scores)
            self.display.get_input()
         elif entry_selected == self.menu.items[2]: # Exit
            break

   def play(self):
      self.numbers = [[None for i in range(self.size)] for j in range(self.size)]
      self.score = 0

      # Generate 2 initial numbers:
      for _ in range(2):
         num, i, j = self.generate_number()
         self.numbers[i][j] = num

      # Game loop
      while True:
         self.display.print_grid(self.numbers)
         self.display.print_score(self.score)

         direction = self.display.get_input()
         if direction in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            self.move_numbers(direction)

            num, i, j = self.generate_number()

            # Game over condition - grid is full
            if num is None:
               self.display.print_message('Game Over! Press q to return to menu.')
               self.scoreboard.add_score(self.score)
               while self.display.get_input() != ord('q'):
                  pass
               break

            self.numbers[i][j] = num

   def get_column(self, col_num):
      column = [row[col_num] for row in self.numbers]
      return column

   def set_column(self, col_num, column):
      for i, row in enumerate(self.numbers):
         row[col_num] = column[i]

   def process_numbers(self, numbers_list):
      numbers = [number for number in numbers_list if number is not None]

      # Merge equal numbers
      i = 0
      while i < len(numbers) - 1:
         if numbers[i] == numbers[i+1]:
            numbers[i] *= 2
            self.score += numbers[i]
            del(numbers[i+1])
            i += 1
         i += 1
      
      # Append empty numbers to match the initial size
      while len(numbers) < self.size:
         numbers.append(None)

      return numbers

   def move_numbers(self, direction):
      if direction == curses.KEY_DOWN:
         for col_num in range(self.size):
            column = self.get_column(col_num)
            column.reverse()
            column = self.process_numbers(column)
            column.reverse()
            self.set_column(col_num, column)

      elif direction == curses.KEY_UP:
         for col_num in range(self.size):
            column = self.get_column(col_num)
            column = self.process_numbers(column)
            self.set_column(col_num, column)

      elif direction == curses.KEY_RIGHT:
         for row_num in range(self.size):
            row = self.numbers[row_num]
            row.reverse()
            row = self.process_numbers(row)
            row.reverse()
            self.numbers[row_num] = row

      elif direction == curses.KEY_LEFT:
         for row_num in range(self.size):
            self.numbers[row_num] = self.process_numbers(self.numbers[row_num])
            
   def is_grid_full(self):
      for row in self.numbers:
         if None in row:
            return False

      return True

   def generate_number(self):
      if self.is_grid_full():
         return None, None, None

      # Random number
      num = Game.generated_numbers[random.randint(0, 1)]

      # Random position
      i = None
      while i is None:
         i = random.randint(0, self.size-1)
         j = random.randint(0, self.size-1)
         if self.numbers[i][j] is not None:
            # The chosen position is not empty, generate another one
            i = None

      return num, i, j
