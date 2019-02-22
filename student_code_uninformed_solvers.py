from solver import *
import queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        #print(self.currentState.state)
        if self.victoryCondition == self.currentState.state:
            return True


        moves = self.gm.getMovables()
        #if moves:
            #for i in moves:
                #print(i)

        if not self.currentState.children and moves:
            self.findChildren(self.currentState)

        if self.currentState.children:
            child = self.currentState.children[0]
            self.gm.makeMove(child.requiredMovable)
            self.visited[child] = True
            self.currentState = child
            #print(str(child.requiredMovable) + "child")

        else:
            #print("touch")
            self.gm.reverseMove(self.currentState.requiredMovable)
            parent = self.currentState.parent
            self.currentState = parent
            found = False
            while parent and not found:
                for i in range(0, len(parent.children) - 1):
                    if parent.children[i] not in self.visited.keys():
                        self.gm.makeMove(parent.children[i].requiredMovable)
                        #print(str(parent.children[i].requiredMovable) + "up")
                        self.visited[parent.children[i]] = True
                        self.currentState = parent.children[i]
                        found = True
                        break
                if parent.requiredMovable:
                    self.gm.reverseMove(parent.requiredMovable) #maybe fix thid line
                    parent = parent.parent
                    self.currentState = parent
                else:
                    #print("hiya")
                    break

        return False




    def findChildren(self, gs):
        moves = self.gm.getMovables()
        for mov in moves:
            self.gm.makeMove(mov)
            #print(mov)
            newState = self.gm.getGameState()
            if gs.parent and newState == gs.parent.state:
                #print("here")
                self.gm.reverseMove(mov)
            else:
                #print("there")
                gState = GameState(newState, gs.depth + 1, mov)
                #print(gState.state)
                if gState not in self.visited.keys():
                    gs.children.append(gState)
                    gState.parent = gs
                self.gm.reverseMove(mov)



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = queue.Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        #print(self.currentState.state)
        if self.victoryCondition == self.currentState.state:
            return True

        moves = self.gm.getMovables()

        # if moves:
        #     for i in moves:
        #        print(i)

        if moves and not self.currentState.children:
            self.findChildren(self.currentState)

        if not self.queue.empty():
            child = self.queue.get()
            while self.currentState.parent:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent

            temp = child
            steps = self.findMoves(temp)
            steps.reverse()

            for step in steps:
                self.gm.makeMove(step)

            self.visited[child] = True
            self.currentState = child

        # pstate = self.currentState.parent
        # if self.currentState.parent and len(pstate.children) > pstate.nextChildToVisit:
        #     print("here")
        #     nextChild = pstate.children[pstate.nextChildToVisit]
        #     #print(nextChild.state)
        #     pstate.nextChildToVisit += 1
        #     self.gm.reverseMove(self.currentState.requiredMovable) ##Reverse to Parent
        #     self.gm.makeMove(nextChild.requiredMovable) #Go to next child
        #     self.visited[nextChild] = True
        #     self.currentState = nextChild
        #
        # elif pstate:
        #     print("came")
        #     imStep = pstate.children[0]
        #     #Go To this State
        #     self.gm.reverseMove(self.currentState.requiredMovable) #Go back up to parent
        #     self.gm.makeMove(imStep.requiredMovable) #Go to First kid
        #     if imStep.children: #If no children might nee do to go to next child
        #         imStep.nextChildToVisit += 1
        #         child = imStep.children[0]
        #         self.gm.makeMove(child.requiredMovable)
        #         self.visited[child] = True
        #         self.currentState = child
        # else:
        #     print("hey")
        #     #No parent so no siblings so go to first child
        #     if self.currentState.children:
        #         self.currentState.nextChildToVisit += 1
        #         child = self.currentState.children[0]
        #         self.gm.makeMove(child.requiredMovable)
        #         self.visited[child] = True
        #         self.currentState = child

        return False

    def findChildren(self, gs):
        moves = self.gm.getMovables()
        for mov in moves:
            self.gm.makeMove(mov)
            #print(mov)
            newState = self.gm.getGameState()
            if gs.parent and newState == gs.parent.state:
                #print("here")
                self.gm.reverseMove(mov)
            else:
                #print("there")
                gState = GameState(newState, gs.depth + 1, mov)
                #print(gState.state)

                found = False
                for tups in self.added.keys():
                    if tups.state == newState:
                        found = True
                        break

                if gState not in self.visited.keys() and not found:
                    gs.children.append(gState)
                    self.queue.put(gState)
                    gState.parent = gs
                    self.added[gState] = True

                self.gm.reverseMove(mov)

    def findMoves(self, gs):
        moves = []
        while gs.parent:
            moves.append(gs.requiredMovable)
            self.gm.reverseMove(gs.requiredMovable)
            gs = gs.parent
        return moves