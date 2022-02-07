class KMP:
    def __init__(self,_sentence,_word):
        self.sentence = _sentence
        self.word = _word

    def getRandtabelle(self):
        return [(self.word[:a],self._getRand(self.word[:a])) for a in range(1,len(self.word)+1)]


    def calcAlgo(self):
        suchtextposition = 0
        raender = 0
        satzlaenge = len(self.sentence)
        wortlaenge = len(self.word)
        vergleiche = 0
        while suchtextposition <= satzlaenge - wortlaenge:
            cacheWord = self.word[:1]
            musterposition = raender if raender != -1 else 0
            matches = 0
            isMatched = True
            suchtextpositionCache = suchtextposition
            while isMatched:
                if cacheWord == self.word:
                    #print(f"Ende Index: {suchtextpositionCache-1}")
                    print(f"Vergleiche: {vergleiche}")
                    return True
                if self.sentence[suchtextpositionCache] == self.word[musterposition]:
                    matches += 1
                    suchtextpositionCache+=1
                    musterposition+=1
                    cacheWord = self.word[:musterposition]
                    vergleiche+=1
                else:
                    vergleiche+=1
                    isMatched = False

            raender = self._getRand(cacheWord)
            suchtextposition += matches if matches > 0 else 1








    def _getRand(self,_part):
        maxIndex = len(_part)-1
        laenge = round(len(_part)/2)
        ### ein buchstabe
        if laenge == 0:
            return -1
        countMax = 0
        firstIndex = 1
        for i in range(laenge+1 if len(_part)%2==1 and len(_part) != 3 else laenge):
            cacheFirst = _part[:firstIndex]
            cacheSecond = _part[maxIndex:]
            if cacheSecond == cacheFirst:
                if len(cacheFirst) > countMax:
                    countMax = len(cacheFirst)
            maxIndex -= 1
            firstIndex += 1
        return countMax

