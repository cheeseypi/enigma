from tkinter import *
import os

from enigma import Machine

keyOrder = 'qwertyuiop\nasdfghjkl\nzxcvbnm'

os.system('xset r off')

machine = Machine()

letters = {}
isAKeyDown = False
curKey = ''

def keydown(e):
    global isAKeyDown
    global curKey
    global letters
    global machine
    if isAKeyDown or e.char not in keyOrder:
        return
    try:
        isAKeyDown = True
        curKey = machine.process(e.char)
        letters[curKey].config(bg='red')
    except KeyError:
        pass
def keyup(e):
    global isAKeyDown
    global curKey
    global letters
    global machine
    try:
        letters[curKey].config(bg='white')
        isAKeyDown = False
    except KeyError:
        pass

root = Tk()
frame = Frame(root, width=800, height=600)
col = 0
row = 0
for ch in list(keyOrder):
    if ch == '\n':
        col = 0
        row = row + 1
        continue
    temp = Label(frame, text=ch)
    temp.grid(row=row, column=col)
    letters[ch] = temp
    col = col + 1
frame.bind("<KeyPress>", keydown)
frame.bind("<KeyRelease>", keyup)
frame.grid()
frame.focus_set()
root.mainloop()
os.system('xset r on')
