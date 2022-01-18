###################################################################################################
#
#   CS Programing Project #10
#
#       Algorithm
#
#           Start
#               Function definitions
#                   initialize()
#                   deal_from_stock(stock, tableau) -> None
#                   display() -> None
#                   get_option() -> List
#                   Validate_move(tableau, src_col, src_row, dst_col)) -> Boolean
#                   move(tableau, src_col, src_row, dst_col)) -> Boolean
#                   check_for_win(foundation) -> None
#                   check_sequence(column_lst) -> Boolean
#                   move_to_foundation(tableau, foundation) -> None
#                   main() -> None
#                       Loop until user quits
#                           Display stock, foundation, tableau
#                           Prompt user for input
#                           Call get_option() -> List (validation check)
#                           Go to user selection
#                               Call relevant functions
#                                   Manipulate data
#                               Display output
#           End
#
##################################################################################################

# Solitaire: Scorpion


# DO NOT DELETE THESE LINES
import cards, random
import copy

random.seed(100)  # random number generator will always generate
# the same random number (needed to replicate tests)

MENU = '''     
Input options:
    D: Deal to the Tableau (one card to first three columns).
    M c r d: Move card from Tableau (column,row) to end of column d.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''


def initialize():
    ''' This function has no parameters. It creates and initializes the stock, tableau, and foundation, and
        then returns them as a tuple, in that order. '''

    # Initialize deck object, foundation, tableau and shuffle deck
    stock = cards.Deck()
    stock.shuffle()

    foundation = [[], [], [], []]

    tableau = [[], [], [], [], [], [], []]

    # Populate tableau
    for i in range(7):

        for j in range(7):

            for k in range(7):
                tableau[j].append(stock.deal())
                break

    # Flip first 3 cards in first 3 columns
    for v in range(3):

        for x in range(3):

            tableau[v][x].flip_card()

    return (stock, tableau, foundation)


def display(stock, tableau, foundation):
    '''Display the stock and foundation at the top.
       Display the tableau below.'''

    print("\n{:<8s}{:s}".format("stock", "foundation"))
    if stock.is_empty():
        print("{}{}".format(" ", " "),
              end='')  # fill space where stock would be so foundation gets printed in the right place
    else:
        print("{}{}".format(" X", "X"), end='')  # print as if face-down
    for f in foundation:
        if f:
            print(f[0], end=' ')  # print first card in stack(list) on foundation
        else:
            print("{}{}".format(" ", " "),
                  end='')  # fill space where card would be so foundation gets printed in the right place

    print()
    print("\ntableau")
    print("   ", end=' ')
    for i in range(1, 8):
        print("{:>2d} ".format(i), end=' ')
    print()
    # determine the number of rows in the longest column
    max_col = max([len(i) for i in tableau])
    for row in range(max_col):
        print("{:>2d}".format(row + 1), end=' ')
        for col in range(7):
            # check that a card exists before trying to print it
            if row < len(tableau[col]):
                print(tableau[col][row], end=' ')
            else:
                print("   ", end=' ')
        print()  # carriage return at the end of each row
    print()  # carriage return after printing the whole tableau


def deal_from_stock(stock, tableau):
    ''' This function will deal a card from the stock to the leftmost three columns of the
        tableau. It will always deal three cards. If the stock is empty, do not deal any cards to the
        tableau. '''

    if stock.is_empty():

        pass

    else:

        # Deal from the stock
        for m in range(3):

            tableau[m].append(stock.deal())


def validate_move(tableau, src_col, src_row, dst_col):
    ''' The function will return True, if the move is valid; and False, otherwise. This function does not display
         anything. '''

    # Check if source card exists
    try:

        tableau[src_col][src_row]

    except IndexError:
        return False

    if len(tableau[dst_col]) == 0:

        # Only allows king to be added to empty column
        if 'K' not in tableau[src_col][src_row].__str__():

            return False

        else:

            pass

    # Check that source card rank is exactly on below destination card rank and suits of both cards are the same
    elif tableau[dst_col][len(tableau[dst_col]) - 1].rank() - tableau[src_col][src_row].rank() == 1 \
            and tableau[dst_col][len(tableau[dst_col]) - 1].suit() \
            == tableau[src_col][src_row].suit():
        return True

    else:
        return False

    return True


def move(tableau, src_col, src_row, dst_col):
    '''  If a move is valid (determined by calling
         validate_move), this function will update the tableau; otherwise, it will do nothing to it.  '''

    if validate_move(tableau, src_col, src_row, dst_col):

        # Move cards
        tableau[dst_col].extend(tableau[src_col][src_row:])
        tableau[src_col] = tableau[src_col][:src_row]

        try:

            # If flipped card is the last in the list, flip over
            if tableau[src_col][src_row - 1].is_face_up() == False:
                tableau[src_col][src_row - 1].flip_card()

        except IndexError:
            pass

        return True

    else:

        return False


def check_sequence(column_lst):
    ''' It returns True, if the sequence is complete and False, otherwise. '''

    if len(column_lst) != 13:
        return False

    else:

        # Compare suit and rank of adjacent cards to determine if complete suit
        for q in range(len(column_lst) - 1):

            if column_lst[q].suit() != column_lst[q + 1].suit():
                return False

            if column_lst[q].rank() - column_lst[q + 1].rank() != 1:
                return False

    return True


def move_to_foundation(tableau, foundation):
    ''' This function checks if any column sequences are complete
        (call check_sequence) and if so, move it to the foundation: '''

    for w in range(len(tableau)):

        if check_sequence(tableau[w]):

            # Add verified sequence to foundation
            for z in range(4):

                if len(foundation[z]) == 0:

                    foundation[z] = copy.deepcopy(tableau[w])
                    tableau[w].clear()
                    break

        else:

            continue


def check_for_win(foundation):
    ''' The function checks if the game has been won. '''

    for r in range(len(foundation)):

        if len(foundation[r]) == 0:

            return False

        else:

            continue

    return True

def get_option():
    '''Prompt the user for an option and check that the input has the
       form requested in the menu, printing an error message, if not.
       Return:
    D: Deal to the Tableau (one card to first three columns).
    M c r d: Move card from Tableau column,row to end of column d.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game
    '''
    option = input("\nInput an option (DMRHQ): ")
    option_list = option.strip().split()

    opt_char = option_list[0].upper()

    if opt_char in 'DRHQ' and len(option_list) == 1:  # correct format
        return [opt_char]

    if opt_char == 'M' and len(option_list) == 4 and option_list[1].isdigit() \
            and option_list[2].isdigit() and option_list[3].isdigit():
        return ['M', int(option_list[1]), int(option_list[2]), int(option_list[3])]

    print("Error in option:", option)
    return None  # none of the above


def main():
    ''' User interface to play game '''

    print("\nWelcome to Scorpion Solitaire.\n")

    stock, tableau, foundation = initialize()

    display(stock, tableau, foundation)

    print(MENU)

    option_lst = get_option()

    while option_lst and option_lst[0] != 'Q':

        error = False
        won = False

        # Deal, reset, display menu, quit
        if len(option_lst) == 1:

            if option_lst[0] == 'D':

                deal_from_stock(stock, tableau)

            elif option_lst[0] == 'R':

                stock, tableau, foundation = initialize()

            elif option_lst[0] == 'H':

                print(MENU)

            elif option_lst[0] == 'Q':

                break

        # Move cards
        elif len(option_lst) == 4:

            # Adjust indexes
            option_lst[1] -= 1
            option_lst[2] -= 1
            option_lst[3] -= 1

            if validate_move(tableau, option_lst[1], option_lst[2], option_lst[3]):

                move(tableau, option_lst[1], option_lst[2], option_lst[3])

                move_to_foundation(tableau, foundation)

                if check_for_win(foundation):

                    stock, tableau, foundation = initialize()
                    print('You won!')
                    won = True
                    print()
                    print('New Game.')

                else:

                    pass

            else:  # move failed
                print("Error in move:", option_lst[0], ",", option_lst[1] + 1, ",", \
                      option_lst[2] + 1, ",", option_lst[3] + 1)
                error = True

        if option_lst[0] == 'H' or error:

            option_lst = get_option()

        else:

            display(stock, tableau, foundation)

            if option_lst[0] == 'R' or won:
                print(MENU)
            else:
                pass

            option_lst = get_option()

    print("Thank you for playing.")

if __name__ == '__main__':
    main()
