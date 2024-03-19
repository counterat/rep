from __init__ import *
from flask import Flask, render_template, request, render_template_string, make_response, jsonify
from flask_socketio import SocketIO
from models import *
from api.main import api_bp
import random
from decimal import Decimal, ROUND_DOWN
from apscheduler.schedulers.background import BackgroundScheduler
import time
import json
import threading
from bs4 import BeautifulSoup
#from pyrog_client import get_random_members_of_chat
import re
from payments import cryptomus
import uuid
import jwt 
def replace_braces_with_empty_string(html):
    cleaned_html = re.sub(r'[{}$@]', '', html)
    return cleaned_html
    return str(soup)

config_for_admin = {
    'login': 'admin',
    'password':"DHICvBAAS0ue"
}
app.register_blueprint(api_bp, url_prefix='/api')

fake_bets = []
current_multiplier = 1
users_and_avatars = {'Эмил': 'https://res.cloudinary.com/du73oow82/image/upload/v1707406838/ujaqwypgrispgiptrjx9.jpg', 'ДОКУМЕНТ': 'https://res.cloudinary.com/du73oow82/image/upload/v1707406839/ef7odcaabmojrofncyvk.jpg', '𝐌𝐞𝐧𝐝𝐚 𝐪𝐨𝐥𝐦𝐚𝐝𝐢 𝐝𝐢𝐥 ❤️': 'https://res.cloudinary.com/du73oow82/image/upload/v1707406840/ppqit540z9zgtonwvhbm.jpg', 'Qwerty': 'https://res.cloudinary.com/du73oow82/image/upload/v1707406842/rjpgsxltppsnduysacby.jpg', 'Рустам': 'https://res.cloudinary.com/du73oow82/image/upload/v1707406844/ohzez5sn6vkzjuxduibl.jpg', 'Gulmira': 'https://res.cloudinary.com/du73oow82/image/upload/v1707406845/wqboqod0ewjlm6sl5frg.jpg', 'Лиля': 'https://res.cloudinary.com/du73oow82/image/upload/v1707406847/vgg5lteawwm8i7jleaun.jpg', '𓄂༗࿐ Шохрухбе 𓄂༗࿐': 'https://res.cloudinary.com/du73oow82/image/upload/v1707406848/quh5u11e2xsc7pg7ptvv.jpg', 'Бахтиёр': 'https://res.cloudinary.com/du73oow82/image/upload/v1707406849/qddpautopk6py0jlv3qt.jpg', '𓃬 𖤓 ДеД 𖤓 ♚Шох♚ Ака 𓃬': 'https://res.cloudinary.com/du73oow82/image/upload/v1707406851/ogkyynvcrkne3zbzjj6d.jpg'}

@app.route('/payment',  methods=['POST', 'GET'])
def payment_info():
    response = request.json
    uuid = response['uuid']
    if 'test' not in response['order_id']:
        with SessionFactory() as session:
            payment = session.query(Payments).filter(Payments.uuid == uuid).first()
            if response['status'] == 'paid':
                payment.status = 'paid'
                user = session.query(User).filter(User.id==payment.user_id).first()
                user.deposit_balance += response['merchant_amount']
                
        print(request.remote_addr)
    return '1'
def generate_token(login, password):
    token = jwt.encode({'login': login, 'password': password}, 'secret_key', algorithm='HS256')
    return token
@app.route('/authadmin', methods=['POST'])
def authadmin():
    data = request.json

    login = data['login']
    password = data['password']
    response = make_response('ok')
 
    if login == config_for_admin['login'] and password == config_for_admin['password']:
        response.set_cookie('aero', generate_token(login, password))

    return response

session_for_api = SessionFactory()

fuck_up_next_game = False


@app.route('/changebalanceforuser2', methods=['POST'])
def changebalanceforuser2():
    cookie_value = request.cookies.get('aero')
    if jwt.decode(cookie_value, "secret_key", algorithms="HS256"):
        user_id = request.json['user_id']
        amount = request.json['amount']
        user = session_for_api.query(User).filter(User.id == user_id).first()
        user.deposit_balance = amount
        session_for_api.commit()
        return jsonify({ 'is_ok':True})
    return jsonify({ 'is_ok':False})
@app.route('/changebalanceforuser', methods=['POST'])
def changebalanceforuser():
    cookie_value = request.cookies.get('aero')
    if jwt.decode(cookie_value, "secret_key", algorithms="HS256"):
        user_id = request.json['user_id']
        user = session_for_api.query(User).filter(User.id == user_id).first()
        if user:
            return jsonify({ 'is_ok':True})
    return jsonify({ 'is_ok':False})
@app.route('/get_users', methods=['POST'])
def get_users_for_tgbot():
    cookie_value = request.cookies.get('aero')
    if jwt.decode(cookie_value, "secret_key", algorithms="HS256"):
        all_users = session_for_api.query(User).all()
        users_data = []
        for user in all_users:
            print(user)
            users_data.append({column.name: getattr(user, column.name) for column in User.__table__.columns if column.name != 'created_at'})
            
        return jsonify({ 'is_ok':True,'users_data':users_data})
    
    return jsonify({ 'is_ok':False})
@app.route('/fuckup', methods=['POST'])
def fuckup():
    cookie_value = request.cookies.get('aero')
    if jwt.decode(cookie_value, "secret_key", algorithms="HS256"):
        global fuck_up_next_game
        fuck_up_next_game = True
        print(fuck_up_next_game, 'fuck')
        return jsonify({'is_ok':True})
    return jsonify({'is_ok':False})
@app.route('/get_stats', methods=['POST'])
def get_stats():
    cookie_value = request.cookies.get('aero')
    
    with session_for_api.begin():
            all_users = session.query(User).all()
            bets = session.query(CrashBets).all()
            games = session.query(Crash).all()
            settings=session.query(Settings).first()
    users_data = []
    bets_data = []
    games_data = []

    for user in all_users:
        users_data.append({column.name: getattr(user, column.name) for column in User.__table__.columns if column.name != 'created_at'})
    for bet in bets:
        bets_data.append({column.name: getattr(bet, column.name) for column in CrashBets.__table__.columns if column.name != 'created_at'})
    for game in games:
        games_data.append({column.name: getattr(game, column.name) for column in Crash.__table__.columns if column.name != 'created_at'})
    settings = {column.name: getattr(settings, column.name) for column in Settings.__table__.columns if column.name != 'created_at'}
    if jwt.decode(cookie_value, "secret_key", algorithms="HS256"):
        return jsonify({'users_data' :users_data, 'bets_data':bets_data, 'games_data':games_data, 'settings':settings})

@app.route('/')
def index():
    response = cryptomus({
	"uuid": "e1830f1b-50fc-432e-80ec-15b58ccac867",
	"currency": "ETH",
	"url_callback": "https://host.yuriyzholtov.com/payment",
	"network": "eth",
	"status": "paid"
},  "https://api.cryptomus.com/v1/test-webhook/payment")


    return render_template('main_design.html', ip_adress=request.remote_addr, is_game_in_progress=is_any_game_in_progress())
    #return render_template('new.html', ip_adress=request.remote_addr, is_game_in_progress=is_any_game_in_progress())
    with open('C:/Users/Юрий/Desktop/gambling/templates/plane.html', 'r', encoding='utf-8') as file:
        html = file.read()
    page = replace_braces_with_empty_string(html)
    return render_template_string(page)


@socketio.on('connect')
def handle_connect():
    client_sid = request.sid


    socketio.emit('message_from_server', {'message': 'Hello, client!'}, room=client_sid )
@socketio.on('disconnect')
def handle_disconnect():
    client_sid = request.sid  


@app.route('/authorize', methods=['POST'])
def handle_message():
    with SessionFactory() as session:
        with session.begin():
            data = request.json

            username = data.get("id")
            print(username)
            
            user = session.query(User).filter(User.telegram_id == username).first()
            if user:
                attributes_dict = {column.name: getattr(user, column.name) for column in User.__table__.columns}
                payment = session.query(Payments).filter(Payments.user_id == user.id).order_by(Payments.id.desc()).first()
                if payment:
                    payment_attributes_dict = {
    column.name: getattr(payment, column.name)
    for column in Payments.__table__.columns
    if column.name != 'created_at'  # Исключаем поле 'created_at'
}
                    return{"user":attributes_dict, 'payments':payment_attributes_dict}
                    return
                
                return{"user":attributes_dict}
            print(data)
            new_user = session.merge( create_new_user(username,data.get("tgusername") ))
            attributes_dict = {column.name: getattr(new_user, column.name) for column in User.__table__.columns}
          
            return {"user":attributes_dict}

def generate_unique_uuid(session):
    while True:
        # Генерируем случайный UUID
        new_uuid = uuid.uuid4()
   
        # Проверяем, существует ли уже такой UUID в базе данных
        
        existing_record = session.query(Payments).filter(Payments.order_id == str(new_uuid)).first()
        if not existing_record:
                # Если такого UUID еще нет в базе данных, возвращаем его
            return str(new_uuid)

@socketio.on('topUpBalance')
def top_up_balance_handler(data):
    with SessionFactory() as session:   
            with session.begin():
                client_id = request.sid
                user_id = data.get('user_id')
                amount = data.get('amount')
                user = session.query(User).filter(User.id == user_id).first()
                if user:
                    payment = cryptomus({
                        "amount":f"{amount}",
                        "currency" :'rub',
                        "order_id":generate_unique_uuid(session),
                        'url_return':'http://127.0.0.1:5000/#',
                        'url_callback':"https://host.yuriyzholtov.com/payment"




                    }, 'https://api.cryptomus.com/v1/payment')
                    
                    if payment:
                      
                        payment_in_db = Payments(user_id=user.id, amount = float(amount), currency = 'RUB',  uuid= payment['result']['uuid'], status = payment['result']['status'], created_at = datetime.now(), order_id = payment['result']['order_id'], address = payment['result']['address'], url = payment['result']['url'] )
                        session.add(payment_in_db)
                        socketio.emit('generate_widget_for_payment', {'url':payment['result']['url']}, room=client_id)
                
                else:
                    socketio.emit('error', {'messsage':'you are not authorized'}, room=client_id)




@socketio.on('new_bet')
def new_bet_handler(data:dict):
    with SessionFactory() as session:
        with session.begin():
            client_sid = request.sid  
            settings = session.query(Settings).first()
    
            game_id = data['game_id']
            user_id = data['user_id']
            bet_in_usd = data['bet_in_usd']
            baltype = data['baltype']
 

            game = session.query(Crash).filter(Crash.id == game_id).first()
            user = session.query(User).filter(User.id == user_id).first()
            if baltype == 'deposit':
                if not (user.deposit_balance >= bet_in_usd):
                
                            return socketio.emit("not_enough_funds_on_the_balance", {"message":"не хватает средств на балансе!"}, room=client_sid)
            if baltype == 'bonus':
                if not (user.bonus_balance >= bet_in_usd):
                
                            return socketio.emit("not_enough_funds_on_the_balance", {"message":"не хватает средств на балансе!"}, room=client_sid)
            
            if game.status == 0:
                if settings.min_bet > bet_in_usd:
                    return socketio.emit("not_enough_funds_on_the_balance", {"message":f"Минимальная сумма ставки - {settings.min_bet}"}, room=client_sid)
                
                if baltype == 'deposit' and user.deposit_balance>=bet_in_usd and settings.min_bet<=bet_in_usd:
           
                    
                    user.deposit_balance -= bet_in_usd
                    

                    new_bet = session.merge(new_bet_create(user_id = user.id, round_id = game.id, price = bet_in_usd,  status = 0, fake = 0, baltype = baltype ))
               
                    attributes_dict = {
    column.name: getattr(new_bet, column.name)
    for column in CrashBets.__table__.columns
    if column.name != 'created_at'  # Исключаем поле 'created_at'
}                   
              
                    socketio.emit("successful_bet", attributes_dict, room=client_sid)
                if baltype == 'ref' and user.referal_balance>=bet_in_usd and settings.min_bet<=bet_in_usd:
                    user.referal_balance -= bet_in_usd
                    new_bet = session.merge(new_bet_create(user_id = user.id, round_id = game.id, price = bet_in_usd,  status = 0, fake = 0, baltype = baltype ))
                   
                    attributes_dict = {
    column.name: getattr(new_bet, column.name)
    for column in CrashBets.__table__.columns
    if column.name != 'created_at'  # Исключаем поле 'created_at'
}
                    socketio.emit("successful_bet", attributes_dict, room=client_sid)
                if baltype == 'bonus' and user.bonus_balance>=bet_in_usd and settings.min_bet<=bet_in_usd:
                    user.bonus_balance -= bet_in_usd
                    new_bet = session.merge(new_bet_create(user_id = user.id, round_id = game.id, price = bet_in_usd,  status = 0, fake = 0, baltype = baltype ))
                   
         
                    attributes_dict = {
    column.name: getattr(new_bet, column.name)
    for column in CrashBets.__table__.columns
    if column.name != 'created_at'  # Исключаем поле 'created_at'
}
                    socketio.emit("successful_bet", attributes_dict, room=client_sid)
            elif game.status == 1:
                socketio.emit("impossible_to_make_a_bet", {"message":"The game already in process"}, room=client_sid)
            elif game.status ==2:
                socketio.emit("impossible_to_make_a_bet", {"message":"The game is already finished"}, room=client_sid)
@socketio.on('pickupwinning')
def pickupwinning_handler(data):  
    if current_multiplier > 1.02:
        with SessionFactory() as session:
            with session.begin():
                client_sid = request.sid  

                bet = session.query(CrashBets).filter(CrashBets.id == data['bet']).first()
                current_game = get_current_game()
                current_game = session.merge(current_game)
                settings = session.query(Settings).first()
                if bet.round_id != current_game.id:
                    return 
                if bet.status == 1:
                    return socketio.emit("error", {"message":"Вы уже проиграли в этой игре"}, room=client_sid)
                if bet.status == 2:
                    return socketio.emit("error", {"message":"Вы уже забрали свой выигрыш!"}, room=client_sid)
                bet.status = 2
                user = session.query(User).filter(User.id == bet.user_id).first()
                multiplier_at_the_moment = current_multiplier
                win = bet.price * multiplier_at_the_moment
                if bet.baltype == 'deposit':
                    current_game.profit -= win-bet.price
                    user.deposit_balance += win
                 
                    user.total_amount_of_money_won += win
                    settings.profit_money -= win-bet.price
                else:
                    user.bonus_balance += win
                user.number_of_wins += 1
                
                
                bet.status = 2
                bet.won += win-bet.price
                attributes_dict = {column.name: getattr(user, column.name) for column in User.__table__.columns if column.name != 'created_at'}
                socketio.emit("you_got_new_winning", {"amount":win, "multiplier_at_the_moment": multiplier_at_the_moment, "user":attributes_dict , "baltype":bet.baltype}, room=client_sid)



@app.route('/get_bets')
def get_bets():
    print(fake_bets)
   
    game = session.query(Crash).filter(Crash.status == 1).order_by(Crash.id.desc()).first()
    if game:
           
        
        print('VAZHNO', fake_bets,'VAZHNO')
        bets_to_send=[]
        if fake_bets:
            for fake_bet in fake_bets:
                for username in fake_bet:
                    bet_to_send = session.query(CrashBets).filter(CrashBets.id == fake_bet[username]['id']).first()
                    bet_to_send = {column.name: getattr(bet_to_send, column.name) for column in CrashBets.__table__.columns if column.name != 'created_at'}
                    bet_to_send['username'] = username
                    bet_to_send['avatar_url'] = fake_bet[username]['avatar_url']
                    bets_to_send.append(bet_to_send)
            return jsonify({'bets':bets_to_send})
    return '1'


@socketio.on('get_previous_xes')
def return_previous_xes():
    client_sid = request.sid
    previous_games =  session.query(Crash).filter(Crash.status == 2).order_by(Crash.id.desc()).all() 
    previous_xes = []
    if len(previous_games) >= 20:
        
        for game in previous_games[:20]:
            previous_xes.append(game.multiplier)
    
        return socketio.emit('previous_xes', {'data':previous_xes }, room=client_sid)    
    
    for game in previous_games:
        previous_xes.append(game.multiplier)    
    return  socketio.emit('previous_xes', {'data':previous_xes }, room=client_sid)



def new_game():
    game = Crash(status=0)
    with SessionFactory() as session_for_thread:
        with session_for_thread.begin():
        
            session_for_thread.add(game)
          
    return game

def is_any_game_in_progress():
    with SessionFactory() as session:
        with session.begin():
            games_that_in_process = session.query(Crash).filter(Crash.status == 1).all()
            if games_that_in_process:
                return True
            return False

def get_current_game():
    with SessionFactory() as session_for_thread:
        with session_for_thread.begin():
            game = session.query(Crash).order_by(Crash.id.desc()).first()
    return game


def check_and_execute():
    game_list = []
    connection_pool = engine.pool

# Получите количество активных соединений
    active_connections = connection_pool.checkedout()

    with SessionFactory() as session_for_thread:
        
        with session_for_thread.begin():
            settings = session_for_thread.query(Settings).first()
            print(settings.profit_money)
            games_that_have_not_begin_yet = session_for_thread.query(Crash).filter(Crash.status == 0).all()
            games_that_in_process = session_for_thread.query(Crash).filter(Crash.status == 1).all()


        if (not games_that_have_not_begin_yet and not games_that_in_process): #and session.query(Crash).all():
    
               

            with session_for_thread.begin():
                game = new_game()
                game = session_for_thread.merge(game)
                games= session_for_thread.query(Crash).all()
                game_list.append(game)
       
         
            used_users = []
            
            fake_bets.clear()
            for item in users_and_avatars.items():
                username = item[0]
          
                        
           
                if username not in used_users:
                    fake_bet = new_bet_create(user_id=1, round_id=game.id, price=random.randint(1, 1000), status=0, fake=True, baltype='deposit')
                    fake_bet = session_for_thread.merge(fake_bet)
                    fake_bet = {column.name: getattr(fake_bet, column.name) for column in CrashBets.__table__.columns if column.name != 'created_at'}
                    fake_bet['avatar_url'] = users_and_avatars[username]
                    fake_bet['username'] = username
                    
                    fake_bets.append( {username:fake_bet})
                    used_users.append(username)
                    print(username )
                    
                
            used_bets = []
            for i in range(61):
                """ if i %10 == 0:
              
                    random_num = random.random()
                    if random_num > 0.3:
                        random_user = session_for_thread.query(User).filter(User.id == random.randint(1,10)).first()
                        if not session_for_thread.query(CrashBets).filter(CrashBets.round_id == game.id).filter(CrashBets.user_id == random_user.id).first():
                            last_bet =  session_for_thread.query(CrashBets).filter(CrashBets.user_id == random_user.id).order_by(CrashBets.round_id.desc()).first()
                            random_bet = random.randint(10, 100)
                            if last_bet:
                                if not last_bet.won:
                                    if 2 * last_bet.price <= random_user.deposit_balance:
                                        random_bet = 2 * last_bet.price
                                    else:
                                        if random_user.deposit_balance >= 1:
                                            import math
                                            random_bet = math.floor(random_user.deposit_balance)
                                else: 
                                    random_bet = last_bet.price
                            if random_user.deposit_balance >= 1 and random_bet >= 1:
                                random_user.deposit_balance -= random_bet
                                session_for_thread.commit()
                                bet = new_bet_create(random_user.id, game.id, random_bet,status=0,fake=0,baltype='deposit')  """

                bets_to_send = [] 
                num_elements = random.randint(0, 2)
                random_elements = random.sample(fake_bets, num_elements)
                for element in random_elements:
                    for key in element:
                        if element[key]['id'] not in used_bets and (i%2==0):

                            used_bets.append(element[key]['id'])
                            bets_to_send.append(element)
                        

                socketio.emit("time_remaining", {"seconds_remained" : i, "for_game":game.id, "fake_bets":bets_to_send})
                
                time.sleep(0.1)

            
                
            socketio.emit("startgame", { "game_id":game.id})

        return {"round_id":game_list[0].id}, session_for_thread
    start_game({"round_id":game.id}, session_for_thread)
                

            


""" def scheduler():
    broadcast_game_is_running = False
    while True:
        
       
        if not broadcast_game_is_running:
            print('залез')  
           
            broadcast_game_is_running = True  
            check_and_execute()
    """




def create_new_user(username, username1):
    with SessionFactory() as session:   
            with session.begin():
                new_user = User(telegram_id=username, username=username1, deposit_balance=5000, bonus_balance=1000)
                session.add(new_user)
    return new_user

def process_crashed_bets(crashed_bets):
    with SessionFactory() as session:   
            with session.begin():
                for bet in crashed_bets:
                    user = session.query(User).filter(User.id==bet.user_id).first()
                    game = session.query(Crash).filter(Crash.id == bet.round_id).first()
                    settings = session.query(Settings).first()
                    if bet.baltype == 'deposit':
                        settings.profit_money += bet.price
                        game.profit += bet.price
                        user.total_amount_of_money_losed += bet.price
                        user.number_of_loses +=1
    return crashed_bets

session_for_tests= SessionFactory()
def test_pick(current_multiplier, game_id):
    
        try:
                        with session_for_tests.begin():
                            settings = session_for_tests.query(Settings).first()
                            game = session_for_tests.query(Crash).filter(Crash.id == game_id).first()

                            bets_all = session_for_tests.query(CrashBets).filter(CrashBets.round_id == game.id).filter(CrashBets.status == 0).all()
                            if bets_all:
                                random_bet = random.choice(bets_all)
                                if 1 <= random_bet.user_id <= 10:
                                    win = random_bet.price * current_multiplier
                                    print('win', random_bet.price, current_multiplier,  win, win-random_bet.price)
                                    random_bet.won = win - random_bet.price
                                    random_bet.status =2 
                                    random_bet.was_grabbed_at_multiplier = round( current_multiplier, 2)
                                    settings.profit_money -= win - random_bet.price 
                                    game.profit = game.profit - ( win - random_bet.price)
                                    print( win - random_bet.price, game.profit, win, random_bet.price,  'kkk')
                                    user = session_for_tests.query(User).filter(User.id == random_bet.user_id).first()
                                    user.deposit_balance += win
                                    user.total_amount_of_money_won += ( win - random_bet.price)
                                    result = int(random_bet.id)
                                    session_for_tests.commit()
                                    print('pizda', result)
                                    return result
        except Exception as ex:
                    print(ex)
                    'ok'
        finally:
            session_for_tests.commit()


def broadcast_current_game_handler(session):

    
    def wrapper():
        with session.begin():
            #client_sid = request.sid
            game = session.query(Crash).filter(Crash.status == 1).order_by(Crash.id.desc()).first()
    
            if not game:
                return socketio.emit("wait_for_next_game", {})
            multiplier = game.multiplier
            global current_multiplier
            list_of_multipliers = [1]
            while list_of_multipliers[-1] < multiplier:
                list_of_multipliers.append(list_of_multipliers[-1]+0.01)
            for i in range(list_of_multipliers.index(current_multiplier), len(list_of_multipliers)):
                    
                        
                current_multiplier = list_of_multipliers[i]
                


                chance = random.random()
                if chance >= 0.85 and  (1.1<=current_multiplier<=3.5):
                    resp = test_pick(current_multiplier=current_multiplier, game_id=game.id)
                    print(resp, 'list')
                    if resp:
                        socketio.emit('current_game', {'game_id':game.id, "current_multiplier":list_of_multipliers[i], "fake_bet":resp})
                socketio.emit('current_game', {'game_id':game.id, "current_multiplier":list_of_multipliers[i]})
                if 10>current_multiplier > 4:
                    time.sleep(0.01)
                elif current_multiplier >10:
                    time.sleep(0.001)
                else:
                    time.sleep(0.1)
            make_bet_status_equal_to_one(game.id)
                
            all_bets_that_are_crashed = session.query(CrashBets).filter(CrashBets.round_id == game.id).filter(CrashBets.status == 1).all()
            all_bets_that_are_crashed = process_crashed_bets(all_bets_that_are_crashed)
            if  all_bets_that_are_crashed:
                for bet in all_bets_that_are_crashed:
                            
                        
                    user = session.query(User).filter(User.id==bet.user_id).first()

                    attributes_dict = {column.name: getattr(user, column.name) for column in User.__table__.columns if column.name != 'created_at'}
                            
                    socketio.emit("crashed_bet", {"amount": bet.price, "user":attributes_dict, 'baltype':bet.baltype, "game_id" : game.id})
            
            socketio.emit('crash')
                    
                    
            current_multiplier = 1
            if not (game.status == 2):
                        
                game.status = 2


                
            

    
    wrapper()
    connection_pool = engine.pool

# Получите количество активных соединений
    active_connections = connection_pool.checkedout()

    broadcast_game_is_running = False
    
def make_bet_status_equal_to_one(game_id):
    with SessionFactory() as session:
        with session.begin():
       
            
            all_bets_that_are_crashed = session.query(CrashBets).filter(CrashBets.round_id == game_id).filter(CrashBets.status == 0).all()
            for bet in all_bets_that_are_crashed:
                bet.status = 1
                
@socketio.on('get_balance')
def get_balance_handler(data):
    with SessionFactory() as session:
        with session.begin():
            client_sid = request.sid  
            user = session.query(User).filter(User.id==data.user_id).first()
            if user:
                return socketio.emit("users_balance",{"deposit_balance":user.deposit_balance, "referal_balance":user.referal_balance, "bonus_balance":user.bonus_balance}, room=client_sid)
            return socketio.emit("error", {"message":"wrong userid"}, room = client_sid)
def new_bet_create(user_id, round_id, price, status, fake, baltype):
    with SessionFactory() as session:
        with session.begin():
            settings = session.query(Settings).first()
            
            game = session.query(Crash).filter(Crash.id == round_id).first()
      
            new_bet = CrashBets(user_id = user_id, round_id = round_id, price = price,  status = 0, fake = fake, baltype = baltype )
            session.add(new_bet)
    return new_bet

def get_float_handler(round_id):
    with SessionFactory() as session:
        with session.begin():
            last_zero = session.query(Crash).filter(Crash.multiplier==1).order_by(Crash.id.desc()).first()
            bets_in_db = session.query(CrashBets).filter(CrashBets.round_id==round_id).filter(CrashBets.fake==0).all()
            settings = session.query(Settings).first()
            this_game = session.query(Crash).filter(Crash.status == 0).order_by(Crash.id.desc()).first()
            bets_price = 0
            for bet in bets_in_db:
                bets_price += bet.price
            
        
            if settings.profit_money <= 0-(settings.bank_mines*0.2) :
                return 1
            if last_zero:
                if this_game.id - last_zero.id == 1:
                    if random.random() <= 0.2:
                        return 1 

            if (settings.profit_money <=0 and bets_price > 0):
                
                random_float = Decimal(random.uniform(1.0, 2.0)).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
          
                return random_float
            if last_zero:
               
                if (last_zero.id) >= (this_game.id + random.randint(3,10)):
                    
                    return 1
            if not last_zero or (this_game.id-last_zero.id >= random.randint(2,7)):
                
                return 1

            list = []
            for i in range(60):
                list.append(1)
            for i in range(10):
                list.append(2)
            for i in range(5):
                list.append(3)
            for i in range(3):
                list.append(4)
            for i in range(2):
                list.append(5)
            for i in range(1):
                list.append(10)
            list.append(50)
            random.shuffle(list)
            if this_game.multiplier:
                return this_game.multiplier
            m = list[random.randint(0, len(list)-1)]
            if m > 1:
                m = random.randint(1, m)
            if m == 1:
                num =  float(f'{list[0]}.{random.randint(5,99)}')
                return  num
        
            num = float(f'{m}.{random.randint(0,9)}{random.randint(1,9)}')
            return num


multipliers = []
def start_game(data:dict, session_for_thread, fuck_up_next_game=False):####
    with session_for_thread.begin():
        game = session_for_thread.query(Crash).filter(Crash.id == data['round_id']).first()

            
        if game:
            
            print(fuck_up_next_game, 'fuck')
            game.status = 1
            if not fuck_up_next_game:
                game.multiplier =100 #get_float_handler(data['round_id']) 
            else:
                game.multiplier = 1
                fuck_up_next_game = False
            multipliers.append(float(game.multiplier))
        
       
    # Получите количество активных соединений
    return session_for_thread
    broadcast_current_game_handler(session_for_thread)

semaphore = threading.Semaphore(value=1)
def func_for_thread():
    with semaphore:
        while True:
            data, session = check_and_execute()
            global fuck_up_next_game
            if fuck_up_next_game:
                session = start_game(data, session, fuck_up_next_game=True)
                fuck_up_next_game = False
            else:
                session = start_game(data, session)
            
            broadcast_current_game_handler(session)
if __name__ == '__main__':
    
    with SessionFactory() as session:
        with session.begin():
            all_setts = session.query(Settings).all()
            for sett in all_setts:
                session.delete(sett)
            games = session.query(Crash).all()
            settings = Settings(bank_mines=1000)
            session.add(settings)
            usersss = session.query(User).all()
            if usersss:
                for userrr in usersss:
                    session.delete(userrr)
            if games:
                for game in games:
                    session.delete(game)
            bets = session.query(CrashBets).all()
            if bets:
                for bet in bets:
                    session.delete(bet)
    for i in range(10):
        new_user = session.merge( create_new_user(random.randint(100, 999), 'ok'))
    thread1 = threading.Thread(target=func_for_thread)
    thread1.start()
    socketio.run(app, debug=False,allow_unsafe_werkzeug=True, host='0.0.0.0', port=5000)
    
    app.run(debug=True,  port=5000, host='0.0.0.0')

'''
server {
    listen 443 ssl;
    server_name host.yuriyzholtov.com;

    ssl_certificate /home/ubuntu/gambling/host-yuriyzholtov-com-Certificate.crt;
    ssl_certificate_key /home/ubuntu/gambling/host-yuriyzholtov-com-Private-Key.key;

    location / {
        proxy_pass https://51.20.105.5;  # Порт, на котором работает ваше Flask приложение
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

'''

"""
server {
    listen 443 ssl;
    server_name host.yuriyzholtov.com;

    ssl_certificate /home/ubuntu/gambling/combined_cert.pem;
    ssl_certificate_key /home/ubuntu/gambling/host-yuriyzholtov-com-Private-Key.key;

    location / {
        proxy_pass http://127.0.0.1:5000;  # Порт, на котором работает ваше Flask приложение
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
sudo /home/ubuntu/gambling/venv/bin/gunicorn -b 0.0.0.0:5000 -w 4 flask-server:app --certfile=host-yuriyzholtov-com-Certificate.crt --keyfile=host-yuriyzholtov-com-Private-Key.key


"""
