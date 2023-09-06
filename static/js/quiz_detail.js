const url = window.location.href;
const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')
var timer = null

const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    timer = setInterval(()=>{
        seconds --
        if (seconds < 0) {
            seconds = 59
            minutes --
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0'+minutes
        } else {
            displayMinutes = minutes
        }
        if(seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b id='inner-time'>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time over')
                sendData()
            }, 500)
        }

        timerBox.innerHTML = `<b id='inner-time'>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}

const updateInterval = setInterval(()=>{
    const inner = document.getElementById('inner-time').innerHTML;
    const elements = [...document.getElementsByClassName('ans')];
    const data = {};
    const arr = [];

    elements.forEach(el=>{
        obj = {}
        if (el.checked || (el.type === 'textarea' && el.value != '')) {
            obj[el.name] = el.value
            arr.push(obj)
        } else {
            if (el.type === 'checkbox' && !obj[el.name]) {
                obj[el.name] = null
                arr.push(obj)
            }
        }
    })

    data["answers"] = JSON.stringify(arr);
    data["time"] = toSeconds(inner);

    $.ajax({
            type:'POST',
            url: `${url}draft/upload/`,
            dataType:'json',
            data:data,
            success: function(res){
            //    console.log(res)
            },
            error: function(error){
                console.log(error)
            }
        })
}, 30000)

function paginate(array, page_size, page_number) {
  // human-readable page numbers usually start with 1, so we reduce 1 in the first argument
  return array.slice((page_number - 1) * page_size, page_number * page_size);
}

function toSeconds(str) {
    var pieces = str.split(":");
    var result = Number(pieces[0]) * 60 + Number(pieces[1]);
    return(result.toFixed(3));
}

$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response){
        const status = response.status;
        const quiz = response.quiz;

        if(status == 202){
            const data = response.data
            data.forEach((el, index) => {
                for (const [question, answers] of Object.entries(el)){
                    quizBox.innerHTML += `
                    ${index==0 ? "": '<div class="divider mt10 mb20"></div>'}
                        <div class="mb10 mt10">
                            <b>${question}</b>
                        </div>
                    `;
                    answers.forEach(answer=>{
                        const id = (typeof answer['id'] !== null) ? answer['id'] : index;
                        const ans = answer['text'];
                        const selected = answer['selected'];
                        const non_structured =  answer['non_structured'];

                        if(!non_structured){
                            var input = document.createElement("input");
                            input.type = "radio"
                            input.classList.add(...["ans", "with-gap"])
                            input.setAttribute('id', `${question}-${ans}`)
                            input.setAttribute('name', `${question}`)
                            input.setAttribute('value', `${ans}`)
                            input.setAttribute('onclick', "getSelected(this)")

                            if(selected == true) input.setAttribute("checked", "")
                            var radioDiv = document.createElement("div");
                            radioDiv.classList.add("radio")
                            var label = document.createElement("label")
                            var span = document.createElement("span")
                            span.innerHTML = `${ans}`
                            label.append(input)
                            label.append(span)
                            radioDiv.append(label)

                            quizBox.append(radioDiv)
                        }else{
                            var textarea = `<div class="row">
                                <div class="input-field col s12 text-section">
                                  <textarea name="${question}" id="${question}-${id}" class="ans non-structured materialize-textarea"></textarea>
                                </div>
                              </div>`;
                              quizBox.innerHTML += textarea
                        }
                    })
                }
            });
            activateTimer(response.time)
        }
    },
    error: function(error){
        console.log(error)
    }
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

function getSelected(e){
    const inner = document.getElementById('inner-time').innerHTML;
    if(e.checked){
        const time = toSeconds(inner);
        const result = {
            'question': e.name,
            'answer': e.value,
            'time': time
        };
        // Dispatch to save time and selected answer
        $.ajax({
                type:'POST',
                url: `${url}checked/save/`,
                dataType:'json',
                data:result,
                success: function(res){
//                    console.log(res);
                },
                error: function(error){
                    console.log(error)
                }
        })
    }
}


const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el=>{
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (el.type === 'radio' && !data[el.name]) {
                data[el.name] = null
            }else if(el.type === 'textarea'){
                data[el.name] = el.value
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){
            const results = response.results;
            quizForm.classList.add('not-visible');

            scoreBox.innerHTML += `<div><p>You have passed <b>${response.score.toFixed(0)}%</b> of the multiple choice questions.
            An examiner will mark your non-structured answers. <b>Final results</b> will be sent to you via <b>email</b>.<br/>
            Thank you for taking this test.
            </p>
            </div>`;

            results.forEach(res=>{
                const resDiv = document.createElement("div");
                for (const [question, resp] of Object.entries(res)){

                    resDiv.innerHTML += question
                    const cls = ['p20', 'white-text', 'mb10', 'z-depth-1'];
                    resDiv.classList.add(...cls);

                    if (resp=='not answered') {
                        resDiv.innerHTML += '- Not answered';
                        resDiv.classList.add('danger-bg');
                    } else {
                        const answer = resp['answered'];
                        const correct = resp['correct_answer'];

                        if (answer == correct) {
                            resDiv.classList.add(...['success-bg']);
                            resDiv.innerHTML += ` Answered: ${answer}`;
                        } else {
                            resDiv.classList.add(...['danger-bg']);
                            resDiv.innerHTML += ` | Correct answer: ${correct}`;
                            resDiv.innerHTML += ` | Answered: ${answer}`;
                        }
                    }
                }

                resultBox.append(resDiv);
            })
            clearInterval(timer);
            clearInterval(updateInterval);
        },
        error: function(error){
            console.log(error)
        }
    })
}



quizForm.addEventListener('submit', e=>{
    e.preventDefault()

    sendData()
})