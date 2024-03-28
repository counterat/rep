from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiogram.filters import Command
import asyncio
import requests
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
TOKEN = '7006701541:AAFk2DBM_wW2ZYUzFU0sx3QXtf4PWue2ooU'



dp = Dispatcher()

def create_play_button(invitation_code=''):
    builder = InlineKeyboardBuilder()
    builder.button(text='Играть🚀', web_app=WebAppInfo(url= f'https://host.yuriyzholtov.com/{invitation_code}'))
    return builder

def create_buttons_for_admin():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Статистика')
    builder.button(text='Слив')
    builder.button(text='Поменять баланс юзеру')
    return builder
""" 🚀 """

def create_buttons_for_detailed_stats():
    builder = InlineKeyboardBuilder()
    builder.button(text='Показать статистику по ставками', callback_data='show_stats_about_bets')
    builder.button(text='Показать статистику по играм', callback_data='show_stats_about_games')
    builder.button(text='Показать статистику по пользователям', callback_data='show_stats_about_users')
    builder.adjust(1,1,1)
    return builder
    
@dp.message(lambda msg : msg.text == 'Слив')
async def fuck_up_next_game( message:  types.Message):
    data = {"login":"admin", "password":"DHICvBAAS0ue"}
    resp = requests.post('https://host.yuriyzholtov.com/authadmin',json=data)
    cookie = resp.cookies.get('aero')
    cookies ={
        "aero":cookie
    }

    resp1 = requests.post('https://host.yuriyzholtov.com/fuckup', cookies=cookies)
  
    answer_from_server = resp1.json()
    is_ok = answer_from_server['is_ok']
    if is_ok:
        await message.answer('Следующая игра будет слита!')
        return  
    await message.answer('Что то пошло не так...')
    return 


class States(StatesGroup):
    first = State()
    second = State()

@dp.message(States.first)
async def input_num(message:  types.Message, state: FSMContext):
    try:
        num = int(message.text)
        data = {"login":"admin", "password":"DHICvBAAS0ue"}
        data = {"login":"admin", "password":"DHICvBAAS0ue"}
        resp = requests.post('https://host.yuriyzholtov.com/authadmin',json=data)
        cookie = resp.cookies.get('aero')
        cookies ={
            "aero":cookie
        }

        resp1 = requests.post('https://host.yuriyzholtov.com/changebalanceforuser', cookies=cookies, json={"user_id":num})
         
        answer_from_server = resp1.json()
        if answer_from_server['is_ok']:
            
            await state.set_state(States.second)
            await state.set_data({'user_id':num})
            return  await message.answer('Введите сумму желаемую сумму баланса')
        return  await message.answer('Что то пошло не так...')
    except Exception as ex:
        print(ex)
        return await message.answer('Вы ввели не число!Повторите попытку еще раз')


@dp.message(States.second)
async def input_num2(message:  types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        data = {"login":"admin", "password":"DHICvBAAS0ue"}
        data = {"login":"admin", "password":"DHICvBAAS0ue"}
        resp = requests.post('https://host.yuriyzholtov.com/authadmin',json=data)
        cookie = resp.cookies.get('aero')
        cookies ={
            "aero":cookie
        }
        result = (await state.get_data())['user_id']
   
        resp1 = requests.post('https://host.yuriyzholtov.com/changebalanceforuser2', cookies=cookies, json={"user_id":result, "amount":amount})
    
        answer_from_server = resp1.json()
        if answer_from_server['is_ok']:
            return  await message.answer('Успешно изменен баланс!')
        return  await message.answer('Что то пошло не так...')
    except:
        return await message.answer('Вы ввели не число!Повторите попытку еще раз')
    finally:
        await state.clear()
@dp.message(lambda msg : msg.text == 'Поменять баланс юзеру')
async def fuck_up_next_game( message:  types.Message, state: FSMContext):
    data = {"login":"admin", "password":"DHICvBAAS0ue"}
    resp = requests.post('https://host.yuriyzholtov.com/authadmin',json=data)
    cookie = resp.cookies.get('aero')
    cookies ={
        "aero":cookie
    }

    resp1 = requests.post('https://host.yuriyzholtov.com/get_users', cookies=cookies)
  
    answer_from_server = resp1.json()
    if answer_from_server['is_ok']:
        users_data = answer_from_server['users_data']
        msg = ''
        for user in users_data:
            msg += f'''\n {user['id']}) telegram_id = {user['telegram_id']} , username = {user['username']} , deposit_balance = {user['deposit_balance']}'''
        await message.answer(msg)
        await state.set_state(States.first)
            
        await message.answer('отправьте номер под которым находится юзер которому вы хотите поменять баланс')

        return
    return  await message.answer('Что то пошло не так...')

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
            all_dep_prices = []
            all_bonus_prices = []
            all_dep_wons = []
            all_bonus_wons = []
            all_dep_loses = []
            all_bonus_loses = []
            for bet in bets_data:
                if not bet['fake']:
                    if bet['baltype'] == 'deposit':
                        all_dep_prices.append(bet['price'])
                        if bet['won']:
                            all_dep_wons.append(bet['won'])
                        else:
                            all_dep_loses.append(bet['price'])
                    else:
                        all_bonus_prices.append(bet['price'])
                        if bet['won']:
                            all_bonus_wons.append(bet['won'])
                        else:
                            all_bonus_loses.append(bet['price'])
            await query.message.answer(f'''

Сумма на которую люди наставили ставок (депы+бонусы) = {sum(all_dep_prices) + sum(all_bonus_prices)}

Общая сумма ставок с деп баланса =  {sum(all_dep_prices) }
Сумма выигрышей с деп баланса = {sum(all_dep_wons)}
Сумма проигрышей с деп баланса = {sum(all_dep_loses)}
Самый большой выигрыш (деп баланс) = {max(all_dep_wons) if all_dep_wons else None}
Самый большой проигрыш (деп баланс) = {max(all_dep_loses) if all_dep_loses else None}


Общая сумма ставок с бонус баланса =  {sum(all_bonus_prices) }
Сумма выигрышей с бонус баланса = {sum(all_bonus_wons)}
Сумма проигрышей (бонус баланс) = {sum(all_bonus_loses)}

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
                total_amount_of_money_losed.append(user['total_amount_of_money_losed'])


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
    
@dp.message(Command('start'))
async def start_handler(messsage, command):
        

        await messsage.answer('🔥', reply_markup=create_buttons_for_admin().as_markup())
        if command.args:
            await messsage.answer('Для запуска, нажмите на кнопку 👇', reply_markup=create_play_button(command.args).as_markup())
    
        else:
            await messsage.answer('Для запуска, нажмите на кнопку 👇', reply_markup=create_play_button().as_markup())


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == '__main__':


    asyncio.run(main())
