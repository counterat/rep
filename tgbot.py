from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.types import MenuButtonWebApp, WebAppInfo
import asyncio
import requests
TOKEN = '7006701541:AAFk2DBM_wW2ZYUzFU0sx3QXtf4PWue2ooU'



dp = Dispatcher()

def create_play_button():
    builder = InlineKeyboardBuilder()
    builder.button(text='Играть🚀', web_app=WebAppInfo(url= 'https://host.yuriyzholtov.com/'))
    return builder

def create_buttons_for_admin():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Статистика')
    return builder
""" 🚀 """

def create_buttons_for_detailed_stats():
    builder = InlineKeyboardBuilder()
    builder.button(text='Показать статистику по ставками', callback_data='show_stats_about_bets')
    builder.button(text='Показать статистику по играм', callback_data='show_stats_about_games')
    builder.button(text='Показать статистику по пользователям', callback_data='show_stats_about_users')
    builder.adjust(1,1,1)
    return builder
    

@dp.message(lambda msg : msg.text == 'Статистика')
async def show_stats(message:  types.Message):
    data = {"login":"admin", "password":"DHICvBAAS0ue"}
    resp = requests.post('https://host.yuriyzholtov.com/authadmin',json=data)
    cookie = resp.cookies.get('aero')
    cookies ={
        "aero":cookie
    }

    resp1 = requests.post('https://host.yuriyzholtov.com/get_stats', cookies=cookies)
  
    stats = resp1.json()
    bets_data = stats['bets_data']
    games_data = stats['games_data']
    settings = stats['settings']
 
    users_data = stats['users_data']
    await message.answer(f'''
Данные приведены снизу
Прибыль - {settings['profit_money']} рублей
Минимальная сумма для ставки - {settings['min_bet']} рублей
Максимальная сумма для ставки - {settings['max_bet']} рублей
Комиссия для вывода - {settings['jackpot_comission']} рублей
Перерыв между играми - {settings['crash_timer']} секунд                       
                         ''', reply_markup=create_buttons_for_detailed_stats().as_markup())
    
@dp.callback_query(lambda query: query.data.startswith('show_stats_about_'))
async def handle_detailed_stats(query:types.CallbackQuery):
    data = {'login':'admin', 'password':'DHICvBAAS0ue'}
    resp = requests.post('https://host.yuriyzholtov.com/authadmin',json=data)
    cookie = resp.cookies.get('aero')
    cookies ={
        "aero":cookie
    }
    resp1 = requests.post('https://host.yuriyzholtov.com/get_stats', cookies=cookies)
    stats = resp1.json()
    bets_data = stats['bets_data']
    games_data = stats['games_data']
    settings = stats['settings']
    users_data = stats['users_data']
    data_about = query.data.split('_')[-1]
    print(data_about)
    
    if data_about == 'bets':
        if bets_data:
            sum_of_bet_prices = 0
            sum_of_bonus_prices= 0
            sum_of_won = 0
            sum_of_won_for_dep = 0
            all_bets_prices = []
            all_deposit_prices= []
            for bet in bets_data:
                sum_of_bet_prices += bet['price']
                if bet['won']:
                    sum_of_won += bet['won']
                all_bets_prices.append(bet['price'])

                if bet['baltype'] == 'bonus':
                    sum_of_bonus_prices += bet['price']
                else:
                    all_deposit_prices.append(bet['price'])
                    if bet['won']:
                        sum_of_won_for_dep += bet['won']

            await query.message.answer(f'''
Информация о ставках:
Общее количество ставок: {len(bets_data)}
Общая сумма ставок (депозитный баланс+бонусный) - {sum(all_bets_prices)}
Общая сумма бонусных ставок - {sum_of_bonus_prices}
Общая сумма депозитных ставок - {sum(all_deposit_prices)}
Общая сумма выигрышей у юзеров (депозитный баланс+бонусный) - {sum_of_won}
Сумма выигрыши (только депозитные балансы) - {sum_of_won_for_dep}
Максимальная ставка - {max(all_bets_prices)}
Максимальная депозитная ставка - {max(all_deposit_prices)}
''')
        else:
            await query.message.answer('К сожалению пользователи пока не делали никаких ставок')
    elif data_about == 'games':
        if games_data:
            all_multipliers = []
            all_profits = []
            for game in games_data:
                all_multipliers.append(game['multiplier'])
                all_profits.append(game['profit'])
            await query.message.answer(f'''
Информация о играх:
Общее количество игр - {len(games_data)}
Самый высокий коефф - {max(all_multipliers)}
Общий профит (со стороны казино) - {sum(all_profits)}
Профит самой прибыльной игры - {max(all_profits)}
Профит самой убыточной игры - {min(all_profits)}

''')
        else:
            await query.message.answer('К сожалению пока нету никаких игр')
    elif data_about == 'users':
        if users_data:
            all_deposit_balances = []
            all_bonus_balances = []
            total_amount_of_money_won = []
            total_amount_of_money_losed = []
            for user in users_data:

                all_deposit_balances.append(user['deposit_balance'])
                all_bonus_balances.append(user['bonus_balance'])
                total_amount_of_money_won.append(user['total_amount_of_money_won'])
                total_amount_of_money_losed.appen(user['total_amount_of_money_losed'])


            await query.message.answer(f'''
Информация о пользователях:
Общее количество юзеров - {len(users_data)}
Общая сумма на дпозитных балансах у юзеров - {sum(all_deposit_balances)}
Общая сумма на бонусных балансах у юзеров - {sum(all_bonus_balances)}
Самая большая сумма депозитного баланса - {max(all_deposit_balances)}
Самая большая сумма бонусного баланса - {max(all_bonus_balances)}
Общее количество проигранных денег (для юзеров) - {sum(total_amount_of_money_losed)}
Самая большая проигранная сумма - {max(total_amount_of_money_losed)}
Общее количество выигранных денег (для юзеров) - {sum(total_amount_of_money_won)}
Самый большой выигрыш - {max(total_amount_of_money_won)}

''')
        else:
            await query.message.answer('К сожалению пока нету юзеров')
    
@dp.message(lambda F :F.text== '/start')
async def start_handler(messsage:types.Message):
    
        await messsage.answer('🔥', reply_markup=create_buttons_for_admin().as_markup())
        await messsage.answer('Для запуска, нажмите на кнопку 👇', reply_markup=create_play_button().as_markup())
    
        


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == '__main__':


    asyncio.run(main())