import itertools
import random
import pprint


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("orX", end="")
                else:
                    print("or ", end="")
            print("or")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        """ 
        We only know if there are mines, if all cells are (cells = count)
        """
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        
        return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        """ 
        We only know if there are safe, if all cells are (count = 0)
        """
        if self.count == 0:
            return self.cells
        
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        """
        Remove the cell from the set and substract 1 from count
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        """
        Remove the cell from the set
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        #1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.mark_safe(cell)
        
        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count`
        # Check neighboring cells
        neighborCells = set()
        
        for row in range(cell[0] - 1, cell[0] + 2):            
            for col in range(cell[1] - 1, cell[1] + 2):
                currCell = (row, col)
                # Ignore the cell itself, or if we know that the cell is already safe then continue loop
                if currCell == cell or currCell in self.safes:
                    continue

                # If cell is a known mine then decrease mines count and continue
                if currCell in self.mines:
                    count -= 1
                    continue

                if 0 <= row < self.height and 0 <= col < self.width:
                    neighborCells.add(currCell)         
                         
        newSentence = Sentence(neighborCells, count)
        self.knowledge.append(newSentence)
        
        noMoreChanges = False
        while (noMoreChanges == False):
            noMoreChanges = True
            # 4) mark any additional cells as safe or as mines
            #    if it can be concluded based on the AI's knowledge base
            for sentence in self.knowledge:
                senMines = sentence.known_mines().copy()
                if senMines:
                    for cell in senMines:
                        if cell not in self.mines: 
                            noMoreChanges = False
                            self.mark_mine(cell)
                        
                senSafes = sentence.known_safes().copy()
                if senSafes:
                    for cell in senSafes:
                        if cell not in self.safes: 
                            noMoreChanges = False
                            self.mark_safe(cell)
                
                if (len(sentence.cells) == 0): 
                    noMoreChanges = False
                    self.knowledge.remove(sentence)
                    
        
        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge
        # Looking for the subsets of sets
        # Number of sentences in knowledge list
        noMoreChanges = False
        while (noMoreChanges == False):
            noMoreChanges = True
            for subset in self.knowledge:
                # Looping through sentences - looking for possible subset
                for sentence in self.knowledge:
                    # Avoiding checking subset of itself
                    if subset is sentence:
                        continue

                    # Remove duplicates
                    if subset == sentence:
                        noMoreChanges = False
                        self.knowledge.remove(sentence)
                    
                    # If found subset
                    if subset.cells.issubset(sentence.cells):
                        # Remove the same cells from superset
                        newCells = sentence.cells - subset.cells
                        # Subtract amount of mines
                        newCount = sentence.count - subset.count
                            
                        # Create new sentence 
                        newSentence = Sentence(newCells, newCount)
                        # And add to the knowledge list only when it is new knowledge
                        if newSentence not in self.knowledge:
                            noMoreChanges = False
                            self.knowledge.append(newSentence)
                        
                        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made: 
                print(safe)
                return safe
        print("None")
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        freeCells = []
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) not in self.moves_made and (row, col) not in self.mines:
                    freeCells.append((row, col))
        
        if len(freeCells):
            return random.choice(freeCells)
        else:
            return None
