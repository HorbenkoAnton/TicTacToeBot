from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def state_mutator(state):
    return [['X' if cell == 1 else 'O' if cell == -1 else ' ' for cell in row] for row in state]

def get_map(state):
    local_state = state.copy()
    local_state = state_mutator(local_state)
    tictactoe = [
    [InlineKeyboardButton(text=local_state[0][0] ,callback_data="a1"),
     InlineKeyboardButton(text=local_state[1][0],callback_data="a2"),
     InlineKeyboardButton(text=local_state[2][0],callback_data="a3")],
    [InlineKeyboardButton(text=local_state[0][1],callback_data="b1"),
     InlineKeyboardButton(text=local_state[1][1],callback_data="b2"),
     InlineKeyboardButton(text=local_state[2][1],callback_data="b3"),],
    [InlineKeyboardButton(text=local_state[0][2],callback_data="c1"),
     InlineKeyboardButton(text=local_state[1][2],callback_data="c2"),
     InlineKeyboardButton(text=local_state[2][2],callback_data="c3")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=tictactoe)