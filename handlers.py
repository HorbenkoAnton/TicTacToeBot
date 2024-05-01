from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from game import TicTacToe , Game_Bot
import kb
import text
import time
games = {}
game_bots = {}
router = Router()

coordinates_map = {
     "a1": [0,0],
     "a2": [1,0],
     "a3": [2,0],
     "b1": [0,1],
     "b2": [1,1],
     "b3": [2,1],
     "c1": [0,2],
     "c2": [1,2],
     "c3": [2,2]
}


@router.message(Command("start"))
async def start_handler(msg:Message):
    await msg.answer(text.start)

@router.message(Command("tictactoe"))
async def tic_tac_toe_handler(msg:Message):
     games[msg.chat.id] = TicTacToe()
     game_bots[msg.chat.id] = Game_Bot()
     game = games[msg.chat.id]
     
     await msg.answer(text.tictactoe,reply_markup=kb.get_map(game.get_state()))
     

@router.callback_query()
async def player_input(callback_query: types.CallbackQuery):

    data = callback_query.data 
    game_bot = game_bots[callback_query.message.chat.id]
    game = games[callback_query.message.chat.id]


    #Decorator func for game_checker
    async def is_game_ended(game_checker ,state):
        winner = game_checker(state)
        if winner == -1:
            await callback_query.message.answer("The O won!")
            await callback_query.message.edit_reply_markup(reply_markup=None)
            game.clear_state()
            return
        elif winner == 0:
            await callback_query.message.answer("It's draw")
            await callback_query.message.edit_reply_markup(reply_markup=None)
            game.clear_state()
            return
        elif winner == 1:
            await callback_query.message.answer("The X won!")
            await callback_query.message.edit_reply_markup(reply_markup=None)
            game.clear_state()
            return
        elif winner is None:
            return


    #Turn handler
    if data in coordinates_map:
        coordinates = coordinates_map[data]
        state = game.get_state()
    

        #Player's turn
        if state[coordinates[0]][coordinates[1]] != 0:
            await callback_query.message.answer(text.wrong_spot)
            return
        game.make_turn(*coordinates)
        state = game.get_state()
        await is_game_ended(game.game_checker ,state)
        await callback_query.message.edit_reply_markup(reply_markup=kb.get_map(state))
        
        

        #testing features
        
        #Bot's turn
        if game.player() == -1:
            minimaxResult = game_bot.minimax(state,True)
            game.make_turn(*minimaxResult[1])
            state = game.get_state()
            await is_game_ended(game.game_checker ,state)
            await callback_query.message.edit_reply_markup(reply_markup=kb.get_map(state))



    else:
        await callback_query.message.answer("Invalid input.")