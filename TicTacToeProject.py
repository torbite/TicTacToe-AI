import numpy as np
import random, copy
class board():
    state = np.array([[0,0,0],[0,0,0],[0,0,0]])
    turn = 1
    lastMove = (0,0)
    lastTurn = 1
    
    
        
    def getLegalMoves(self):
        moves = []
        for y in range(3):
            for x in range(3):
                if(self.state[y,x] == 0):
                    moves.append((x,y))
        return moves

    def checkIfItHasEnded(self):
        moves = self.getLegalMoves()
        itsov = False
        if len(moves) == 0:
            itsov = True
        lines = []
        columns = []
        diagonals = [[],[]]
        every = []
        a = 0
        b = 2
        for i in range(3):
            diagonals[0].append(self.state[i,i])
            diagonals[1].append(self.state[i,b])
            
            lines.append(self.state[i])
            columns.append(self.state[:,i])
            
            every.append(self.state[i])
            every.append(self.state[:,i])

            
            b -= 1
        every.append(diagonals[0])
        every.append(diagonals[1])
        #print(diagonals[0], diagonals[1])
        win1 = [1,1,1]
        win2 = [2,2,2]
        wins = [win1,win2]
        playerWon = 0
        
        for i in range(2):
            if(playerWon == 0):
                win = wins[i]
                for j in every:
                    #print(j, win)
                    if(list(j) == win):
                        
                        playerWon = win[0]
                        itsov = True
                        break
        return playerWon, itsov

    def makeMove(self, move):
        legalMoves = self.getLegalMoves()
        if move in legalMoves:
            x = move[0]
            y = move[1]
            self.state[y,x] = self.turn
            self.lastMove = move
            self.lastTurn = self.turn
            self.turn = 1 if self.turn == 2 else 2 
            
        else:
            print ("Invalid move")

    def showBoard(self):
        print(self.state)
        

    def unmakeMove(self, mv):
        self.turn = self.state[mv[1],mv[0]]
        self.state[mv[1],mv[0]] = 0

class bot():
    endings =[]
    def __init__(self, myTurna):
        self.myTurna = myTurna
    
    ag = 0
    ly = 0
    def getEval(self, board):
        
        numb = 0
        waslast = False
        a, b = board.checkIfItHasEnded()
        
        if b:
            
            #if not any(np.array_equal(board.state, ending) for ending in self.endings):
                
                #self.endings.append(copy.deepcopy(board.state))
                
            waslast = True
            #print(a)
            en = 2 if self.myTurna == 1 else 1
            if a ==self.myTurna:
                
                #board.showBoard()
                #print()
                win = 0
                return 1, 0, waslast
            elif a == en:
                
                #board.showBoard()
                #print()
                losses = 0
                return -1, 0, waslast
            else:
                
                #board.showBoard()
                #print()
                return 0, 0, waslast
        else:
            legalMoves = board.getLegalMoves()
            theTurn = board.turn
            
            ponctuation = -10 if self.myTurna == theTurn else 10
            
            for i in legalMoves:
                board.makeMove(i)
                self.ag+=1
                
                JOJ, wowieee,waslast = self.getEval(board)
                
                
                    
                if theTurn == self.myTurna:
                    #ponctuation +=self.getEval(board)
                    
                        
                    if ponctuation > JOJ and waslast == True:
                        numb = wowieee
                    ponctuation = max(ponctuation, JOJ)
                else:
                    if ponctuation < JOJ and waslast == True:
                        numb = wowieee
                    #ponctuation += self.getEval(board)
                    ponctuation = min(ponctuation, JOJ)
                if waslast:
                    waslast = False
                    if JOJ == 1:
                        numb += 1
                    elif JOJ == -1:
                        numb -= 1
                board.unmakeMove(i)
            return ponctuation, numb, waslast
    def getBestMove(self, board):
        a, b = board.checkIfItHasEnded()
        ag = 0
        if b == False:
            moves = board.getLegalMoves()
            best = -10
            bemovr = []
            bestNumb = -1000
            for i in moves:
                board.makeMove(i)
                #board.showBoard()
                #print()
                pc, numb, was = self.getEval(board)
                if pc > best:
                    best = pc
                    bemovr = [i]
                    print(numb)
                elif pc == best:
                    if numb > bestNumb:
                        best = pc
                        bemovr = [i]
                        bestNumb = numb
                    elif numb == bestNumb:
                        bemovr.append(i)
                    

                board.unmakeMove(i)
                self.ag+=1
            
            
            return random.choice(bemovr)



s = board()

gameGoing = True
boa2 = bot(2)
boa1 = bot(1)
playerNumber = int(input("Which number do you wish to play as? (1 or 2): "))
print()
while gameGoing:
    s.showBoard()
    print()
    if s.turn == playerNumber:
        y = int(input(f"Which layer do you want to play at? (turn = {s.turn}): ")) - 1
        x = int(input(f"Which column do you want to play at? (turn = {s.turn}): ")) - 1
        
        print()
        s.makeMove((x,y))
        
        
    else:
        if(s.turn == 1):
            s.makeMove(boa1.getBestMove(s))
        else:
            s.makeMove(boa2.getBestMove(s))
    winner, hasEnded = s.checkIfItHasEnded()
    if hasEnded:
        print()
        if winner != 0:
            print()
            s.showBoard()
            print(f"Player {winner} wins!")
            gameGoing = False
        else:
            print("The game was a draw!")

