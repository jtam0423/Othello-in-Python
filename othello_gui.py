#Jason Tam 24063520

#Othello_GUI

###This module is the GUI for the game, OTHELLO.
###It contains the classes OthelloApplication and InputClass. It also is the main module
###and runs the program. It handles entry and interfaces with othello_game_logic.py.

import othello_game_logic
import tkinter
import point

DEFAULT_FONT = ('Helvetica', 16)
BACKGROUND = 'green'
DISC_B = 'black'
DISC_W = 'white'

class OthelloApplication:
    def __init__(self, row: int, column: int, game: 'GameState', board: list):
        '''
        Sets up main game, visual board, pieces, labels, and win state.
        '''
        self._row = row
        self._column = column
        self._game = game
        self._board = board
        self._row_list = []
        self._column_list = []
        
        self._root_window = tkinter.Tk()
        self._root_window.wm_title('Othello!')

        self._label_turn = tkinter.Label(
             self._root_window, text= self._color_turn(), font = DEFAULT_FONT)

        self._label_turn.grid(
             row = 0, column = 0, padx = 10, pady = 10, columnspan = 2,
             sticky = tkinter.N + tkinter.W + tkinter.S)

        self._black_pieces = tkinter.Label(
            self._root_window, text= self._black_num(), font = DEFAULT_FONT)

        self._black_pieces.grid(
            row = 0, column = 1, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S)

        self._white_pieces = tkinter.Label(
            self._root_window, text= self._white_num(), font = DEFAULT_FONT)

        self._white_pieces.grid(
            row = 0, column = 2, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.E + tkinter.S)
            
        self._canvas = tkinter.Canvas(
            master = self._root_window,
            width = 500, height = 500,
            background = BACKGROUND)

        self._canvas.grid(
            row = 1, column = 0, padx = 10, pady = 10, columnspan = 3,
            sticky = tkinter.N + tkinter.W + tkinter.E + tkinter.S)

        self._canvas.bind('<Configure>', self._on_canvas_resized) #Resizing objects
        self._canvas.bind('<Button-1>', self._click_move) #ClickPoint -> Make Discs

        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''Called when canvas resizes'''
        self._make_lines()
        self._make_discs()
        
    def _make_lines(self) -> None:
        '''Make rows and columns'''
        self._canvas.delete(tkinter.ALL)
        self._root_window.update()
        board_width = self._canvas.winfo_width() - 4
        board_height = self._canvas.winfo_height() - 4
        divide_num = 0
        for col in range(self._column):
            self._canvas.create_line(divide_num, 0, divide_num, board_height)
            self._column_list.append(divide_num)
            divide_num += (board_width/self._column)
        divide_num = 0
        for r_ow in range(self._row):
            self._canvas.create_line(0, divide_num, board_width, divide_num)
            self._row_list.append(divide_num)
            divide_num += (board_height/self._row)

    def _color_turn(self) -> str:
        '''Finds the turn color, then returns a string'''
        if self._game.get_turn() == 'W':
            return "It's White's turn!"
        else:
            return "It's Black's turn!"

    def _pieces_on_board(self) -> list:
        '''Returns number of pieces on the board as a list'''
        piece_list = []
        black_win = 0
        white_win = 0
        for element in self._board:
            for num in element:
                if num == 1: #BLACK
                    black_win +=1
                elif num == 2: #WHITE
                    white_win += 1
        piece_list.append(black_win)
        piece_list.append(white_win)
        return piece_list

    def _black_num(self) -> str:
        '''Returns number of black pieces on board'''
        return 'Black: ' + str(self._pieces_on_board()[0]) #Black: (num)

    def _white_num(self) -> str:
        '''Returns number of white pieces on board'''
        return 'White: ' + str(self._pieces_on_board()[1]) #White: (num)
        
    def _click_move(self, event: tkinter.Event) -> None:
        '''Makes a move based on valid click location'''
        width = self._canvas.winfo_width() + 4
        height = self._canvas.winfo_height() + 4
        click_pix = point.from_pixel(
            event.x, event.y, width, height).pixel(width, height)
        click_x = click_pix[0]
        click_y = click_pix[1]
        for cols in range(self._column):
            for rows in range(self._row):
                x_up_left = (width/self._column)*cols + 2 #+2 to make up for positioning
                x_down_right = (width/self._column)*(cols + 1) + 2
                y_up_left = (height/self._row)*rows + 2
                y_down_right = (height/self._row)*(rows + 1) + 2
                if (click_x >= x_up_left) and (click_x <= x_down_right) and (click_y >= y_up_left) and (click_y <= y_down_right):
                    input_list = self._game.make_turn(rows, cols)
                    self._execute_move(input_list)

    def _execute_move(self, inp_list: list) -> None:
        '''Function to execute a move on the board'''
        if self._game.check_gamestate(inp_list, self._board):
            self._game.valid_turn(inp_list, self._board)
            self._make_discs()
            self._game.change_turn()
            if self._game.check_board_for_moves(self._board):
                self._update_labels()
            elif self._game.check_board_for_moves(self._board) == False: #checks for valid moves on other team
                self._game.change_turn()
                if self._game.check_board_for_moves(self._board) == False: #if also no moves, game over
                    self._make_discs()
                    self._update_labels()
                    self._update_win_label()
                    over = GameOver()#opens toplevel window
                    over._show()
                    self._end()
                else: #if not game, over, keep playing
                    self._make_discs()
                    self._update_labels() #change name
                    p_u = PopUp(self._game.get_turn())
                    p_u._show()
            else:
                return #invalid

    def _make_disc(self, x1: float, y1: float, x2: float, y2: float, color: str) -> None:
        '''Creates an oval object on the board'''
        self._canvas.create_oval(x1,y1,x2,y2, fill = color) #Each disc fills space
        
    def _make_discs(self) -> None:
        '''Makes all discs for the board'''
        width = self._canvas.winfo_width() - 4 # - 4 for canvas equals 500 + 4
        height = self._canvas.winfo_height() - 4
        
        for cols in range(self._column):
            for rows in range(self._row):
                x_up_left = (width/self._column)*cols
                x_down_right = (width/self._column)*(cols + 1)
                y_up_left = (height/self._row)*rows
                y_down_right = (height/self._row)*(rows + 1)
                if self._board[cols][rows] == 1:
                    self._make_disc(x_up_left, y_up_left, x_down_right, y_down_right, DISC_B)
                elif self._board[cols][rows] == 2:
                    self._make_disc(x_up_left, y_up_left, x_down_right, y_down_right, DISC_W)

    def _update_labels(self) -> None:
        '''Updates the each label'''
        self._black_pieces.grid_forget() #removes label
        
        self._black_pieces = tkinter.Label(
            self._root_window, text= self._black_num(), font = DEFAULT_FONT)

        self._black_pieces.grid(
            row = 0, column = 1, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S)

        self._white_pieces.grid_forget()
        
        self._white_pieces = tkinter.Label(
            self._root_window, text= self._white_num(), font = DEFAULT_FONT)

        self._white_pieces.grid(
            row = 0, column = 2, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.E + tkinter.S)

        self._label_turn.grid_forget()
        
        self._label_turn = tkinter.Label(
             self._root_window, text= self._color_turn(), font = DEFAULT_FONT)

        self._label_turn.grid(
             row = 0, column = 0, padx = 10, pady = 10, columnspan = 2,
             sticky = tkinter.N + tkinter.W + tkinter.S)

    def _update_win_label(self) -> None:
        '''Change turn label to winner label'''
        self._label_turn.grid_forget()
        
        self._label_turn = tkinter.Label(
             self._root_window, text= self._game.scoring(self._pieces_on_board()), font = DEFAULT_FONT)

        self._label_turn.grid(
             row = 0, column = 0, padx = 10, pady = 10, columnspan = 2,
             sticky = tkinter.N + tkinter.W)
    
    def _start(self) -> None:
        '''Creates the lines and discs'''
        self._make_lines() #creates everything
        self._make_discs()
        self._root_window.mainloop()

    def _end(self) -> None:
        '''Closes the window'''
        self._root_window.destroy()

class InputClass:
    def __init__(self):
        '''
        Sets up input window, entry objects, and error response labels
        '''
        self._input_list = [] #holds input

        self._input_window = tkinter.Tk()
        
        self._input_window.wm_title('New Game')

        label_title = tkinter.Label(
            self._input_window, text= "Othello!", font =('Helvetica', 24))

        label_title.grid(
            row = 0, column = 0, columnspan = 3, padx = 10, pady = 10,
            sticky = tkinter.N)

        label_title = tkinter.Label(
            self._input_window, text= "*   *   *   *   Full   *   *   *   *", font = DEFAULT_FONT)

        label_title.grid(
            row = 1, column = 0, columnspan = 3,
            sticky = tkinter.N)
        
        label_1 = tkinter.Label(
            self._input_window, text= "Select number of Rows:")

        label_1.grid(
            row = 2, column = 0, padx = 10, pady = 10, columnspan = 2,
            sticky = tkinter.W)

        self._row_var = tkinter.IntVar(master = self._input_window)

        self._row_var.set(4) #default value is 4

        opt_1 = tkinter.OptionMenu(
            self._input_window, self._row_var, 4, 6, 8, 10, 12, 14, 16)
        
        opt_1.grid(
            row = 2, column = 2, padx = 10, pady = 10,
            sticky = tkinter.E)

        label_2 = tkinter.Label(
            self._input_window, text= "Select number of Columns:")

        label_2.grid(
            row = 3, column = 0, padx = 10, pady = 10, columnspan = 2,
            sticky = tkinter.W)

        self._col_var = tkinter.IntVar(master = self._input_window)

        self._col_var.set(4) #default value is 4

        opt_2 = tkinter.OptionMenu(
            self._input_window, self._col_var, 4, 6, 8, 10, 12, 14, 16)
        
        opt_2.grid(
            row = 3, column = 2, padx = 10, pady = 10,
            sticky = tkinter.E)

        label_3 = tkinter.Label(
            self._input_window, text= "Which Color Moves First?")

        label_3.grid(
            row = 4, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._move_choice = tkinter.IntVar()

        self._move_choice.set(1) #default value is 1 (black)

        blk_m = tkinter.Radiobutton(
            master = self._input_window, text = 'Black', variable = self._move_choice, value = 1)

        wht_m = tkinter.Radiobutton(
            master = self._input_window, text = 'White', variable = self._move_choice, value = 2)

        blk_m.grid(
            row = 4, column = 1, padx = 10, pady = 10,
            sticky = tkinter.W)

        wht_m.grid(
            row = 4, column = 2, padx = 10, pady = 10,
            sticky = tkinter.E)

        label_4 = tkinter.Label(
            self._input_window, text= "Which Color is in the Upper Left?")

        label_4.grid(
            row = 5, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._order_choice = tkinter.IntVar()

        self._order_choice.set(1) #default value is 1 (black)

        blk_o = tkinter.Radiobutton(
            master = self._input_window, text = 'Black', variable = self._order_choice, value = 1)

        wht_o = tkinter.Radiobutton(
            master = self._input_window, text = 'White', variable = self._order_choice, value = 2)

        blk_o.grid(
            row = 5, column = 1, padx = 10, pady = 10,
            sticky = tkinter.W)

        wht_o.grid(
            row = 5, column = 2, padx = 10, pady = 10,
            sticky = tkinter.E)

        label_5 = tkinter.Label(
            self._input_window, text= "Who is the winner: More (>) or Less (<)?")

        label_5.grid(
            row = 6, column = 0, padx = 10, pady = 10, columnspan = 2,
            sticky = tkinter.W)

        self._str_var = tkinter.StringVar(master = self._input_window)

        self._str_var.set('>') #default value is >

        opt_2 = tkinter.OptionMenu(
            self._input_window, self._str_var, '>', '<')
        
        opt_2.grid(
            row = 6, column = 2, padx = 10, pady = 10,
            sticky = tkinter.E)

        submit = tkinter.Button(
            master = self._input_window, text= "Ready to Play!", font = ('Helvetica', 16), command = self._get_entry)

        submit.grid(
            row = 7, column = 0, columnspan = 3, padx = 10, pady = 10,
            sticky = tkinter.S)

        self._input_window.columnconfigure(0, weight = 1)
        self._input_window.rowconfigure(0, weight = 1)
        self._input_window.rowconfigure(1, weight = 1)

        self._input_window.mainloop()

    def _get_entry(self) -> None:
        '''Retrieves the entry and modifies the _input_list'''
        move = ''
        order = ''

        if self._move_choice.get() == 1:
            move = 'B'
        else:
            move = 'W'

        if self._order_choice.get() == 1:
            order = 'B'
        else:
            order = 'W'

        self._input_list = [
            self._row_var.get(), self._col_var.get(), move, order, self._str_var.get()]

        self._input_window.destroy()

    def _get_input_list(self) -> list:
        '''Returns the _input_list'''
        return self._input_list

    def _end(self) -> None:
        '''Closes window'''
        self._input_window.destroy()


class PopUp:
    def __init__(self, color: str):
        '''
        PopUp class opens up a Toplevel window whenever a players turn has been skipped
        due to game logic
        '''
        self._color = color
        
        self._pop_up = tkinter.Toplevel()

        skip_label = tkinter.Label(
            master = self._pop_up, text = self._player_string(), font = DEFAULT_FONT)

        skip_label.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W + tkinter.E)

        okay_button = tkinter.Button(
            master = self._pop_up, text = 'OK', font = DEFAULT_FONT,
            command = self._ok_press)

        okay_button.grid(row = 1, column = 0, padx = 10, pady = 10)

        self._pop_up.rowconfigure(1, weight = 1)
        self._pop_up.columnconfigure(0, weight = 1)

    def _player_string(self) -> str:
        '''Returns a string with current player who was skipped'''
        opp_player = ''
        if self._color == 'W':
            opp_player = 'Black' #find out which turn was skipped
        else:
            opp_player = 'White'
        return 'Player ' + opp_player + ' turn skipped!'

    def _show(self) -> None:
        '''Shows the okay window'''
        self._pop_up.grab_set()
        self._pop_up.wait_window()

    def _ok_press(self) -> None:
        '''Destroys the window'''
        self._pop_up.destroy()

class GameOver:
    def __init__(self):
        '''
        GameOver Class opens a game over Toplevel window to let the player know the game
        is over; also button closes both the toplevel window and the root window (board)
        '''
        self._game_over = tkinter.Toplevel()

        skip_label = tkinter.Label(
            master = self._game_over, text = '* * * GAME OVER! * * *', font  = DEFAULT_FONT)

        skip_label.grid(
            row = 0, column = 0, padx = 15, pady = 10,
            sticky = tkinter.W + tkinter.E)

        okay_button = tkinter.Button(
            master = self._game_over, text = 'End Game', font = DEFAULT_FONT,
            command = self._ok_press)

        okay_button.grid(row = 1, column = 0, padx = 10, pady = 10)

        self._game_over.rowconfigure(1, weight = 1)
        self._game_over.columnconfigure(0, weight = 1)
        
    def _show(self) -> None:
        '''Shows the okay window'''
        self._game_over.grab_set()
        self._game_over.wait_window()

    def _ok_press(self) -> None:
        '''Destroys the window'''
        self._game_over.destroy() #just to show text

def run_othello() -> None:
    '''Initializes classes and runs Othello Program'''
    try:
        o_input = InputClass()
        list_inputs = o_input._get_input_list()
        r = list_inputs[0] #gets number of rows
        c = list_inputs[1] #gets number of columns
        g = othello_game_logic.GameState(list_inputs)
        game_list = g.new_game()
        app = OthelloApplication(r, c, g, game_list)
        app._start()
    except: #if exit initial window
        pass

if __name__ == '__main__':
    run_othello()
