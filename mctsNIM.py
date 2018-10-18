import random
import math
from random import choice



# game specific logic/states - this is the "state manager" that is required in the exercise desc.
#
# gameover, pieces, removemax, next states, randomPlay, etc
#
class GameManager:
    def __init__(self, player=1, numPieces=8, removeMax=3):
        self.player = player  #which players turn
        
        #NIM specific
        self.numPieces = numPieces
        self.removeMax = removeMax

    def getVisitCount(self):
        return self.visitCount

    def getWinCount(self):
        return self.winCount


    def getNumPieces(self):
        return self.numPieces

    #NIM specific
    def gameIsOver(self):
        return (self.numPieces <= 0)


    #NIM specific
    def getAllPossibleNextStates(self):
        numNextStates = self.removeMax
        nextStates = []
        nextPlayer = self.switchPlayer(self.player)
        for i in range (1, numNextStates + 1):
            if self.numPieces - i < 0:
                break
                
            piecesLeft = self.numPieces - i
            nextStates.append(State(player=nextPlayer, numPieces=piecesLeft, removeMax=self.removeMax))
        return nextStates



    def getPlayer(self):
        return self.player

    def setPlayer(self, player):
        self.player = player


    
    #get a list of possible positions on the 'board' and play a random move
    def randomPlay(self):
        nextStates = self.getAllPossibleNextStates()
        randomChoice = nextStates[random.randint(0, len(nextStates) - 1)]
        return randomChoice

    def switchPlayer(self, player):
        return 3 - player


#
#
# Every node has a state
#
# keeps track of the state of the game AND the state of the Nodes
#
class State:
    def __init__(self, player=1, numPieces=8, removeMax=3):

        #MCTS states
        self.visitCount = 1
        self.winCount = 0
        #MCTS states


        #game states
        self.gameManager = GameManager(numPieces=numPieces, removeMax=removeMax, player=player)
        #game states

    def __str__(self):
        return ' ,  '.join(['( {key} = {value} )'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


    def getVisitCount(self):
        return self.visitCount

    def getWinCount(self):
        return self.winCount


    def getNumPieces(self):
        return self.gameManager.getNumPieces()


    def gameIsOver(self):
        return (self.getNumPieces() <= 0)



    def getAllPossibleNextStates(self):
        return self.gameManager.getAllPossibleNextStates()



    def getPlayer(self):
        return self.gameManager.getPlayer()

    def setPlayer(self, player):
        self.gameManager.setPlayer(player)

    def randomPlay(self):
        return self.gameManager.randomPlay()

    def incrementVisitCount(self):
        self.visitCount += 1

    def incrementWinCount(self):
        self.winCount += 1

    def decrementWinCount(self):
        self.winCount -= 1

    #switch from 1 to 2 and vice versa
    def switchPlayer(self, player):
        return self.gameManager.switchPlayer(player)




#
# Each node keeps track of relationship between nodes/states
#
#
class Node:

    #initalize node
    def __init__(self, parentNode=None, state=State()):
        self.parentNode = parentNode
        self.state = state
        self.childNodes = []

    def __str__(self):
        return ' ,  '.join(['( {key} = {value} )'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
    
    def getParent(self):
        return self.parentNode

    def setParent(self, parentNode):
        self.parentNode = parentNode

    def getChildren(self):
        return self.childNodes

    def setChildren(self, childNodes):
        self.childNodes = childNodes

    #add a childNode
    def addChild(self, childNode=None):
        self.childNodes.append(childNode)
    
    #choose a random childnode
    def getRandomChildNode(self):
        return self.childNodes[random.randint(0, len(self.childNodes) - 1)]

    #return the childnode with the highest score
    def getChildWithMaxScore(self, node):
        return UCT(node)

    



#
# A search tree consisting of connected nodes with states
#
#
class Tree:

    #initalize Tree
    def __init__(self, rootNode = Node()):
        self.rootNode = rootNode
    
    def getRootNode(self):
        return self.rootNode

    def setRoot(self, node):
        self.rootNode = node
    
    #add childnode to a parentnode
    def addChildToANode(self, parent, child):
        parent.getChildren().append(child)




# Main system for running x number of games
class NIMSimulator:
    def __init__(self, numGames = 100, numPieces = 30, removeMax = 3, verbose=True, numberOfSimulations = 10, player=1):
        self.numGames = numGames
        self.numPieces = numPieces
        self.removeMax = removeMax

        #if the system should print the game progress to the console
        self.verbose = verbose

        # flag for determining which player should start
        # 1 = player1,   2 = player2,   3 = random
        self.startingPlayer = player
        self.players = [1, 2]
        
        self.numberOfSimulations = numberOfSimulations

    def run(self):

        print("Starting up..  Playing " + str(self.numGames) + " games:")
      

        #pick random player if set to random
        if self.startingPlayer == 3:
            player = choice(self.players)
        else:
            player = self.startingPlayer


        startNode = Node(state=State(player=player, numPieces=self.numPieces, removeMax=self.removeMax))
        mcts = MCTS(numberOfSimulationsPerMove=self.numberOfSimulations)
      
        player = startNode.getState().getPlayer()

        startNodeCopy = startNode
        player1Wins = 0
        player2Wins = 0
        player1Starts = 0
        player2Starts = 0

        gc = 1
        for game in range(0, self.numGames):
            #Start of a game

            startNode = startNodeCopy

            # random starting player if random is set
            if self.startingPlayer == 3:
                newPlayer = choice(self.players)
                if newPlayer != player: 
                    player = newPlayer
                    changePlayer(startNode)
                    
                

            startingPlayer = startNode.getState().getPlayer()
        
            if startingPlayer == 1:
                player1Starts += 1
            else: 
                player2Starts += 1

            print("\n\n\n --- Game number " + str(gc))
            print("\n There are  " + str(self.numPieces) + " pieces placed on the table. Player " + str(startingPlayer) + " starts the game." )



            while not startNode.getState().gameIsOver():
  

                player = startNode.getState().getPlayer()

                nextNode = mcts.findNextMove(startNode, player, startingPlayer)
                if self.verbose: self.printMove(startNode, nextNode, player)
                if nextNode.getState().gameIsOver():

                    if self.verbose: print("\nPlayer " + str(player) + " won! \n")
                    
                    if player == 1: 
                        player1Wins += 1
                    else:
                        player2Wins += 1
              

                startNode = nextNode

                if nextNode.getState().gameIsOver():
                    break
            gc += 1
               

            
        #print result of all games
        print("\nPlayer 1 started " + str(player1Starts) + " games and won " + str(player1Wins) + " of "  + str(self.numGames) + " games!   " + str((player1Wins/self.numGames*100)) + " % ")
        print("Player 2 started " + str(player2Starts) + " games and won " + str(player2Wins) + " of "  + str(self.numGames) + " games!   " + str((player2Wins/self.numGames*100)) + " % ")
        print("\n")
     

                
    def printMove(self, previousState, nextState, player):
        piecesRemoved = previousState.getState().getNumPieces() - nextState.getState().getNumPieces()
        print("Player " + str(player) + " removed  " + str(piecesRemoved) + " pieces.  " + str(nextState.getState().getNumPieces()) + " pieces left !")

















# Monte Carlo Tree Search class
#
# Basically in charge of choosing and learning.
#
# Finds the next move and updates the Q values in the search tree while playing
#
class MCTS:
    def __init__(self, numberOfSimulationsPerMove = 300):
        self.numberOfSimulationsPerMove = numberOfSimulationsPerMove


    def findNextMove(self, node, player, startingPlayer):   

      
        rootNode = node
        rootNode.getState().setPlayer(player)




        simulations = self.numberOfSimulationsPerMove

        while simulations > 0:
     
            #SELECTION
            selectedNode = self.selectNode(rootNode, player, startingPlayer)
            #print("after selectNode")

            #EXPANSION
            selectedNode = self.expandNode(selectedNode)
       

            #SIMULATION
            if len(selectedNode.getChildren()) > 0:
                selectedNode = selectedNode.getRandomChildNode()

            winner = self.simulateRandomPlayout(selectedNode)
       


            #UPDATE (backpropagate)
            self.backpropagate(selectedNode, winner, startingPlayer)
      

            simulations = simulations - 1

    

        selectedMove = chooseMostVisitedPath(rootNode, player, startingPlayer)

        return selectedMove


    # simulates a game until game over and returns the winner.
    # uses the 'default policy' which in this case is random picks 
    def simulateRandomPlayout(self, node):
        currentPlayer = node.getState().getPlayer()
        tempNode = node
        tempState = tempNode.getState()
    
        if(tempState.gameIsOver()):
            #winner was the one who took the action that led to game over
            winner = 3 - currentPlayer
            return winner
         
        while not tempState.gameIsOver():
            if (tempState.gameIsOver()):
                winner = 3 - tempState.getPlayer()
                return winner
            tempState = tempState.randomPlay()
            tempState.switchPlayer(tempState.getPlayer())
        

    # propagate the result back upwards to all parent states/nodes
    def backpropagate(self, selectedNode, winner, startingPlayer):
        tempNode = selectedNode
        while tempNode != None:
            tempNode.getState().incrementVisitCount()
   
            #update wincount for states
            if(tempNode.getState().getPlayer() != winner):
                tempNode.getState().incrementWinCount()
            tempNode = tempNode.getParent()
       

    # selects next node based on the 'tree policy' - uses UCB1 function to determine values 
    def selectNode(self, rootNode, player, startingPlayer):
        node = rootNode
        if node is not None:
            while len(node.getChildren()) is not 0:
                newNode = UCT(node, player, startingPlayer, True)
                node = newNode
        return node

    #expands chosen node (adds childnodes of possible next states)
    def expandNode(self, node):
        possibleNextStates = node.getState().getAllPossibleNextStates()
        tempNode = node
        for state in possibleNextStates:
            childNode = Node(state=state)
            childNode.setParent(tempNode)
            tempNode.addChild(childNode)
           
        return tempNode
          

#misleading name, actually chooses based on wincount/visitcount
def chooseMostVisitedPath(node, player, startingPlayer):
    children = node.getChildren()
    temp = -999999999
    choice = None

    for child in children:
        if child.getState().getWinCount() / child.getState().getVisitCount() >= temp:
            temp = child.getState().getWinCount() / child.getState().getVisitCount()
            choice = child
        

    return choice


# UCT function to determine values in Selection phase.
#  uses the "upper confidence bound" method
# 
def UCT(node, player, startingPlayer, rollout):
    parentVisits = node.getState().getVisitCount()
    explorationParam = 1 #math.sqrt(2)  'c'
    
    if parentVisits == 0:
        parentVisits = parentVisits + 1

    children = node.getChildren()
    selectedNode = None
    if player == startingPlayer:
        tempMax = -9999999
        #choose max
     
        for childNode in children:
            exploitationTerm = childNode.getState().getWinCount() / (childNode.getState().getVisitCount() + 1)
            
            #ucb1 function
            value = exploitationTerm +  explorationParam * math.sqrt((math.log(parentVisits))/(1 + childNode.getState().getVisitCount()))
           
            if value >= tempMax:
                tempMax = value
                selectedNode = childNode
    else:
        tempMax = 99999999
        #choose min
        for childNode in children:
            exploitationTerm = childNode.getState().getWinCount() / (childNode.getState().getVisitCount() + 1)
            
            #ucb1 function
            value = exploitationTerm +  explorationParam * math.sqrt((math.log(parentVisits))/(1 + childNode.getState().getVisitCount()))
      
            if value <= tempMax:
                tempMax = value
                selectedNode = childNode
    return selectedNode




# method for changing player - actually flips the player in every node in the tree
def changePlayer(node):
    newPlayer = 3 - node.getState().getPlayer()
    node.getState().setPlayer(newPlayer)
    childNodes = node.getChildren()
    if len(childNodes) > 0:
        for node in childNodes:
            changePlayer(node)





# entry for starting the simulator
def main():
   sim = NIMSimulator(numGames=3, numPieces=99, removeMax=6, verbose=True
        ,numberOfSimulations = 100, player=1)
   sim.run()




if __name__ == '__main__':
    main()
 



