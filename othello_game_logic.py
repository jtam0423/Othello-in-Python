#Jason Tam 24063520

#GAME LOGIC

###This module is the logic for the game, OTHELLO.
###It contains the classes GameState and GameError. It is a secondary module to the main,
###othello_gui.py. It uses a 2D list and functions to interpret the game.

NONE = 0
BLACK = 1
WHITE = 2

MOVE_LIST = [[0,1],[1,0],[0,-1],[-1,0],[1,1],[-1,-1],[1,-1],[-1,1]]

#right, down, left, up, dRight, uLeft, dLeft, uRight

class GameError(Exception):
    '''
    Raised whenever an attempt to use an invalid game mechanic, row, or column
    '''
    pass

class GameState:
    def __init__(self, inp_list: list):
        ''' Initializes inputs from an input list '''
        self._rows = int(inp_list[0]) #integer
        self._columns = int(inp_list[1]) #integer
        self._turn = inp_list[2] #B or W
        self._position = inp_list[3] #B or W
        self._mode = inp_list[4] #< or >
    
    def make_turn(self, row_input: int, col_input: int) -> list:
        '''Takes input and places them in list: [row, column]'''
        new_list = []
        new_list.append(row_input)
        new_list.append(col_input)
        return new_list
        
    def check_gamestate(self, make_list: list, game_list: list) -> bool:
        '''Returns True if passes all requirements; checks input compatibility with game'''
        try:
            row = make_list[0] #if empty, raises exception
            column = make_list[1]
            if self.check_disc_cell(row, column, game_list) != 0:
                raise GameError()
            elif len(self.list_of_moves(make_list, game_list, self.get_opposite_num())) == 0:
                raise GameError()
            elif self.use_find(row, column, game_list) == False:
                raise GameError()
            else:
                return True
        except:
            return False

    def list_of_moves(self, make_list:list, game_list: list, color: int) -> list:
        '''Returns list of pieces that are around inputted position based on color'''
        row = make_list[0]
        column = make_list[1]
        new_list = []
        for coordinate in MOVE_LIST:
            x = row + coordinate[0] #adds 1, 0, -1
            y = column + coordinate[1]
            if x >= 0 and x <= self._rows - 1:
                if y >= 0 and y <= self._columns - 1:
                    if game_list[y][x] == color:
                        new_list.append((x,y))
        return new_list

    def check_list(self, find_list: list, game_list: list)-> int:
        '''Checks the list for something to flip, returns coordinate to flip'''
        if len(find_list) > 0:
            if find_list[0] != self.get_opposite_num():
                return None
            for num in range(len(find_list)):
                if num != 0:
                    if find_list[num] != self.get_turn_num():
                        if find_list[num] != self.get_opposite_num():
                            return None
                    else:
                        return num #^ needs to be sandwich
        else:
            return None

    def coord_find(self, row: int, column: int, game_list: list, element: list) -> int:
        '''
        Mutates a list of coordinates in the specified direction, returns int to be
        checked later; either returns a number or None
        '''
        row_list = []
        col_list = []
        rf_list = []
        while True:
            if row + element[0] >= 0 and row + element[0] < self._rows:
                if column + element[1] >= 0 and column + element[1] < self._columns:
                    row = row + element[0]
                    column = column + element[1]
                    row_list.append(row) #for later indexing
                    col_list.append(column)
                    rf_list.append(game_list[column][row])
                else:
                    break
            else:
                break
        checked = self.check_list(rf_list, game_list)
        try:
            for num in range(checked):
                row_num = row_list[num] #same indexing as checked (a list)
                col_num = col_list[num]
                self.change_piece_color(row_num, col_num, game_list)
        finally:
            return checked
                          
    def use_find(self, row: int, column: int, game_list: list)-> bool:
        '''Uses coord_find to flip all potential flips for all directions'''
        try:
            none_list = [] #will be list of None and (maybe) numbers
            for obj in MOVE_LIST:
                none_list.append(self.coord_find(row, column, game_list, obj))
            for element in none_list:
                if element != None: #if at least 1 number, valid
                    return True
            raise GameError()
        except:
            return False
        
    def get_turn(self) -> str:
        '''Returns str identifying the turn'''
        if self._turn == 'B':
            return "B"
        else:
            return "W"
        
    def get_turn_num(self) -> int:
        '''Returns BLACK or WHITE int identifying the turn'''
        if self._turn == 'B':
            return BLACK
        else:
            return WHITE

    def get_opposite_num(self) -> int:
        '''Returns BLACK or WHITE int identifying opposite turn'''
        if self._turn == 'B':
            return WHITE
        else:
            return BLACK

    def check_disc_cell(self, row: int, column: int, game_list: list) -> int:
        '''Returns value inside of a certain disc cell as an int'''
        value = game_list[column][row]
        return value

    def valid_turn(self, make_list: list, game_list) -> None:
        '''Adds valid input coordinates onto the board'''
        row = make_list[0]
        column = make_list[1]
        game_list[column][row] = self.get_turn_num() #inputted coordinatess

    def new_game(self) -> list:
        '''Creates a new board'''
        new_list = []
        for column in range(self._columns):
            new_list.append([])
            for rows in range(self._rows):
                new_list[-1].append(NONE)
        r_half = int(self._rows/2) - 1
        c_half = int(self._columns/2)- 1
        if self._position == 'B': #whether B or W is in top left corner
            new_list[c_half][r_half] = BLACK
            new_list[c_half+1][r_half] = WHITE
            new_list[c_half][r_half+1] = WHITE
            new_list[c_half+1][r_half+1] = BLACK
        else:
            new_list[c_half][r_half] = WHITE
            new_list[c_half+1][r_half] = BLACK
            new_list[c_half][r_half+1] = BLACK
            new_list[c_half+1][r_half+1] = WHITE
        return new_list

    def change_turn(self) -> None:
        '''Change the turn'''
        if self._turn == 'B':
            self._turn = 'W'
        else:
            self._turn = 'B'

    def change_piece_color(self, row: int, column: int, game_list: list) -> None:
        '''Changes color of a piece'''
        if game_list[column][row] == BLACK:
            game_list[column][row] = WHITE
        else:
            game_list[column][row] = BLACK
            
    def scoring(self, piece_list: list) -> str:
        '''Counts up and returns the winner based on mode as a string'''
        black_win = piece_list[0]
        white_win = piece_list[1]
        if black_win > white_win and self._mode == '>':
            return 'Black Wins!'
        elif black_win > white_win and self._mode == '<':
            return 'White Wins!'
        elif black_win < white_win and self._mode == '>':
            return 'White Wins!'
        elif black_win < white_win and self._mode == '<':
            return 'Black Wins!'
        else:
            return 'No One Wins!'

    def check_board_for_moves(self, game_list: list) -> bool:
        '''Returns true if there are still moves on the board'''
        move_list = []
        copy_list = []
        for element in game_list: #prevents modifying game_list
            spare_list = []
            for obj in element:
                spare_list.append(obj) #list obj inside need new id
            copy_list.append(list(spare_list)) #create a whole new list with new id
        for column_num in range(len(copy_list)):
            for row_num in range(len(copy_list[column_num])):
                if self.check_disc_cell(row_num, column_num, copy_list) == 0:
                    if self.use_find(row_num, column_num, copy_list) == False:
                        move_list.append(0) #no moves
                    else:
                        move_list.append(1) #at least 1 move
                else:
                    move_list.append(0)
        for num in move_list: 
            if num != 0: #if no moves at all
                return True
        return False
