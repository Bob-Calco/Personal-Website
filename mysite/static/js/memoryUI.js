var time;
var totalTime = 0;
var turns = 0
var started = false;

function pageLoad(){
    document.getElementById('id_name').disabled = true;
    document.getElementById('id_time').disabled = true;
    document.getElementById('id_turns').disabled = true;
}

function moveCardsUI(card1, card2){
    fadeOut(card1, 50);
    fadeOut(card2, 50);
}

function fadeOut(element, time){
    var opacity = 1;
    var timer = setInterval(function(){
        if(opacity <= 0.1){
            clearInterval(timer);
            element.className += ' invisible';
        }
        element.style.opacity = opacity;
        opacity -= 0.1;
    }, time)
}

function victory(){
  // STOP THE TIME!
  stopTime()

  // Now show the submit form for the highscores
  document.getElementById('id_name').disabled = false;
  document.getElementById('id_time').disabled = false;
  document.getElementById('id_time').readOnly = true;
  document.getElementById('id_time').value = totalTime.toFixed(1);
  document.getElementById('id_turns').disabled = false;
  document.getElementById('id_turns').readOnly = true;
  document.getElementById('id_turns').value = turns;
  document.getElementById('formpje').className = 'submit-form';
  document.getElementById('please_submit').textContent = "Good job! your score is: " + (100-(totalTime - 10)-(2*(turns-10))).toFixed(1)
  document.getElementById('please_submit').className = '';

  // Make the gameboard dissappear by setting the height of all canvas' to 0, and then set display: none;
  var height = document.getElementById(0).clientHeight;
  a = document.getElementsByTagName('canvas')
  var i;
  var timer = setInterval(function(){
      if(height <= 1){
          clearInterval(timer);
          for(i=0; i < a.length; i++){
            a[i].className = 'hidden';
          }
      }
      for(i=0; i < a.length; i++){
        a[i].style.height = height.toString().concat('px');
      }
      height -= 1;
  }, 10);
}

function start(){
  if(started === false){
    // Hide the form
    document.getElementById('id_name').disabled = true;
    document.getElementById('id_time').disabled = true;
    document.getElementById('id_turns').disabled = true;
    document.getElementById('formpje').className = 'submit-form hidden';
    document.getElementById('please_submit').className = 'hidden';

    // Clear the data
    totalTime = 0;
    turns = 0;
    document.getElementById('time').textContent = totalTime;
    document.getElementById('turns').textContent = turns;

    // Show gameboard again
    a = document.getElementsByTagName('canvas')
    var i;
        // Show canvas again
    for(i=0; i < a.length; i++){
            a[i].className = '';
            a[i].style.opacity = 1;
          }
        // Grow the canvas to the correct height
    var finalHeight = document.getElementById(0).clientWidth;
    var height = 0;
    var timer = setInterval(function(){
        if(height >= finalHeight){
            clearInterval(timer);
        }
        for(i=0; i < a.length; i++){
            a[i].style.height = height.toString().concat('px');
        }
        height += 1;
    }, 10)

    // count down
    document.getElementById('countdown').className = 'countdown-container'

    document.getElementById('three').className = 'countdown';
    fadeOut(document.getElementById('three'), 100);

    window.setTimeout(function(){
        document.getElementById('two').className = 'countdown';
        fadeOut(document.getElementById('two'), 100);
    },900)

    window.setTimeout(function(){
        document.getElementById('one').className = 'countdown';
        fadeOut(document.getElementById('one'), 100);
    },1800)

     // start the time after the countdown finished
    window.setTimeout(function(){
        document.getElementById('countdown').className += 'hidden'
        time = setInterval(setTime, 100);
        started = true;
    }, 2700)
  }
}

function setTime(){
  totalTime += 0.1;
  document.getElementById('time').textContent = totalTime.toFixed(1);
}

function setTurns(){
    turns += 1;
    document.getElementById('turns').textContent = turns;
}

function stopTime(){
  if(started === true){
    clearInterval(time);
    started = false;
  }
}