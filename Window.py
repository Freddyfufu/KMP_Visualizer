import tkinter as tk
from tkinter import ttk

import CalculateKMP


class Window:
    def __init__(self, _height, _width):
        self.root = tk.Tk()
        self.root.resizable(False,False)
        self.vergleiche = 0
        self.vergleicheLabel = ttk.Label(self.root)
        self.currentRand = 0
        self.currentMatches = 0
        self.currentMusterPart = None
        self.musterposition = 0
        self.suchtextposition = 0

        self.kmp = None
        self.HEIGHT = _height
        self.WIDTH = _width
        self.root.geometry((f"{self.HEIGHT}x{self.WIDTH}"))
        self.root.title("Knuth-Morris-Pratt Visualizer")
        self.satzValue = None
        self.wortValue = None

        self.satzLabel = ttk.Label(self.root, text="Satz:")
        self.satzLabel.grid(column=0, row=0)
        self.satzEntry = ttk.Entry(self.root)
        self.satzEntry.grid(column=1, row=0)

        self.wortLabel = ttk.Label(self.root, text="Wort:")
        self.wortLabel.grid(column=0, row=1)

        self.wortEntry = ttk.Entry(self.root)
        self.wortEntry.grid(column=1, row=1)

        self.inputButton = ttk.Button(self.root, command=lambda: self.evalInput(
            [self.reset, self.showRandtabelle, self.initWidgets]), text="Bestätigen")
        self.inputButton.grid(column=1, row=2)

        self.randtabelleLabel = ttk.Label(self.root)
        self.randtabelleLabel.grid(row=3, column=1)
        self.randtabelleValueLabel = ttk.Label(self.root)
        self.randtabelleValueLabel.grid(row=3, column=2)
        self.suchLabel = ttk.Label(self.root)
        self.musterLabel = ttk.Label(self.root)
        self.suchtextLabels = []
        self.musterLabels = []
        self.weiterButton = ttk.Button(self.root)
        self.dontDeleteTheseLabels = []

        self.resetButton = ttk.Button(self.root,text="Reset",command=self.resetAll).grid(row=4,column=1)

    def reset(self):
        ### entferne alle labels
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.destroy()
        self.satzLabel = ttk.Label(self.root, text="Satz:")
        self.satzLabel.grid(column=0, row=0)
        self.wortLabel = ttk.Label(self.root, text="Wort:")
        self.wortLabel.grid(column=0, row=1)
        self.randtabelleLabel = ttk.Label(self.root)
        self.randtabelleLabel.grid(row=3, column=1)
        self.randtabelleValueLabel = ttk.Label(self.root)
        self.randtabelleValueLabel.grid(row=4, column=2)
        self.weiterButton = ttk.Button(self.root)
        self.suchLabel = ttk.Label(self.root)
        self.musterLabel = ttk.Label(self.root)
        self.weiterButton = ttk.Button(self.root)

    def resetAll(self):
        self.vergleiche = 0
        self.vergleicheLabel = ttk.Label(self.root)
        self.currentRand = 0
        self.currentMatches = 0
        self.currentMusterPart = None
        self.musterposition = 0
        self.suchtextposition = 0
        self.kmp = None
        self.satzValue = None
        self.wortValue = None
        self.reset()
        self.emptyEntry()

    def emptyEntry(self):
        self.satzEntry.delete(0,"end")
        self.wortEntry.delete(0,"end")

    ### bestätigen
    def evalInput(self, listeners):
        self.satzValue = self.satzEntry.get()
        self.wortValue = self.wortEntry.get()
        ### leere eingabe in einen von beiden feldern
        if self.satzValue == "" or self.wortValue == "":
            return 0
        self.kmp = CalculateKMP.KMP(self.satzValue, self.wortValue)
        ### callbacks
        for listener in listeners:
            listener()

    def showRandtabelle(self):
        self.randtabelleLabel.config(text="Randtabelle:")
        self.randtabelleValueLabel.config(text="\n".join([str(a) for a in self.kmp.getRandtabelle()]))

    def initWidgets(self):
        ### aktueller muster part
        self.vergleicheLabel = ttk.Label(self.root,text=f"Vergleiche: {self.vergleiche}").grid(row=2,column=2)
        self.suchLabel = ttk.Label(self.root, text="Suchtext: ").grid(row=0, column=2)
        self.musterLabel = ttk.Label(self.root, text="Muster: ").grid(row=1, column=2)
        self.suchtextLabels = [ttk.Label(self.root, text=self.satzValue[a]).grid(row=0, column=a + 3) for a in
                               range(len(self.satzValue))]
        self.musterLabels = [ttk.Label(self.root,background="blue" if a < self.musterposition else "", text=self.wortValue[a]).grid(row=1, column=a + 3 +self.suchtextposition - self.currentRand) for a in
                             range(len(self.wortValue))]
        self.weiterButton = ttk.Button(self.root, text="Weiter", command=self.doStep if not self.isOver() else self.zuende)
        self.weiterButton.grid(row=3, column=2)
        self.currentMusterPart = "".join([a.cget("text") for a in self.getBlueLabels()])
        self.randMatches = len(self.currentMusterPart)


    def zuende(self):
        ttk.Label(self.root,text="ZUENDE").grid(row=5,column=2)
        self.weiterButton["state"] = "disabled"

    def isWordFound(self):
        return self.currentMusterPart == self.wortValue

    def getBlueLabels(self):
        li = []
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Label):
                try:
                    if str(widget.cget("background")) == "blue":
                        li.append(widget)
                        self.currentMusterPart = widget.cget("text")
                except:
                    pass
        return li

    def isOver(self):
        return self.suchtextposition == len(self.satzValue) - len(self.wortValue)+1

    def getAlleLabels(self):
        li = []
        for widget in self.root.winfo_children():
            if isinstance(widget,ttk.Label):
                li.append(widget)
        return li

    def doStep(self):
        if self.isWordFound() or self.isOver():
            self.weiterButton.config(state="disabled")
            return
        self.vergleiche += 1
        if self.isMatch():
            self.musterposition+=1
            self.currentMatches+=1
        ### missmatch
        else:
            self.suchtextposition += self.currentMatches if self.currentMatches != 0 else 1
            rand = self.kmp._getRand(self.currentMusterPart) if self.currentMusterPart != "" else -1
            self.currentRand = rand if rand != -1 else 0
            self.currentMatches = 0
            self.musterposition =  rand if rand != -1 else 0
        self.reset()
        self.showRandtabelle()
        self.initWidgets()

    def isMatch(self):
        return self.wortValue[self.musterposition] == self.satzValue[self.suchtextposition+self.musterposition - self.currentRand]


    def calcAlgo(self):
        self.suchtextposition = 0
        raender = 0
        satzlaenge = len(self.satzValue)
        wortlaenge = len(self.wortValue)
        vergleiche = 0
        while self.suchtextposition <= satzlaenge - wortlaenge:
            cacheWord = self.wortValue[:1]
            self.musterposition = raender if raender != -1 else 0
            matches = 0
            isMatched = True
            suchtextpositionCache = self.suchtextposition
            while isMatched:
                if cacheWord == self.wortValue:
                    # print(f"Ende Index: {suchtextpositionCache-1}")
                    print(f"Vergleiche: {vergleiche}")
                    return True
                if self.satzValue[suchtextpositionCache] == self.wortValue[self.musterposition]:
                    matches += 1
                    suchtextpositionCache += 1
                    self.musterposition += 1
                    cacheWord = self.wortValue[:self.musterposition]
                    vergleiche += 1
                else:
                    vergleiche += 1
                    isMatched = False

            raender = self.kmp._getRand(cacheWord)
            self.suchtextposition += matches if matches > 0 else 1