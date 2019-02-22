from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        t = []
        for i in range(1, 4):
            info = self.kb.kb_ask(parse_input('fact: (on ?DISK peg' + str(i) + ')'))
            states = []
            if info:
                for piece in info:
                    disk = piece['?DISK']
                    num = int(disk[-1])
                    states.append(num)
            states.sort()
            tuptemp = tuple(states)
            t.append(tuptemp)
        return tuple(t)
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        ##Change the on statements first
        ### ADD our known knowledge
        disk = movable_statement.terms[0]
        speg = movable_statement.terms[1]
        fpeg = movable_statement.terms[2]

        states = self.getGameState()


        self.kb.kb_retract(parse_input('fact: (on ' + str(disk) + ' ' + str(speg) + ')'))
        self.kb.kb_retract(parse_input('fact: (top ' + str(disk) + ' ' + str(speg) + ')'))
        self.kb.kb_assert(parse_input('fact: (on ' + str(disk) + ' ' + str(fpeg) + ')'))
        self.kb.kb_assert(parse_input('fact: (top ' + str(disk) + ' ' + str(fpeg) + ')'))

        spegn = int(str(speg)[-1])
        if len(states[spegn - 1]) > 1:
            nt = 'disk' + str(states[spegn - 1][1])
            self.kb.kb_assert(parse_input('fact: (top ' + nt + ' ' + str(speg) + ')'))
        else:
            self.kb.kb_assert(parse_input('fact: (empty ' + str(speg) + ')'))

        fpegn = int(str(fpeg)[-1])
        if len(states[fpegn - 1]) <= 0:
            self.kb.kb_retract(parse_input('fact: (empty ' + str(fpeg) + ')'))
        else:
            ot = 'disk' + str(states[fpegn - 1][0])
            self.kb.kb_retract(parse_input('fact: (top ' + ot + ' ' + str(fpeg) + ')'))
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        gen_state = []
        for i in range(1, 4):
            t = []
            for j in range(1, 4):
                s = 'fact: (loc ?TILE pos' + str(j) + ' pos' + str(i) + ')'
                binds = self.kb.kb_ask(parse_input(s))
                if binds:
                    for b in binds:
                        tile = b['?TILE']
                        num = tile[-1]
                        if num == 'y':
                            num = -1
                        t.append(int(num))
            tup = tuple(t)
            gen_state.append(tup)

        return tuple(gen_state)
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile = movable_statement.terms[0]
        initx = movable_statement.terms[1]
        inity = movable_statement.terms[2]
        finx = movable_statement.terms[3]
        finy = movable_statement.terms[4]

        #if(initx == finx and inity == finy):
            #print("fuck")
            #return


        #if str(initx)[-1] != '2' and str(inity)[-1] != '2' and str(finx)[-1] != '2' and str(finy)[-1] != '2':
            #print("weird error")
            #return




        ret_stat = 'fact: (loc ' + str(tile) + ' ' + str(initx) + ' ' + str(inity) + ')'
        self.kb.kb_retract(parse_input(ret_stat))

        add_stat = 'fact: (loc ' + str(tile) + ' ' + str(finx) + ' ' + str(finy) + ')'
        self.kb.kb_assert(parse_input(add_stat))

        ##must also change empty
        empty_stat = 'fact: (loc empty ' + str(initx) + ' ' + str(inity) + ')'
        self.kb.kb_assert(parse_input(empty_stat))

        empty_ret = 'fact: (loc empty ' + str(finx) + ' ' + str(finy) + ')'
        self.kb.kb_retract(parse_input(empty_ret))
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
