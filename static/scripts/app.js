const $form = $('form')
let score = 0
let endGame = false
let guesses=[]

$form.on('submit',function(e){
    e.preventDefault();
    if(endGame){
        message('The game has ended!')
        return
    }
    
    let guess =$('#guess').val();
    submitGuess(guess);
})

//sends axios request to /guess, the server then checks that value against all english words and words on the board and returns according information
async function submitGuess(guess){
    axios.post('/guess',{guess}).then(function(response){
        handleResponse(response,guess)
    })
}
//handles the response information and parses out a message
function handleResponse(response, guess){
    const messages = {
        'not-word':'That is not a real word!',
    'ok': 'Nice guess!',
    'not-on-board':'That word is not on the board!',
    'empty': 'Type a word first!'
    }
    const result = response.data.result;
    message(messages[result]);
    if(result === 'ok'){
        updateScore(guess);
    }
}
//changes the message displaying below the board
function message(mes){
    $('#message').text(mes);

}
function updateScore(word){
    if(guesses.includes(word)){
        message('You already guessed that!')
        return
    }
    guesses.push(word)
    score += word.length;
    $('#score').text(score);
}
function timerUpdate(){
    let timer= $('#timer')
    if(timer.text() == 0){
        clearInterval(timerInterval);
        endTheGame()
        message('Time is up!')
    }
    else timer.text(Number(timer.text())-1)
}
let timerInterval = setInterval(timerUpdate,1000)

async function endTheGame(){
    endGame=true
    score = $("#score").text()
    axios.post('/game/data',{score}).then(function(result){
        console.log(result)
    })

}