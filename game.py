from copy import deepcopy
import random

class TicTacToe:
    
    def __init__(self) -> None:
        self.__state = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ]

    def clear_state(self):
        self.__state = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
        ]

    def get_state(self):
        return self.__state
    
    def player(self,stateArgument = None):
        state = stateArgument if stateArgument is not None else self.__state
        X_turns = 0
        O_turns = 0
        for a in range(0,3):
            X_turns += state[a].count(1)
            O_turns += state[a].count(-1)
        if X_turns != 0 or O_turns != 0:
            if X_turns > O_turns:
                return -1
            else: return 1
        else: return 1

    def make_turn(self,x,y):
        current_player = self.player()
        x = int(x)
        y = int(y)
        if x not in range(0, 3) or y not in range(0, 3):
            return
        if self.__state[x][y] == 0:
            self.__state[x][y] = current_player
        else:
            print("You picked wrong place")
        
    def game_checker(self, stateArgument=None):
        state = stateArgument if stateArgument is not None else self.__state

        # Define a function to check wins for a player
        def check_win(player):
            # Check horizontal and vertical wins
            for i in range(3):
                if all(state[i][j] == player for j in range(3)) or all(state[j][i] == player for j in range(3)):
                    return True

            # Check diagonal wins
            if all(state[i][i] == player for i in range(3)) or all(state[i][2-i] == player for i in range(3)):
                return True

            return False

        # Check for wins
        if check_win(1):
            return 1
        elif check_win(-1):
            return -1

        # Check for a draw (all spots are used)
        if all(element != 0 for row in state for element in row):
            return 0

        # If the game is not ended
        return None


class Game_Bot(TicTacToe):

    #result of action on state
    def result(self, state, action):
        # Make a deep copy of the state to avoid mutating the original state
        new_state = [row[:] for row in state]
        # Extract row and column from the action
        row, col = action
        current_player = self.player(state)
        
        # Apply the action to the state
        if new_state[row][col] == 0:  # Ensure the spot is empty
            new_state[row][col] = current_player
        else:
            raise ValueError("Invalid action: Position already taken.")
        
        return new_state
    

    #Returns list of all possible turns
    def get_actions(self,state): 
        actions = []
        for y in range(0,3):
            for x in range(0,3):
                if state[y][x] == 0:
                    actions.append([y,x])
        return actions
    
    def calculate_depth(self, state):
        empty_spots = sum(row.count(0) for row in state)
        return empty_spots

    #returns result of action on state
    def minimax(self, state, isMinimizingPlayer):
        actions = self.get_actions(state)

        if self.game_checker(state) is not None:
            return [self.game_checker(state), None ]
        

        best_action = None
        if isMinimizingPlayer:
            best_score = float('inf')
            for action in actions:
                potentialState = self.result(state, action)
                score, _ = self.minimax(potentialState, False)
                if score < best_score:
                    best_score, best_action = score, action
        else:
            best_score = float('-inf')
            for action in actions:
                potentialState = self.result(state, action)
                score, _ = self.minimax(potentialState, True)
                if score > best_score:
                    best_score, best_action = score, action

        return [best_score, best_action]
