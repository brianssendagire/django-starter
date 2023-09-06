var resultBox = document.getElementById('result-box')
const url = window.location.href;
$.ajax({
        type:'GET',
        url: `${url}data`,
        success: function(res){
            const status = res.status;
            const data = res.answers;
            if(status == 202){
                data.forEach((el, index) => {
                    const question = el['question']
                    const answered = el['answered']
                    const non_structured =  el['non_structured'];
                    const id = el['id']
                    const ques = question.text;

                    resultBox.innerHTML += `
                    ${index==0 ? "": '<div class="divider mt10 mb20"></div>'}
                        <div class="mb10 mt10">
                            <b>${ques}</b>
                        </div>
                    `;
                    if(!non_structured){
                        const ans = `${answered != null ? answered.text : 'Not Answered'}`;
                        const correct = el['correct']
                        const correct_answer = el['correct_answer']

                        var input = document.createElement("input");
                        input.type = "radio"
                        input.classList.add(...["ans", "with-gap"])
                        input.setAttribute('id', `${ques}-${ans}`)
                        input.setAttribute('name', `${ques}`)
                        input.setAttribute('value', `${ans}`)
                        input.setAttribute('onclick', "getSelected(this)")

                        input.setAttribute("checked", "")
                        var radioDiv = document.createElement("div");
                        radioDiv.classList.add("radio")
                        var label = document.createElement("label")
                        var span = document.createElement("span")
                        span.innerHTML = `${ans}`
                        label.append(input)
                        label.append(span)
                        radioDiv.append(label)
                        resultBox.append(radioDiv);
                        var correctClass = `${correct ? 'green-text' : 'red-text'}`
                        var extras = `<div class="row text-dark mt20">
                                        <div class="col s12 m6" id="actions">
                                            <span class="section-label">Correct: </span>
                                            <span class="info-text ${correctClass}">${correct ? 'Yes': 'No'}</span>
                                        </div>
                                        <div class="col s12 m6">
                                            <span class="section-label">Correct Answer: </span>
                                            <span class="info-text">${correct_answer.text}</span>
                                        </div>
                                    </div>`
                        resultBox.insertAdjacentHTML("beforeend", extras);
                    }else{
                        const explanation = el['answered_explanation']
                        const quiz_id = el['quiz'].id
                        resultBox.innerHTML += `<div class="row">
                                <div class="input-field col s12 text-section">
                                  <textarea name="${ques}" class="ans non-structured materialize-textarea" disabled="">${explanation}</textarea>
                                </div>
                              </div>`;
                        const examined = el['examined']
                        const non_structured_score = el['non_structured_score']
                        var score = `${examined ? non_structured_score : ''}`
                        resultBox.innerHTML += `<div class="row">
                                                <div class="input-field col m6 s12 marking-section">
                                                    <input id="${ques}-${id}" type="number"
                                                    data-id=${id}
                                                    data-quiz_id=${quiz_id}
                                                    class="score-mark" placeholder="" value=${score}>
                                                    <label class="active" for="${ques}-${id}"><span>Score (Out of 10)</span></label>
                                                </div>`;
                    }
                })
            }
        },
        error: function(error){
            console.log(error)
        }
});

const isEmpty = str => !str.trim().length;

const sendData = () => {
    const elements = [...document.getElementsByClassName('score-mark')]
    var valid = true
    var mark = 0
    var result = {}
    var data = []

    for(const el of elements){
        const score = el.value;
        if(isEmpty(score)){
                var parent = el.parentElement;
                var errors = document.createElement('div')
                errors.classList.add("errors")
                var small = document.createElement("small")
                small.classList.add("error")
                small.innerHTML = "Score is required"
                errors.append(small)
                parent.append(errors);
                valid = false;
        }

        const id = el.getAttribute('data-id');
        const quiz_id = el.getAttribute('data-quiz_id');
        mark += parseInt(score);
        data.push({'id': id, 'score': score, 'quiz_id': quiz_id});
    }

    result['mark'] = mark
    result["data"] = JSON.stringify(data)

    if(valid){
        $.ajax({
            type:'POST',
            url: `${url}mark/`,
            dataType:'json',
            data:result,
            success: function(res){
                if(res.status==200){
                    M.toast({html: `Updated with percentage score: ${parseFloat(res.percentage_score).round(2)}%.`, displayLength: 5000, classes: "toast-success"})
                    setTimeout(function(){ history.back() }, 2500);
                }else{
                    M.toast({html: `Something went wrong, please contact your administrator if persists.`, displayLength: 5000, classes: "toast-error"})
                }
            },
            error: function(error){
                console.log(error)
            }
        })
    }else{
        M.toast({html: "Fix some errors.", displayLength: 3000, classes: "toast-error"})
    }

}

Number.prototype.round = function(places) {
  return +(Math.round(this + "e+" + places)  + "e-" + places);
}

const resultForm = document.getElementById('result-form')
resultForm.addEventListener('submit', e=>{
    e.preventDefault();

    sendData()
})