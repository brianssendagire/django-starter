$(document).ready(function(){
    $('.modal').modal();
    const windowUrl = window.location.href;
    $('#quizTrigger').on('click', function(e){
        console.log(e);
        const pk = $(this).attr('data-pk');
        const title = $(this).attr('data-title');
        const url = $(this).attr('data-url');
        const max_structured_questions = $(this).attr('data-max_structured_questions');
        const max_non_structured_questions = $(this).attr('data-max_non_structured_questions');
        const time = $(this).attr('data-time');
        const pass_mark = $(this).attr('data-pass_mark');

        html = `<p>Are you sure you want to begin <b>${title}</b>?</p>
        <div>
            <span class="section-label">Total Structured Questions:</span> <span class="info-text">${max_structured_questions}</span>
        </div>
        <div>
            <span class="section-label">Total Non-Structured Questions:</span> <span class="info-text">${max_non_structured_questions}</span>
        </div>
        <div>
            <span class="section-label">Duration:</span> <span class="info-text">${time} minutes</span>
        </div>
        <div></div>`;

        $('#quizStartBtn').attr('data-url', url);
        $('#quizStartModal').find('.modal-body').html(html);
        $('#quizStartModal').modal("open");
    });

    $('#quizStartBtn').on('click', function(e){
        const slug = $(this).attr('data-url');
        window.location.href = windowUrl + slug;
    });
});