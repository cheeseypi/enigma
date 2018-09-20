from abc import ABC, abstractmethod
import string
import sys

class EnigmaComponent(ABC):
    @abstractmethod
    def process(self, letter): raise NotImplementedError

class Plugboard(EnigmaComponent):
    def __init__(self):
        self.board1 = []
        self.board2 = []

    def plug_in(self, letter1, letter2):
        if letter1 in self.board1 or letter1 in self.board2:
            return False
        if letter2 in self.board1 or letter2 in self.board2:
            return False
        self.board1.append(letter1)
        self.board2.append(letter2)
        return True

    def process(self, letter):
        if letter in self.board1:
            letter = self.board2[self.board1.index(letter)]
        elif letter in self.board2:
            letter = self.board1[self.board2.index(letter)]
        return letter

    def __str__(self):
        return str([self.board1, self.board2])

class Rotor(EnigmaComponent):
    def __init__(self, defPosition = 0, table = string.ascii_lowercase):
        if defPosition >= 26:
            raise Exception("Invalid Position")
        self.position = defPosition
        self.table = table[defPosition+1:]+table[:defPosition+1]

    def advance(self):
        ntable = []
        for letter in self.table:
            ntable.append(
                string.ascii_lowercase[
                    (string.ascii_lowercase.index(letter) + 1) % 26
                ]
            )
        self.table = ntable
        self.position = self.position + 1
        if self.position == 26:
            self.position = 0
            return True
        return False

    def revprocess(self, letter):
        return string.ascii_lowercase[self.table.index(letter)]
    def process(self, letter):
        return self.table[string.ascii_lowercase.index(letter)]

class Reflector(EnigmaComponent):
    def process(self, letter):
        return string.ascii_lowercase[25-string.ascii_lowercase.index(letter)]

class Machine(EnigmaComponent):
    def __init__(self, rotor1=0, rotor2=0, rotor3=0, plugs={}):
        self.defaults = (rotor1, rotor2, rotor3, plugs)
        self.rotors = [Rotor(rotor1), Rotor(rotor2), Rotor(rotor3)]
        self.reflector = Reflector()
        self.plugboard = Plugboard()
        for key,val in plugs.items():
            self.plugboard.plug_in(key, val)

    def process(self, letter):
        if(self.rotors[2].advance()):
            if(self.rotors[1].advance()):
                self.rotors[0].advance()
        letter = self.plugboard.process(letter)
        letter = self.rotors[2].process(letter)
        letter = self.rotors[1].process(letter)
        letter = self.rotors[0].process(letter)
        letter = self.reflector.process(letter)
        letter = self.rotors[0].revprocess(letter)
        letter = self.rotors[1].revprocess(letter)
        letter = self.rotors[2].revprocess(letter)
        letter = self.plugboard.process(letter)
        return letter

    def reset(self):
        r1,r2,r3,plugs = self.defaults
        self.rotors = [Rotor(r1),Rotor(r2),Rotor(r3)]
        self.plugboard = Plugboard()
        for key,val in plugs.items():
            self.plugboard.plug_in(key, val)

if __name__ == '__main__':
  def process_string(machine, msg):
      msg = msg.lower()
      result = ''
      for letter in msg:
          if not letter in string.ascii_lowercase:
              continue
          result = result + machine.process(letter)
      return result
  machine = Machine()
  msg = "Hello, World"
  if len(sys.argv) >= 2:
      msg = sys.argv[1]
  processed = process_string(machine, msg)
  machine.reset()
  doubleprocessed = process_string(machine, processed)
  print(msg,processed,doubleprocessed)
