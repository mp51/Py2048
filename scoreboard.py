from array import array

class ScoreBoard:
   def __init__(self, filename, items_limit=15):
      self.filename = filename
      self.high_scores = [0 for _ in range(items_limit)]
      self.load_from_file()

   def add_score(self, score):
      self.high_scores.append(score)
      self.high_scores.sort(reverse=True)
      del(self.high_scores[-1])
      self.save_to_file()

   def save_to_file(self):
      with open(self.filename, 'wb') as f:
         arr = array('Q', self.high_scores)
         arr.tofile(f)

   def load_from_file(self):
      try:
         with open(self.filename, 'rb') as f:
            arr = array('Q', [])
            arr.fromfile(f, len(self.high_scores))
            self.high_scores = arr.tolist()
      except FileNotFoundError:
         pass
