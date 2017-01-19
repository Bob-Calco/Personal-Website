var cards_order = ["circle", "diamond", "heart", "house", "lightning", "parallellogram", "pentagon", "square", "star", "triangle","circle", "diamond", "heart", "house", "lightning", "parallellogram", "pentagon", "square", "star", "triangle"]
var cards_correct = [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false];
var card_1 = -1;
var card_2 = -1;
var waitingFlip = false;
var waitingMove = false;

function setup(){
    cards_correct = [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false];
    cards_order = shuffleArray(cards_order);
    for(var i = 0; i < 20; i ++){
      clearCanvas(i);
    }
    start();
}

function stop(){
  stopTime();
}

function cardClick(id){
  // check if cards are still waiting to be flipped back
  if(waitingFlip === true){
    flipCardsBack();
  }
  // check if cards are still waiting to be moved
  if(waitingMove === true){
      moveCards()
  }
  // check if we've begun playing.
  if(started === false){
    return;
  }
  // check if user clicked a card that is already correct
  else if(cards_correct[id] === true){
    return;
  }
  // check if user clicked the card that was already flipped
  else if(card_1 === id){
    return;
  }
  // check if this is the first card of the two
  else if(card_1 === -1) {
    drawShape(cards_order[id], id);
    card_1 = id;
  }
  // otherwise it is the second and we need to also check if there is a match
  else{
    drawShape(cards_order[id], id);
    card_2 = id;
    checkIfMatch();
  }
}

function checkIfMatch(){
  // add one to the turns counter
  setTurns();
  // are the two cards a match?
  if(cards_order[card_1] === cards_order[card_2]){
    cards_correct[card_1] = true;
    cards_correct[card_2] = true;
    waitingMove = true;
    window.setTimeout(moveCards, 1000);

    // check if victory is achieved
    for(card in cards_correct){
      if(cards_correct[card] === false){
        return;
      }
    }
    // for loop hasn't found any wrong cards
    victory();
  }

  // wait for 1.5 seconds and then flip the cards over.
  else{
    waitingFlip = true;
    window.setTimeout(flipCardsBack, 1500);
  }
}

// Flips the two cards that are turned back.
function flipCardsBack(){
  if(waitingFlip === true){
    clearCanvas(card_1);
    clearCanvas(card_2);
    card_1 = -1;
    card_2 = -1;
    waitingFlip = false;
  }
}

function moveCards(){
    if(waitingMove === true){
        card1 = document.getElementById(card_1);
        card2 = document.getElementById(card_2);
        moveCardsUI(card1, card2);
        card_1 = -1;
        card_2 = -1;
        waitingMove = false;
    }
}

// Durstenfeld shuffle
function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}
