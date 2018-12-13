let img = new Image();
var isUploaded = false;

function validateForm() {
    if (!isUploaded) {
        alert("Please upload an image!");
        return false;
    }
    return true;
}

$(document).ready( function() {

    document.getElementById('input-image').onchange = function(e) {
        isUploaded = true;
        img.src = URL.createObjectURL(e.target.files[0]);
        img.onload = function () {
            drawOnCanvasFromImage('before-canvas', img);
            // drawOnCanvasFromImage('after-canvas', img);
        }
    };
    
    document.getElementById('button-recognize').onclick = function(e) {
        
        if (!validateForm()) {
            return;
        }

        // disable input
        $('#button-recognize').text('Processing..');
        $('#button-recognize').prop('disabled', true);
        $('#input-image').prop('disabled', true);

        var formData = new FormData();
        formData.append('file', $('#input-image')[0].files[0]);
        formData.append('label', $('#image-label').val());

        $.ajax({
            url : '/face_recognition_test_process',
            type : 'POST',
            data : formData,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success : function(data) {
                $("#result").attr("src",data.result);
            },
            error: function() {
                alert ('Oops, Something went wrong');
            },
            complete: function() {
                // enable input
                $('#button-recognize').text('Recognize!');
                $('#button-recognize').prop('disabled', false);
                $('#input-image').prop('disabled', false);
            }
        });
    };
});

function drawOnCanvasFromImage(canvas_id, img_elmt) {
    var canvas = document.getElementById(canvas_id);
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    console.log(img_elmt.width, img_elmt.height);
    canvas.width = img_elmt.width;
    canvas.height = img_elmt.height;
    ctx.drawImage(img_elmt, 0, 0);
}
