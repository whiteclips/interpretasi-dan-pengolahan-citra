var url = "/example";
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
    
    document.getElementById('button-preprocess').onclick = function(e) {
        
        if (!validateForm()) {
            return;
        }

        // disable input
        $('#button-preprocess').text('Processing..');
        $('#button-preprocess').prop('disabled', true);
        $('#input-image').prop('disabled', true);

        var formData = new FormData();
        formData.append('file', $('#input-image')[0].files[0]);

        $.ajax({
            url : '/face_detection_process',
            type : 'POST',
            data : formData,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success : function(data) {
                $("#result").attr("src",data.path);
                // $("#result-pred").text(data.prediction);
            },
            error: function() {
                alert ('Oops, Something went wrong');
            },
            complete: function() {
                // enable input
                $('#button-preprocess').text('Detect now!');
                $('#button-preprocess').prop('disabled', false);
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
