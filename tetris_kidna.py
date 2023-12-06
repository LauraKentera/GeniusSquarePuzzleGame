import random
import subprocess 

def playSound(file_path):
    subprocess.run(['afplay', file_path])


EMPTY_SPOT = '-'
BLOCKER_SPOT = 'o'

class Shape:
    __slots__ = ['__table', '__position', '__label', '__color']

    def __init__(self, table, label, color):
        self.__table = table
        self.__position = None
        self.__label = label
        self.__color = color

    def get_table(self):
        return self.__table

    def get_label(self):
        return self.__label

    def get_color(self):
        return self.__color
    
    def rotate(self, direction):
        if direction == 'R': ## Rotate the shape to the right 
            self.__table = [list(row) for row in zip(*reversed(self.__table))]
        elif direction == 'L': ## Totate the shape to the left 
            self.__table = [list(row) for row in zip(*reversed(self.__table[::-1]))]

    def display_table(self):
        for row in self.__table:
            for col in row:
                if col == 1:
                    print('\033[' + self.__color + 'm#\033[0m', end = ' ')
                else:
                    print(EMPTY_SPOT, end = ' ')
            print()


    def __str__(self):
        return str(self.__table) + " " + str(self.__position)

class Puzzle:
    __slots__ = ["__board", "__blocker_locations"]

    def __init__(self, blocker_locations) -> None:
        self.__board = [[EMPTY_SPOT for _ in range(6)] for _ in range(6)]
        self.__blocker_locations = blocker_locations

        for r, c in blocker_locations:
            self.__board[r][c] = BLOCKER_SPOT  # Representing blockers with 'o'

        self.display_board()  # Display board upon initialization

    def draw(self, position: tuple, shape: Shape, symbol: str):
        row, col = position
        table_shape = shape.get_table()
        shape_color = shape.get_color()

        for index in range(len(table_shape)):
            for j in range(len(table_shape[0])):
                if table_shape[index][j] == 1:
                    new_row = index + row
                    new_col = j + col

                    if not (0 <= new_row < len(self.__board) and 0 <= new_col < len(self.__board[0])):
                        print("Shape cannot be put there. Try a different spot.")
                        return False

                    if self.__board[new_row][new_col] != EMPTY_SPOT:
                        print("Shape cannot be put there. Try a different spot.")
                        return False

        for index in range(len(table_shape)):
            for j in range(len(table_shape[0])):
                if table_shape[index][j] == 1:
                    self.__board[index + row][j + col] = '\033[' + shape_color + 'm' + symbol + '\033[0m'

        self.display_board()  # Display board after placing the shape
        return True

    def is_board_filled(self):
        for row in self.__board:
            if EMPTY_SPOT in row:
                return False
        return True

    def display_board(self):
        s = '   0 1 2 3 4 5\n'
        s += '  ------------\n'
        for index in range(len(self.__board)):
            s += str(index) + " | "
            for sth in self.__board[index]:
                s += sth + ' '
            s += "\n"
        print(s)

    def display_shapes(self, shapes):
        for shape in shapes:
            table = shape.get_table()
            color = shape.get_color()
            print("Shape:", shape.get_label())
            for row in table:
                for col in row:
                    if col == 1:
                        print('\033[' + color + 'm#\033[0m', end=' ')
                    else:
                        print(EMPTY_SPOT, end=' ')
                print()

    def randomize_blockers(self):
        self.__blocker_locations = [
            (random.randint(0, 5), random.randint(0, 5)) for _ in range(random.randint(1, 10))
        ]
        self.__board = [[EMPTY_SPOT for _ in range(6)] for _ in range(6)]

        for r, c in self.__blocker_locations:
            self.__board[r][c] = BLOCKER_SPOT
    
    def restart_game(self):
        self.randomize_blockers()
        self.display_board()

    def __str__(self):
        self.display_board()  # Display board upon initialization
        return ""
    

def main():
    shape_1 = Shape([[1, 1, 1], [0, 1, 0]], "T", "31")  # Red color for shape_1
    shape_2 = Shape([[1, 1], [1, 1]], "S", "32")  # Green color for shape_2
    shape_3 = Shape([[1, 1, 1]], "L", "34")  # Blue color for shape_3
    shape_4 = Shape([[1]], "D", "33") # Yellow color for shape_4 
    shape_5 = Shape([[1,1,0], [0,1,1]], "Z", "35") # Magenta color for shape_5

    blocker_locations = ((0, 0), (0, 1), (3, 4), (4, 0), (5, 5))
    

    shapes = [shape_1, shape_2, shape_3, shape_4, shape_5]

    while True:
        blocker_locations = [
            (random.randint(0,5), random.randint(0,5)) for _ in range(random.randint(1,10))
        ]
        puzzle1 = Puzzle(blocker_locations)

        while not puzzle1.is_board_filled():
            puzzle1.display_shapes(shapes)
            print("Next shapes in line: T, S, L, D, Z")
            selected_shape = input("Enter shape (T/S/L/D/Z) to place: ").upper()
            if selected_shape not in ['T', 'S', 'L', 'D', 'Z']:
                print("Invalid shape selected. Please choose from T, S, L, D or Z.")
                continue

            shape_to_place = None
            for shape in shapes:
                if shape.get_label() == selected_shape:
                        shape_to_place = None
            for shape in shapes:
                if shape.get_label() == selected_shape:
                    shape_to_place = shape
                    break

            if shape_to_place:
                print("Rotate the shape. Press Enter to stop rotation.")
                while True:
                    direction = input("Enter rotation direction (L/R) or press Enter to stop: ").upper()
                    if direction == '':
                        break
                    elif direction in ['L', 'R']:
                        shape_to_place.rotate(direction)
                        shape_to_place.display_table() # Display rotated shape
                    else:
                        print("Invalid direction entered. Please enter L, R, or press Enter.")
                
                coordinates = input("Enter coordinates (row, col) to place the shape (e.g., 0,0): ")
                row, col = map(int, coordinates.split(','))

                symbol = selected_shape
                if not puzzle1.draw((row, col), shape_to_place, symbol):
                    continue
            else:
                print("Invalid shape selected. Please choose from T, S, L, D or Z.")

        print("Game is finished, you win!")
        sound_file = 'victory.mp3'
        playSound(sound_file)

        play_again = input("Do you want to play another round? (Y/N): ").upper()
        if play_again != 'Y':
            break 


if __name__ == "__main__":
    main()

