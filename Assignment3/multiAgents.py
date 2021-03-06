# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import util

from game import Agent

#class ReflexAgent(Agent):
#    """
#    A reflex agent chooses an action at each choice point by examining
#    its alternatives via a state evaluation function.
#
#    The code below is provided as a guide.  You are welcome to change
#    it in any way you see fit, so long as you don't touch our method
#    headers.
#    """
#
#
#    def getAction(self, gameState):
#        """
#        You do not need to change this method, but you're welcome to.
#
#        getAction chooses among the best options according to the evaluation function.
#
#        Just like in the previous project, getAction takes a GameState and returns
#        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
#        """
#        # Collect legal moves and successor states
#        legalMoves = gameState.getLegalActions()
#
#        # Choose one of the best actions
#        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
#        bestScore = max(scores)
#        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
#        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
#
#        "Add more of your code here if you want to"
#
#        return legalMoves[chosenIndex]
#
#    def evaluationFunction(self, currentGameState, action):
#        """
#        Design a better evaluation function here.
#
#        The evaluation function takes in the current and proposed successor
#        GameStates (pacman.py) and returns a number, where higher numbers are better.
#
#        The code below extracts some useful information from the state, like the
#        remaining food (newFood) and Pacman position after moving (newPos).
#        newScaredTimes holds the number of moves that each ghost will remain
#        scared because of Pacman having eaten a power pellet.
#
#        Print out these variables to see what you're getting, then combine them
#        to create a masterful evaluation function.
#        """
#        # Useful information you can extract from a GameState (pacman.py)
#        successorGameState = currentGameState.generatePacmanSuccessor(action)
#        newPos = successorGameState.getPacmanPosition()
#        newFood = successorGameState.getFood()
#        newGhostStates = successorGameState.getGhostStates()
#        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
#
#        "*** YOUR CODE HERE ***"
#        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        listOfActions = gameState.getLegalActions(0)    # Pac-Man's initial options
        bestAction = [None, float('-inf')]
        # Expanding the action-tree and using the minimax attribute
        for a in listOfActions:
            nextState = gameState.generateSuccessor(0, a)
            value = self.minValue(nextState, 0, 1)
            if value > bestAction[1]:
                bestAction = [a, value]
        return bestAction[0]    # return the optimal action

    # currentDepth keeps track of the depth of the player
    # currentIndex in order to identify the player
    def minValue(self, gameState, currentDepth, currentIndex):
        # For the Min players i.e. ghosts

        v = float('inf')
        listOfActions = gameState.getLegalActions(currentIndex)
        if len(listOfActions) == 0:     # i.e. terminal node
            return self.evaluationFunction(gameState)   # returns the utility
        if currentIndex == gameState.getNumAgents() - 1:    # Last ghost
            for a in listOfActions:
                nextState = gameState.generateSuccessor(currentIndex, a)
                v = min(v, self.maxValue(nextState, currentDepth + 1))
        else:
            for a in listOfActions:
                nextState = gameState.generateSuccessor(currentIndex, a)
                v = min(v, self.minValue(nextState, currentDepth, currentIndex + 1))
        return v

    def maxValue(self, gameState, currentDepth):
        # For the Max player i.e. Pac-Man

        if currentDepth == self.depth: return self.evaluationFunction(gameState)    # reached the depth limit
        v = float('-inf')
        listOfActions = gameState.getLegalActions(0)
        if len(listOfActions) == 0:     # i.e. terminal node
            return self.evaluationFunction(gameState)
        for a in listOfActions:
            nextState = gameState.generateSuccessor(0, a)
            v = max(v, self.minValue(nextState, currentDepth, 1))
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # return the optimal action within the depth
        return self.maxValue(gameState, 0, float('-inf'), float('inf'))

    def minValue(self, gameState, currentDepth, currentIndex, alfa, beta):
        v = float('inf')
        listOfActions = gameState.getLegalActions(currentIndex)
        if len(listOfActions) == 0:     # i.e. terminal node
            return self.evaluationFunction(gameState)
        if currentIndex == gameState.getNumAgents() - 1:    # Last ghost
            for a in listOfActions:
                nextState = gameState.generateSuccessor(currentIndex, a)
                v = min(v, self.maxValue(nextState, currentDepth + 1, alfa, beta))
                if v < alfa: return v   # prune
                beta = min(beta, v)
        else:
            for a in listOfActions:
                nextState = gameState.generateSuccessor(currentIndex, a)
                v = min(v, self.minValue(nextState, currentDepth, currentIndex + 1, alfa, beta))
                if v < alfa: return v   # prune
                beta = min(beta, v)
        return v

    def maxValue(self, gameState, currentDepth, alfa, beta):
        if currentDepth == self.depth: return self.evaluationFunction(gameState)    # reached depth limit
        listOfActions = gameState.getLegalActions(0)
        if currentDepth == 0:   # initial node
            if len(listOfActions) == 0: return [None, self.evaluationFunction(gameState)]   # No legal actions
            value_and_action = [None, float('-inf')]
            for a in listOfActions:
                nextState = gameState.generateSuccessor(0, a)
                value_and_action = max(value_and_action, [a, self.minValue(nextState, currentDepth, 1, alfa, beta)],
                                       key=lambda k: k[1])  # using the value parameter as key in the comparison
                alfa = max(alfa, value_and_action[1])
            return value_and_action[0]  # optimal action
        else:
            if len(listOfActions) == 0:     # no legal actions
                return self.evaluationFunction(gameState)
            v = float('-inf')
            for a in listOfActions:
                nextState = gameState.generateSuccessor(0, a)
                v = max(v, self.minValue(nextState, currentDepth, 1, alfa, beta))
                if v > beta: return v   # prune
                alfa = max(alfa, v)
            return v


#class ExpectimaxAgent(MultiAgentSearchAgent):
#    """
#      Your expectimax agent (question 4)
#    """
#
#    def getAction(self, gameState):
#        """
#        Returns the expectimax action using self.depth and self.evaluationFunction
#
#        All ghosts should be modeled as choosing uniformly at random from their
#        legal moves.
#        """
#        "*** YOUR CODE HERE ***"
#        util.raiseNotDefined()
#
#def betterEvaluationFunction(currentGameState):
#    """
#    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
#    evaluation function (question 5).
#
#    DESCRIPTION: <write something here so we know what you did>
#    """
#    "*** YOUR CODE HERE ***"
#    util.raiseNotDefined()
#
## Abbreviation
#better = betterEvaluationFunction
