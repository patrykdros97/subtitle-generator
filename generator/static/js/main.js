console.log('Welcome in the SubtitleGenerator')

function upload_file(){
    var form_data = new FormData();
    form_data.append('file', $('input[id^="file"]')[0].files[0]);
    form_data.append('csrfmiddlewaretoken', window.CSRF_TOKEN );
    $('#spinner-box').show();
    $.ajax({
        method: 'POST',
        url:"/wav/",
        processData: false,
        contentType: false,
        data: form_data,
        success: function (data) {
            $('#spinner-box').hide()
            alert('success');
        },
        error: function (data) {
            $('#spinner-box').hide()
            alert('Something went wrong during processing file');
        },

    })
}
