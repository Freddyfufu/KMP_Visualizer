import CalculateKMP
import Window
import tkinter as tk
from tkinter import ttk


kmp = CalculateKMP.KMP("BANANA UND ANANAS","ANANAS")
win = Window.Window(750,500)



print(kmp.calcAlgo())

win.root.mainloop()