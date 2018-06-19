import tkinter

DEFAULT_FONT = ('Helvetica', 16)

class InputClass:
    def __init__(self):
        
if __name__ == "__main__":
    x = InputClass()
    print(x._get_input_list())


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
            self._input_window, text= "Enter even number of rows: 4 to 16?")

        label_1.grid(
            row = 2, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        self.entry_1 = tkinter.Entry(
            self._input_window, width = 5)
        
        self.entry_1.grid(
            row = 2, column = 2, padx = 10, pady = 1,
            sticky = tkinter.E)
        
        label_2 = tkinter.Label(
            self._input_window, text = "Enter even number of columns: 4 to 16?")

        label_2.grid(
            row = 3, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        self.entry_2 = tkinter.Entry(
            self._input_window, width = 5)

        self.entry_2.grid(
            row = 3, column = 2, padx = 10, pady = 1,
            sticky = tkinter.E)
        
        label_3 = tkinter.Label(
            self._input_window, text = "Which player goes first: B or W?")

        label_3.grid(
            row = 4, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.entry_3 = tkinter.Entry(
            self._input_window, width = 5)

        self.entry_3.grid(
            row = 4, column = 2, padx = 10, pady = 1,
            sticky = tkinter.E)

        label_4 = tkinter.Label(
            self._input_window, text = "Who is in top left corner: B or W?")

        label_4.grid(
            row = 5, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.entry_4 = tkinter.Entry(
            self._input_window, width = 5)

        self.entry_4.grid(
            row = 5, column = 2, padx = 10, pady = 1,
            sticky = tkinter.E)

        label_5 = tkinter.Label(
            self._input_window, text = "More or less pieces wins: > or <?")

        label_5.grid(
            row = 6, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.entry_5 = tkinter.Entry(
            self._input_window, width = 5)

        self.entry_5.grid(
            row = 6, column = 2, padx = 10, pady = 1,
            sticky = tkinter.E)

        submit = tkinter.Button(
            master = self._input_window, text= "Ready!", command = self._get_entry)

        submit.grid(
            row = 7, column = 1, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E)

        self._label_6 = tkinter.Label(
            self._input_window, text = '----------------------------------------')
        
        self._label_6.grid(
            row = 7, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        self._input_window.rowconfigure(0, weight = 1)
        self._input_window.rowconfigure(1, weight = 1)
        self._input_window.rowconfigure(2, weight = 1)
        self._input_window.rowconfigure(3, weight = 1)
        self._input_window.rowconfigure(4, weight = 1)
        self._input_window.rowconfigure(5, weight = 1)
        self._input_window.rowconfigure(6, weight = 1)
        self._input_window.rowconfigure(7, weight = 1)
        self._input_window.columnconfigure(0, weight = 1)
        
    def _get_entry(self) -> None:
        '''Returns each get() for each entry'''
        self._input_list = [] #reset for invalid input
        self._label_6.grid_forget()
        if self._if_correct_input() != None:
            self._label_6 = tkinter.Label(
            self._input_window, text = self._if_correct_input())

            self._label_6.grid(
            row = 7, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)
        else:
            self._end()

    def _if_correct_input(self) -> str:
        '''Checks each entry for validity'''
        #self.entry_1
        #self.entry_2
        if self._int_input() != None:
            return self._int_input()
        #self.entry_3
        #self.entry_4
        if self._str_input(self.entry_3.get()) != None:
            return self._str_input(self.entry_3.get())
        
        if self._str_input(self.entry_4.get()) != None:
            return self._str_input(self.entry_4.get())
        #self.entry_5
        if self._more_less() != None:
            return self._more_less()
        return None

    def _int_input(self) -> str:
        '''Checks first two inputs'''
        try:
            e1 = int(self.entry_1.get()) #first two integers
            e2 = int(self.entry_2.get())           
        except:
            return 'Entry 1 and 2 must be numbers!'

        if self._even_num(e1) == False or self._four_sixteen(e1) == False:
            return 'Entry 1: Even and between 4 and 16!'
        
        if self._even_num(e2) == False or self._four_sixteen(e2) == False:
            return 'Entry 2: Even and between 4 and 16!'
        
        self._input_list.append(e1)
        self._input_list.append(e2)
        return None

    def _even_num(self, num: int) -> bool:
        '''Checks if num is even'''
        if num % 2 == 0:
            return True
        return False

    def _four_sixteen(self, num: int) -> bool:
        '''Checks if num is between 4 and 16'''
        if num < 4 or num > 16:
            return False
        return True
    
    def _str_input(self, input_str: str) -> str:
        '''Checks inputs 3 and 4'''
        if input_str != 'W' and input_str != 'B':
                return 'Entry 3 and 4 must be W or B!'
        else:
            self._input_list.append(input_str)
            return None
        
    def _more_less(self) -> str:
        '''Checks last input'''
        if self.entry_5.get() != '<' and self.entry_5.get() != '>':
            return 'Entry 5 must be < or >!'
        else:
            self._input_list.append(self.entry_5.get())
            return None
    
    def _get_input_list(self) -> list:
        '''Return self._input_list'''
        return self._input_list
