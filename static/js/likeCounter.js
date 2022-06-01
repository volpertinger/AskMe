function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$(".btn_like").on('click', function (ev) {
    const $this = $(this);
    console.log('liked');
    console.log('this id=' + $this.data("id"));

    const request = new Request(
        'http://127.0.0.1:8000/vote/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'data_id=' + $this.data('id') + ' like'
        }
    )
    fetch(request).then(function (response) {
        console.log(request);
    })
})

$(".btn_dislike").on('click', function (ev) {
    console.log('disliked');
})