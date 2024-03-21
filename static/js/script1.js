var buttons = document.querySelectorAll('button');

// Перебираем каждую кнопку и добавляем обработчики событий
buttons.forEach(function(button) {
    button.addEventListener('mousedown', function() {
        // При нажатии на кнопку уменьшаем ее размер
        button.style.transform = 'scale(0.9)';
    });

    button.addEventListener('mouseup', function() {
        // При отпускании кнопки возвращаем ее к исходному размеру
        button.style.transform = 'scale(1)';
    });
});
        var notificationContainer = document.querySelector('#notificationContainer');
        var faketable = document.querySelector('.faketable');
        var isAuthorized = false;
        var frog = document.querySelector('#frog');

        console.log(frog)
        var fakeBets;
        var used_childs = [];
       
 
var socket = io.connect(`${window.location.protocol}//${window.location.hostname}:${window.location.port}`);
        var balance = parseFloat(document.querySelector('#depositBalance'))
        var balanceElement = document.querySelector('#depositBalance')
        var gameInProgressElement = document.querySelector('#gameInProgress');
        var make_bet_button = document.querySelector('#make_bet_button');
        var currentMultiplier = 0;
        var currentMultiplierElement = document.querySelector('#currentMultiplier')
        var currentBet;
	 
        var forGame;
		var user_id;
        var currentGame;
		var upcomingGame;
        var selectedBalance = document.querySelector('#selected-balance');
        var selectedBalanceObject = {
            baltype: 'deposit'
            
        }
        var bonusBalanceElement = document.querySelector('#bonusBalance');
        var betAmount = document.querySelector('#betAmount')
        var progressBarOfGame = document.querySelector('#progressBarOfGame')
        var containerForProgress = document.querySelector('#container-for-progress')
        var container_for_btns = document.querySelector('.container-for-btns')
        var colForCoefs = document.querySelector('#col-for-coefs')
        var autoWithdrawal = document.querySelector('#auto-withdrawal');
        var autoWithdrawalCoeff;
        var autoWithdrawalCoeffInput = document.querySelector('#coeff')
    
        socket.on("you_got_new_winning", function(data){
            

            
            var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-success', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent = `Вы выиграли ${data.amount.toFixed(2)} ₽`;
			sky.appendChild(notification);
          
            if (data.baltype == 'deposit'){
			balanceElement.innerHTML = `${(data.user.deposit_balance).toFixed(2)} F`;
            if (selectedBalanceObject.baltype == 'deposit'){
            selectedBalance.innerHTML = balanceElement.innerHTML;}

            }
            else{
                bonusBalanceElement.innerHTML = `${(data.user.bonus_balance).toFixed(2)} F`
                if (selectedBalanceObject.baltype == 'bonus'){
                    selectedBalance.innerHTML = bonusBalanceElement.innerHTML;
                }
            }
            
            make_bet_button.onclick =  makeBet;
            currentBet = null;
		});
        if (gameInProgressElement.getAttribute('value') == "True"){
			gameInProgress = true;

		}
		else {
			gameInProgress = false;
		};
        
        socket.on("prev_bets", function(newData){
            console.log(newData['bets'])
            

        })

        socket.on('connect', function(data) {
		     var WebApp = window.Telegram.WebApp; 
	

        var tgusername = document.querySelector('#ipAdress').value;   
            var ipAdress = document.querySelector('#ipAdress').value; 

	
		
            var xhr = new XMLHttpRequest();

// Указываем метод и URL для запроса
xhr.open("POST", "/authorize", true);

// Устанавливаем заголовок Content-Type для передачи данных в формате JSON
xhr.setRequestHeader("Content-Type", "application/json");

// Определяем функцию, которая будет вызвана при завершении запроса
xhr.onreadystatechange = function () {
  if (xhr.readyState === XMLHttpRequest.DONE) {
    
    var data = JSON.parse(xhr.response);
    
    isAuthorized = true;
            user_id = data.user['id'];
       
            balanceElement.innerHTML =  (data.user.deposit_balance).toFixed(2) + ' F';
            bonusBalanceElement.innerHTML = (data.user.bonus_balance).toFixed(2) + ' F';
            if (selectedBalanceObject.baltype == 'deposit'){
            selectedBalance.innerHTML = (data.user.deposit_balance).toFixed(2) + ' F';	
            
            }
            else{
                selectedBalance.innerHTML = (data.user.bonus_balance).toFixed(2) + ' F';
            }
            
			
  }
};

// Создаем объект с данными для отправки на сервер
var messageData = {
                id: ipAdress,
                tgusername : tgusername
            };


// Преобразуем объект с данными в формат JSON
var jsonData = JSON.stringify(messageData);

// Отправляем запрос на сервер с данными
xhr.send(jsonData);
        
		
	
           

get_bets()
get_previous_xes()
        });

function get_previous_xes(){
    var xhr = new XMLHttpRequest();

// Указываем метод и URL для запроса
xhr.open("GET", "/get_previous_xes", true);

// Устанавливаем заголовок Content-Type для передачи данных в формате JSON
xhr.setRequestHeader("Content-Type", "application/json");

// Определяем функцию, которая будет вызвана при завершении запроса
xhr.onreadystatechange = function () {
  if (xhr.readyState === XMLHttpRequest.DONE) {
    var data = JSON.parse(xhr.response);
    var previous_xes = data.data.reverse()
    previous_xes.forEach(element => {
        if (parseFloat(element) <1.05){

colForCoefs.innerHTML =` <div class="coeff_lose" >
<span>${parseFloat( element)+'x'}</span>
</div>${colForCoefs.innerHTML}`

}
else if (parseFloat(element) >= 2){

colForCoefs.innerHTML = `<div class="coeff_big_win" >
<span>${parseFloat(parseFloat( element)+'x')}</span>
</div>${colForCoefs.innerHTML}`
}
else{

colForCoefs.innerHTML =   `<div class="coeff_win" style="border-radius: 47px;
background-color: #ffffff;  display: flex; justify-content: center; align-items: center; height: 5vh;
border: 3px solid #65a7fb; color: #65a7fb;text-align: center; width: 18%; font-weight: 500; flex: 0 0 20%;">
<span>${parseFloat( element)+'x'}</span>   
</div>${colForCoefs.innerHTML}`
}
    });


  }

}
xhr.send();
}


function get_bets(){

    var xhr = new XMLHttpRequest();

// Указываем метод и URL для запроса
xhr.open("GET", "/get_bets", true);

// Устанавливаем заголовок Content-Type для передачи данных в формате JSON
xhr.setRequestHeader("Content-Type", "application/json");

// Определяем функцию, которая будет вызвана при завершении запроса
xhr.onreadystatechange = function () {
  if (xhr.readyState === XMLHttpRequest.DONE) {
    
    var newData = JSON.parse(xhr.response);

    if (newData['bets']){
             
             newData['bets'].forEach(bet => {

                 if (bet['was_grabbed_at_multiplier']){
             faketable.innerHTML += `<button class="btn  fakeusers" >
                     <img src="${bet['avatar_url']}" class="img-fakeusers"  alt="">
                     <div class="cont-fakeusers" >
                       <span style="font-weight: 300; font-size: 8px; ">${bet['username']}</span><br>
                       <span style="font-weight: 400; font-size: 12px; ">${bet['price']} F</span>
                     </div>
                     <div  class="btn btn-primary coeff bet${bet['id']}" >${bet['was_grabbed_at_multiplier']}x</div>
                   </button>`
                 }
                 else{
                     faketable.innerHTML += `<button class="btn  fakeusers" >
                     <img src="${bet['avatar_url']}"  class="img-fakeusers"  alt="">
                     <div class="cont-fakeusers">
                       <span style="font-weight: 300; font-size: 8px; ">${bet['username']}</span><br>
                       <span style="font-weight: 400; font-size: 12px; ">${bet['price']} F</span>
                     </div>
                     <div  class="btn btn-primary coeff bet${bet['id']}"></div>
                   </button>`
                 }

             });
     }
			
  }
};

// Создаем объект с данными для отправки на сервер

// Отправляем запрос на сервер с данными
xhr.send();
        

}

        socket.on('previous_xes', function (data){
            var previous_xes = data.data
            previous_xes.forEach(element => {
                if (parseFloat(element) <1.05){

colForCoefs.innerHTML =` <div class="coeff_lose" >
<span>${parseFloat( element)+'x'}</span>
</div>${colForCoefs.innerHTML}`

}
else if (parseFloat(element) >= 2){

colForCoefs.innerHTML = `<div class="coeff_big_win" >
<span>${parseFloat(parseFloat( element)+'x')}</span>
</div>${colForCoefs.innerHTML}`
}
else{

colForCoefs.innerHTML =   `<div class="coeff_win" style="border-radius: 47px;
background-color: #ffffff;  display: flex; justify-content: center; align-items: center; height: 5vh;
border: 3px solid #65a7fb; color: #65a7fb;text-align: center; width: 18%; font-weight: 500; flex: 0 0 20%;">
<span>${parseFloat( element)+'x'}</span>   
</div>${colForCoefs.innerHTML}`
}
            });
        })

        socket.on('error', function(data){
           
			var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-error', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent = `${data.message}`;
			sky.appendChild(notification);

		});
        
        socket.on('not_enough_funds_on_the_balance', function(data){
           currentBet = null;
           var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-warning', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent = `${data.message}`;
			sky.appendChild(notification);


       });
        socket.on('successful_authorizing', function(data){
            isAuthorized = true;
            user_id = data.user.id;
            balanceElement.innerHTML =  (data.user.deposit_balance).toFixed(2) + ' F';
            bonusBalanceElement.innerHTML = (data.user.bonus_balance).toFixed(2) + ' F';
            if (selectedBalanceObject.baltype == 'deposit'){
            selectedBalance.innerHTML = (data.user.deposit_balance).toFixed(2) + ' F';	
            
            }
            else{
                selectedBalance.innerHTML = (data.user.bonus_balance).toFixed(2) + ' F';
            }
            
			if (data.payments){
				data_for_args = {confirmation_token : data.payments.confirmation_token}
				generate_widget_for_payment(data_for_args)
			}
        });

        function pickUpWInning(){
            autoWithdrawalCoeff = null;
			if (!isAuthorized){
                var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-error', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent = `Вы не зарегистрированы`;
			 return sky.appendChild(notification);

            }
			if (!currentMultiplier){
                var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-blue', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent = `Дождитесь начала игры`;
			return sky.appendChild(notification);

			}
            if (currentBet){

            
			socket.emit("pickupwinning", {bet : currentBet.id})
            currentBet = null;
            }}

socket.on("crashed_bet", function(data){
    try{
            if (currentBet.round_id == currentGame){
                if (data.user.id == user_id){
                	var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-error', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent = `Вы проиграли ${data.amount} F`
			sky.appendChild(notification);

            
				balanceElement.innerHTML =( data.user.deposit_balance).toFixed(2) + ' F'
                bonusBalanceElement.innerHTML = data.user.bonus_balance.toFixed(2) +' F'
            }
                if (selectedBalanceObject.baltype == 'deposit'){
                selectedBalance.innerHTML = balanceElement.innerHTML;}
                else{
                    selectedBalance.innerHTML = bonusBalanceElement.innerHTML;
                }
                currentBet = null;
			}}catch (error){}


})
            
        socket.on("crash", function(data){
            isSliding = false;
            isSlidingFast = false;
		isSlidingVeryFast = false;
        
            make_bet_button.style.background = 'linear-gradient(180deg, #cf090f 0%, #fd4b27 100%, #fd4b27 100%)';
            make_bet_button.style.border = '2px solid #cde2f2';
	autoWithdrawalCoeff = null;
            used_childs = [];
            faketable.innerHTML = '';
            frog.classList.remove('fly-from-button')
            if (( 'fast-fly-from-button' in frog.classList)){
                frog.classList.remove('fast-fly-from-button');
            }
            frog.classList.add('fly-top-right');

            slidingLeft()
            var childs = colForCoefs.querySelectorAll('.coeff_lose, .coeff_big_win,  .coeff_win');
            if (childs.length >= 20){
                childs[childs.length-1].remove()
            }
            
            if (parseFloat(currentMultiplier) <1.05){

                colForCoefs.innerHTML =` <div class="coeff_lose" >
                <span>${currentMultiplier}</span>
            </div>${colForCoefs.innerHTML}`
            
            }
            else if (parseFloat(currentMultiplier) >= 2){
   
                colForCoefs.innerHTML = `<div class="coeff_big_win" >
                <span>${currentMultiplier}</span>
            </div>${colForCoefs.innerHTML}`
            }
            else{
          
                colForCoefs.innerHTML =   `<div class="coeff_win" >
                <span>${currentMultiplier}</span>   
            </div>${colForCoefs.innerHTML}`
            }
            /* try{
            if (currentBet.round_id == currentGame){
                if (data.user.id == user_id){
                	var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-error', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent = `Вы проиграли ${data.amount} F`
			sky.appendChild(notification);

            
				balanceElement.innerHTML =( data.user.deposit_balance).toFixed(2) + ' F'
                bonusBalanceElement.innerHTML = data.user.bonus_balance.toFixed(2) +' F'
            }
                if (selectedBalanceObject.baltype == 'deposit'){
                selectedBalance.innerHTML = balanceElement.innerHTML;}
                else{
                    selectedBalance.innerHTML = bonusBalanceElement.innerHTML;
                }
                currentBet = null;
			}}catch (error){} */
                
		})
        function topUpBalanceClicked(){
			amount_in_rub = parseFloat(prompt('Укажите сумму на которую вы хотите пополнить баланс'))

			socket.emit("topUpBalance", {user_id : user_id, amount : amount_in_rub})

		}
       /*  function generate_widget_for_payment(data){
			var confirmation_token = data.confirmation_token

			var parentElement = document.getElementById("parent-container");
			// Удаляем переменную checkout, если она существует


			var scriptElement = document.createElement("script");
			var scriptElement2 = document.createElement("script");

		

// Создаем текст скрипта

// Устанавливаем атрибут src для этого элемента
			scriptElement.src = "https://yookassa.ru/checkout-widget/v1/checkout-widget.js";

// Устанавливаем id для этого элемента
			
	
			//container_for_payment.appendChild(scriptElement);
			var scriptText = `
			if (window.checkout) {
				delete window.checkout;;
}
// Инициализация виджета. Все параметры обязательные.
const checkout = new window.YooMoneyCheckoutWidget({
    confirmation_token: '${confirmation_token}', //Токен, который перед проведением оплаты нужно получить от ЮKassa
    return_url: 'https://example.com/', //Ссылка на страницу завершения оплаты, это может быть любая ваша страница
    customization: {
        //Настройка способа отображения
        modal: true
    },
	error_callback: function(error) {
        console.log(error);
    }
});

// Отображение платежной формы в контейнере
checkout.render('payment-form');
`;

// Устанавливаем содержимое скрипта
			scriptElement2.innerHTML = scriptText;
			parentElement.appendChild(scriptElement)
			parentElement.appendChild(scriptElement2)

			


		} */

		socket.on("generate_widget_for_payment", function(data) {
    
            var overlay = document.createElement("div");
overlay.classList.add("overlay");
overlay.id = "overlay";
var widgetContainer = document.createElement("div");
widgetContainer.classList.add("widgetContainer");
widgetContainer.onclick = function(event) {
    event.stopPropagation();
};
            var closeButton = document.createElement("button");
closeButton.classList.add("close-btn");
closeButton.textContent = "✖";
closeButton.onclick = closeWidget;

// Создаем iframe
var iframe = document.createElement("iframe");
iframe.src = data['url'];
iframe.height = "100%";
iframe.width = "100%";

// Добавляем кнопку закрытия в контейнер
widgetContainer.appendChild(closeButton);

// Добавляем iframe в контейнер
widgetContainer.appendChild(iframe);

// Добавляем контейнер в overlay
overlay.appendChild(widgetContainer);

// Добавляем overlay в body
document.body.appendChild(overlay);
console.log(overlay)
});

function maxPossibleBet(){
   
    
    if (selectedBalanceObject.baltype == 'bonus'){
        betAmount.value = parseFloat(bonusBalanceElement.innerHTML);
                }
                else{
    betAmount.value = parseFloat(balanceElement.innerHTML);}
}

function makeBet(){

            if (!isAuthorized){
                var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-error', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent = "Вы не зареганы!"
			return sky.appendChild(notification);

              
            }
	
			if (gameInProgress){
                var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-warning', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent = "Вы не можете ставить ставки во время игры!"
			return sky.appendChild(notification);

				
			}
			if (!betAmount.value){
                var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-blue', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent = "Введите сумму ставки"
			return sky.appendChild(notification);

				
			}
			if (!gameInProgress && isAuthorized && forGame){
				if (currentBet){
                    var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-error', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent ="Вы уже поставили ставку в этой игре!"
			return sky.appendChild(notification);

				
					
				}
             
				
                if (autoWithdrawal.checked){
                    if (autoWithdrawalCoeffInput.value){
                        if ((parseFloat(autoWithdrawalCoeffInput.value) < 1.1)){
                           
                            var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-warning', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent ="Минимальный коеффициент для автовывода - 1.1"
			return sky.appendChild(notification);

                        }
                        autoWithdrawalCoeff = parseFloat( autoWithdrawalCoeffInput.value) 
                

                    }
                    else{   
                        var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-warning', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent ="Введите коэффициент для вывода!"
			return sky.appendChild(notification);
                    }
                }
     
				socket.emit("new_bet", {"user_id":user_id, game_id:forGame,  bet_in_usd:parseFloat(betAmount.value), baltype:selectedBalanceObject.baltype})
			}
        
		};
        socket.on("successful_bet",function(data){
			currentBet = data;
            var notification = document.createElement('div');
            notification.classList.add('alert', 'notification-blue', 'notification');
            notification.setAttribute('role', 'alert'); 
            notification.textContent ="Вы успешно поставили ставку";
console.log('stavka')
			sky.appendChild(notification);
            console.log(notification)
            if (data.baltype == 'deposit'){
			balanceElement.innerHTML = `${(parseFloat(balanceElement.innerHTML) - data.price).toFixed(2)} F` ;
                if (selectedBalanceObject.baltype == 'deposit'){
            selectedBalance.innerHTML = balanceElement.innerHTML;}}
            else {
                
                bonusBalanceElement.innerHTML = `${(parseFloat(bonusBalanceElement.innerHTML)-data.price).toFixed(2)} F`;
                if (selectedBalanceObject.baltype == 'bonus'){
                    

                    selectedBalance.innerHTML = bonusBalanceElement.innerHTML;
      
                }
            }

            
            make_bet_button.style.background = '#99c5ff';
            make_bet_button.style.border = '2px solid #6cabfb';
            make_bet_button.innerHTML =  '<span style="font-weight: 700; font-size: 26px;">...</span>';
		});
var isSlidingVeryFast = false;
        socket.on("current_game", function(newData) {
			/* for (k=0; k<=300; k++){
				сhart.data.labels.push(numbers[k])
				chart.data.datasets[0].data.push(values[k])
			} */
            currentMultiplierElement.innerHTML = newData.current_multiplier.toFixed(2)+'x';
			currentMultiplier = newData.current_multiplier.toFixed(2)+'x';
            if (newData['fake_bet'])
            {
                try{
                var id_of_bet = (newData['fake_bet']);
                var fake_bet =document.querySelector(`.bet${id_of_bet}`);
                fake_bet.innerHTML=currentMultiplier;
		}
	    	catch(error){}
	    }
          
            if (newData.current_multiplier.toFixed(2) < 2 && !isSliding){
            isSliding = true;
            slidingLeftBottom()
            if (frog.classList != ['fly-from-button']){
		frog.classList.add('fly-from-button');
	    }
            }

            else if (newData.current_multiplier.toFixed(2) > 10 && !isSlidingVeryFast) {
                isSlidingVeryFast = true;
                slidingVeryFastLeftBottom()
                if (!( 'fast-fly-from-button' in frog.classList)){
                frog.classList.add('fast-fly-from-button');
            }
            }

            else if (( newData.current_multiplier.toFixed(2) > 2 )&& (!isSlidingFast)){
                
                isSlidingFast = true;
                
            slidingFastLeftBottom()

            if (!( 'fast-fly-from-button' in frog.classList)){

frog.classList.remove('fly-from-button');

frog.classList.add('fast-fly-from-button');
            }
            }
            

	   
            gameInProgress = true;
            containerForProgress.style.display = 'none'
            if (!currentBet){
                make_bet_button.innerHTML =  '<span style="font-weight: 700; font-size: 26px;">...</span>';
           
            }
            
			if (newData.fake_bets){
			
				for (const key in newData.fake_bets){
            
					var userName_and_avatar = newData.fake_bets[key]
                    for (const userName in userName_and_avatar){
						faketable.innerHTML += `<button class="btn  fakeusers" style=" align-items: center; background-color: rgba(255, 255, 255, 0.1); border: none; font-family: 'Roboto'; border-radius: 47px; color: white; text-align: center;">
                            <img src="${userName_and_avatar[userName]}" style="width: 25px; margin-right: 10px; border-radius:30px" alt="">
                            <div style="text-align: left;overflow: auto;  -webkit-overflow-scrolling: touch;">
                              <span style="font-weight: 300; font-size: 8px; ">${userName}</span><br>
                              <span style="font-weight: 400; font-size: 12px; ">${key} F</span>
                            </div>
                          </button>`
                    }}
				
			}
            
            
            if (currentBet && autoWithdrawalCoeff){
            
                
             
                
                if (parseFloat(currentMultiplier) > parseFloat(autoWithdrawalCoeff).toFixed(2))
           
                    pickUpWInning()
            }
           
            

        });
        socket.on("time_remaining", function (data){
		make_bet_button.onclick = makeBet;
        
        if ( 'fast-fly-from-button' in frog.classList){
                frog.classList.remove('fast-fly-from-button');
            }
            if (frog.classList != ['fly-top-right']){
		    frog.classList.add('fly-top-right');
	    }
            if (!currentBet){
                make_bet_button.style.background = 'linear-gradient(180deg, #cf090f 0%, #fd4b27 100%, #fd4b27 100%)';
            make_bet_button.style.border = '2px solid #cde2f2';
            make_bet_button.innerHTML =  '<span style=" font-weight: 700; font-size: 26px;">СТАВКА</span>';
            }
            make_bet_button.onclick = makeBet;
			gameInProgress = false;
			var secondsToUpcomingGame = data.seconds;
			forGame = data.for_game;

            
            progressBarOfGame.style.width = `${data.seconds_remained*1.667}%`;
            containerForProgress.style.display = 'flex'
        
            currentMultiplierElement.innerHTML = '';
            if (data.fake_bets){
                data = data.fake_bets

data.forEach(bet => {

    for (const username in bet){
        
        var avatarUrl = bet[username]['avatar_url']
     
        var randomNumber = bet[username]['price'];
        console.log(faketable)
        faketable.innerHTML += `<button class="btn  fakeusers" >
                     <img src="${bet[username]['avatar_url']}"  class="img-fakeusers"  alt="">
                     <div class="cont-fakeusers" >
                       <span style="font-weight: 300; font-size: 8px; ">${bet[username]['username']}</span><br>
                       <span style="font-weight: 400; font-size: 12px; ">${bet[username]['price']} F</span>
                     </div>
                     <div  class="btn btn-primary coeff bet${bet[username]['id']}"></div>
                   </button>`
    }
});
            }
		});
        socket.on("startgame", function(data){
            frog.classList.remove('fly-top-right');
            frog.classList.remove('fast-fly-from-button');
            frog.classList.add('fly-from-button')
        
    
            if (currentBet){
              
            make_bet_button.onclick = pickUpWInning
            make_bet_button.innerHTML =  '<span style="b font-weight: 700;  font-size: 26px;">ЗАБРАТЬ</span>';
            
          
        }
            else{
                make_bet_button.innerHTML =  '<span style=" font-weight: 700; font-size: 26px;">...</span>';
           
            }

            containerForProgress.style.display = 'none'
    currentMultiplierElement.innerHTML = '';
    currentMultiplier = 0;
    currentGame = data.game_id;
    gameInProgress = true;
    if (currentBet){

        if (currentBet.round_id !=currentGame){
        currentBet = null
    }
    }
    
 
   

});

socket.on('fake_bets', function(newData){
    



})

function toggleMenu(){
        var closeBtn = document.querySelector('.closeBtn');
        var closeBtnText = document.querySelector('#closeBtnText');
        closeBtn.classList.toggle('closeBtnCollapse')
        faketable.classList.toggle('collapsed')
        faketable.classList.toggle('faketable')
        
        if  (closeBtnText.classList == 'fas fa-arrow-right'){
      
        
            closeBtn.innerHTML = '<i class="fas fa-arrow-left" id="closeBtnText"></i> Закрыть';
            
        }
        else{
            closeBtn.innerHTML = '<i class="fas fa-arrow-right" id="closeBtnText"></i>';
        }
       
    }
    var dropdownBtn = document.querySelector('#dropdownBtn');
function depositBalanceIsMain(){
    selectedBalanceObject.baltype ='deposit'
    selectedBalance.innerHTML = balanceElement.innerHTML;
    
}
function bonusBalanceIsMain(){
   
    selectedBalanceObject.baltype = 'bonus'
    selectedBalance.innerHTML = bonusBalanceElement.innerHTML;
}
function hideNotifications(){
    var notifications = document.querySelectorAll('.notification');

// Добавляем слушатель событий для клика к каждому элементу
notifications.forEach(function(notification) {
    notification.addEventListener('click', function() {
        this.style.display = 'none'; // Скрыть элемент при клике
    });
});
}
setInterval(hideNotifications, 1000);

function terminateNotifications(){
    // Находим все элементы с классом notification
var notifications = document.querySelectorAll('.notification');

// Проходимся по каждому элементу
notifications.forEach(function(notification) {
    notification.style.opacity = 0;
    notification.addEventListener('transitionend', function(){
        notification.remove();

    }) // Через 2 секунды (2000 миллисекунд)
});

}
setInterval(terminateNotifications, 1000)
var inputs = document.querySelectorAll("input");

  // Для каждого инпута добавляем обработчик события keypress
  inputs.forEach(function(input) {
    input.addEventListener("keypress", function(event) {
      if (event.key === "Enter") {
        input.blur();
      }
    });
  });
	    
