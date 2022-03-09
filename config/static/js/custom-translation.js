const getCookie = (name) => {
    let value = '; ' + document.cookie,
        parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const reload_page = () => {
    window.location.reload(true);
}

$('#language-list a').on('click', function (event) {
    event.preventDefault();
    const target = $(event.target);
    const url = target.attr('href');
    const language_code = target.data('language-code');
    console.log(url, language_code)
    $.ajax({
        type: 'POST',
        url: url,
        data: {language: language_code},
        headers: {"X-CSRFToken": getCookie('csrftoken')}
    }).done(function (data, textStatus, jqXHR) {
        reload_page();
    });
});