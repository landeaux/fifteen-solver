"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Check if tile zero is positioned at (i,j).
        if self._grid[target_row][target_col] != 0:
            return False
        # Check if all tiles in rows i+1 or below are positioned at their solved location.
        if target_row + 1 < self._height:
            for row in range(target_row + 1, self._height):
                for col in range(self._width):
                    solved_value = (col + self._width * row)
                    if solved_value != self.get_number(row, col):
                        return False
        # All tiles in row i to the right of position (i,j) are positioned at 
        # their solved location.
        if target_col + 1 < self._width:
            for col in range(target_col + 1, self._width):
                solved_value = (col + self._width * (target_row))
                if solved_value != self.get_number(target_row, col):
                    return False
        return True
    
    def position_tile(self, target_row, target_col, target_tile, move_string, col0 = False):
        """
        Helper function that positions a target_tile to (target_row, target_col)
        and returns the move_string that will get it there
        """
        
        if col0:
            if (target_tile[1] > target_col) and (target_tile[0] == target_row):
                move_string += "r" * (target_tile[1] - 1)
                for _ in range(target_tile[1] - 2):
                    move_string += "ulldr"
                move_string += "ulld"
                return move_string
        
        # if the target tile is above target row
        if target_tile[0] < target_row:
            move_string += "u" * (target_row - target_tile[0])
            
            # if target tile is to the right of target column
            if target_tile[1] > target_col:
                move_string += "r" * (target_tile[1] - target_col)
                               
                for _ in range(target_tile[1] - target_col - 1):
                    move_string += "ulldr" if target_tile[0] > 0 else "dllur"
                move_string += "ulld" if target_tile[0] > 0 else "dluld"
                    
            # if target tile is to the left of target column
            if target_tile[1] < target_col:
                move_string += "l" * (target_col - target_tile[1])
                               
                for _ in range(target_col - target_tile[1] - 1):
                    move_string += "drrul"            
            
            if target_tile[1] == target_col:
                move_string += "ld"            

            if col0:
                puzzle_clone = self.clone()
                puzzle_clone.update_puzzle(move_string)
                if puzzle_clone.current_position(0, 0) == (target_row, 0):
                    return move_string
            
            puzzle_clone = self.clone()
            puzzle_clone.update_puzzle(move_string)
            
            zero = puzzle_clone.current_position(0, 0)
            
            for _ in range(target_row - zero[0]):
                    move_string += "druld" 
                
        # if target tile is to the left of zero tile
        else:
            if not col0:
                move_string += "l" * (target_col - target_tile[1])
                for _ in range(target_col - target_tile[1] - 1):
                    move_string += "urrdl"
            else:
                move_string += "l" * (target_col - target_tile[1] + 1)
                for _ in range(target_col - target_tile[1]):
                    move_string += "urrdl"
        
        return move_string
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_string = ""
        target_tile = self.current_position(target_row, target_col)
        
        move_string = self.position_tile(target_row, target_col, target_tile, move_string)
        self.update_puzzle(move_string)
        
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_string = "ur"
        target_tile = self.current_position(target_row, 0)
        
        if target_tile != (target_row - 1, 0):
            move_string = self.position_tile(target_row - 1, 1, target_tile, move_string, True)
            move_string += "ruldrdlurdluurddlur"
            
        move_string += "r" * (self._width - 2)
        
        self.update_puzzle(move_string)
        
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check whether tile zero is at (0,j)
        if self._grid[0][target_col] != 0:
            return False
        # check whether tiles to right of zero tile are solved
        for row in range(2):
            for col in range(target_col + 1, self._width):
                solved_value = (col + self._width * row)
                if solved_value != self.get_number(row, col):
                    return False
        # check whether the tile at (1,j) is solved 
        if (target_col + self._width) != self.get_number(1, target_col):
            return False
        # check whether all tiles from in rows 2 and below are solved
        for row in range(2, self._height):
            for col in range(self._width):
                solved_value = (col + self._width * row)
                if solved_value != self.get_number(row, col):
                    return False    
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check whether tile zero is at (1,j)
        if self._grid[1][target_col] != 0:
            return False
        # check whether all positions below this position are solved
        if not self.lower_row_invariant(1, target_col):
            return False
        # check whether all positions to the right of this position are solved
        for col in range(target_col + 1, self._width):
            if col != self.get_number(0, col):
                return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move_string = "ld"
        temp = ""
        
        target_tile = self.current_position(0, target_col)          
        
        if target_tile != (0, target_col - 1):
            # reposition the target tile to position (1,j−1) with tile zero in position (1,j−2).
            if target_col - target_tile[1]  == 1:
                move_string += "uld" 
            if target_tile[0] == 0:
                move_string += "u"
                temp = "dru"
            move_string += "l" * (target_col - target_tile[1] - 1)
            move_string += temp
            
            if target_col - target_tile[1]  > 2:
                for count in range(target_col - target_tile[1] - 2):
                    if target_tile[0] == 0:
                        move_string += "ur" if count > 0 else ""
                        move_string += "rdl"
                    else:
                        move_string += "urrdl"
            
            if (target_col - target_tile[1]  != 1) and (target_tile[0] == 0) and (target_col - target_tile[1]  <= 2):
                move_string += "ld"
            
            move_string += "urdlurrdluldrruld"
            
        self.update_puzzle(move_string)
        
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        move_string = ""
        temp = ""
        target_tile = self.current_position(1, target_col)
        
        # if the target tile is above target row
        if target_tile[0] == 0:
            move_string += "u"
            temp = "dru" if target_tile[1] != target_col else ""
        else:
            temp = "ur"
        move_string += "l" * (target_col - target_tile[1])
        move_string += temp

        for _ in range(target_col - target_tile[1] - 1):
            move_string += "rdlur"            
        
        self.update_puzzle(move_string)
        
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_string = "lu"
        
        if self.get_number(1, 0) == 1:
            move_string += "rdlu"
        elif self.get_number(0, 0) == 1:
            move_string += "rdlurdlu"
        
        self.update_puzzle(move_string)
        
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        
        # Find out where the zero tile is, save coordinates
        zero_row, zero_col = self.current_position(0, 0)

        if zero_row == 0:
            if self.row0_invariant(0):
                return ""
        
        if (zero_row, zero_col) != (self._height - 1, self._width - 1):
            move_string += "d" * (self._height - zero_row - 1)
            move_string += "r" * (self._width - zero_col - 1)
            self.update_puzzle(move_string)
            zero_row, zero_col = self.current_position(0, 0)
            
        for _ in range(self._height - 2):
            while zero_col > 0:
                move_string += self.solve_interior_tile(zero_row, zero_col)
                zero_row, zero_col = self.current_position(0, 0)
            move_string += self.solve_col0_tile(zero_row)
            zero_row, zero_col = self.current_position(0, 0)
        for _ in range(self._width - 2):
            while zero_col > 1:
                if zero_row == 1:
                    move_string += self.solve_row1_tile(zero_col)
                    zero_row, zero_col = self.current_position(0, 0)
                else:
                    move_string += self.solve_row0_tile(zero_col)
                    zero_row, zero_col = self.current_position(0, 0)
        move_string += self.solve_2x2()
        
        return move_string

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
