


    
    

            

    

   

function slidingLeft(){
    var styleSheet = document.styleSheets[0];
    document.querySelectorAll('.big-cloud, .small-cloud').forEach(function(element) {
      // Получаем текущее значение left и устанавливаем его как начальное значение анимации
      
      var random_number = Math.floor(Math.random() * 3) + 4;
      element.style.animation = `slideLeft ${random_number}s linear infinite`;
      
    });}
    var sky = document.querySelector('.sky');
var isSliding = false
function slidingLeftBottom(){
var styleSheet = document.styleSheets[0];
    document.querySelectorAll('.big-cloud, .small-cloud').forEach(function(element) {
      // Получаем текущее значение left и устанавливаем его как начальное значение анимации
      
      var random_number = Math.random() * (4 - 2) + 2;
      element.style.animation = `slideLeftBottom ${random_number}s linear infinite`;
   
    });
}

var isSlidingFast = false;
function slidingFastLeftBottom(){
var styleSheet = document.styleSheets[0];
    document.querySelectorAll('.big-cloud, .small-cloud').forEach(function(element) {
      // Получаем текущее значение left и устанавливаем его как начальное значение анимации
      
      var random_number = Math.random() + 1;
      element.style.animation = `slideLeftBottom ${random_number}s linear infinite`;
   
    });
}

function slidingVeryFastLeftBottom(){
var styleSheet = document.styleSheets[0];
    document.querySelectorAll('.big-cloud, .small-cloud').forEach(function(element) {
      // Получаем текущее значение left и устанавливаем его как начальное значение анимации
      

      element.style.animation = `slideLeftBottom 0.5s linear infinite`;
   
    });
}

slidingLeft()

// Получаем ссылки на облака
var bigCloud = document.querySelector('.big-cloud');
var smallClouds = document.querySelectorAll('.small-cloud');

// Функция для перемещения облаков
function moveClouds() {

// Получаем текущую позицию облаков
var bigCloudLeft = parseInt(bigCloud.offsetLeft);
var smallCloudsLeft = Array.from(smallClouds).map(function(cloud) {
    return parseInt(cloud.style.left);
});


if (bigCloudLeft < -bigCloud.offsetWidth) {
    bigCloud.style.left = '110%';
  
}

smallClouds.forEach(function(smallCloud){
    var smallCloudLeft = smallCloud.offsetLeft;
    if (smallCloudLeft < -smallCloud.offsetWidth){
        let min = 10;
let max = 40;
let randomNumberInRange = Math.random() * (max - min + 1) + min;

        smallCloud.style.left = `1${randomNumberInRange}%`;
    } 

})
}

// Вызываем функцию для перемещения облаков каждые 10 миллисекунд
setInterval(moveClouds, 1000);