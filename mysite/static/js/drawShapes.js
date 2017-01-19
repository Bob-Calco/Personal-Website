/* This file has all the draw functions to make shapes.
 * All the functions draw starting from the top against the clock
 */

function clearCanvas(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.font = "20px sans-serif";
  ctx.fillText("Memory", 15, 55);
}

function drawShape(shape, id){
  clearCanvas(id);
  switch(shape){
    case 'circle':
      drawCircle(id);
      break;
    case 'diamond':
      drawDiamond(id);
      break;
    case 'heart':
      drawHeart(id);
      break;
    case 'house':
      drawHouse(id);
      break;
    case 'lightning':
      drawLightning(id);
      break;
    case 'parallellogram':
      drawParallellogram(id);
      break;
    case 'pentagon':
      drawPentagon(id);
      break;
    case 'square':
      drawSquare(id);
      break;
    case 'star':
      drawStar(id);
      break;
    case 'triangle':
      drawTriangle(id);
      break;
  }
}

function drawCircle(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.beginPath();
  ctx.arc(50,50,30,0,2*Math.PI);
  ctx.fill();
  ctx.stroke();
}

function drawDiamond(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.beginPath();
  ctx.moveTo(50,15);
  ctx.lineTo(25,50);
  ctx.lineTo(50,85);
  ctx.lineTo(75,50);
  ctx.fill();
  ctx.stroke();
}

function drawHeart(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.beginPath();
  ctx.arc(35,40,20,0,2*Math.PI);
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(65,40,20,0,2*Math.PI);
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(18,50);
  ctx.lineTo(50,90);
  ctx.lineTo(82,50);
  ctx.fill();
  ctx.stroke();
}

function drawHouse(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.beginPath();
  ctx.moveTo(50,15);
  ctx.lineTo(20,45);
  ctx.lineTo(20,80);
  ctx.lineTo(80,80);
  ctx.lineTo(80,45);
  ctx.fill();
  ctx.stroke();
}

function drawLightning(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.beginPath();
  ctx.moveTo(50,10);
  ctx.lineTo(20,20);
  ctx.lineTo(40,45);
  ctx.lineTo(30,50);
  ctx.lineTo(80,90);
  ctx.lineTo(60,50);
  ctx.lineTo(70,45);
  ctx.fill();
  ctx.stroke();
}

function drawParallellogram(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.beginPath();
  ctx.moveTo(45,20);
  ctx.lineTo(15,80);
  ctx.lineTo(55,80);
  ctx.lineTo(85,20);
  ctx.fill();
  ctx.stroke();
}

function drawPentagon(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.beginPath();
  ctx.moveTo(50,15);
  ctx.lineTo(15,40);
  ctx.lineTo(30,80);
  ctx.lineTo(70,80);
  ctx.lineTo(85,40);
  ctx.fill();
  ctx.stroke();
}

function drawSquare(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.fillRect(20,20,60,60);
}

function drawStar(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.beginPath();
  ctx.moveTo(50,15);
  ctx.lineTo(40,40);
  ctx.lineTo(15,40);
  ctx.lineTo(35,55);
  ctx.lineTo(30,80);
  ctx.lineTo(50,65);
  ctx.lineTo(70,80);
  ctx.lineTo(65,55);
  ctx.lineTo(85,40);
  ctx.lineTo(60,40);
  ctx.fill();
  ctx.stroke();
}

function drawTriangle(id){
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.beginPath();
  ctx.moveTo(50,20);
  ctx.lineTo(20,80);
  ctx.lineTo(80,80);
  ctx.fill();
  ctx.stroke();
}
