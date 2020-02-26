function selectAll(param){
    $('input[type="checkbox"]:visible').each(function() {
        this.checked = param.checked
    })
}

function searchTable(param, access_id) {
    let text = $(param).val().toLowerCase()
    $(`#${access_id} tr`).filter(
        function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(text) > -1)
    })
}

function getCookie (name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';')
        for (let i=0; i<cookies.length; i++) {
            let cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}

function formatTimestamp(timestamp) {
    return timestamp.slice(0,16)
}

function parseDate(date) {
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    let day = date.getDate();
    return `${year}-${month}-${day}`
}
