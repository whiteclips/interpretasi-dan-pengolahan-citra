var url = "/example";

// function draw() {
//     let canvas = document.getElementById('myCanvas');
//     canvas.width = this.width;
//     canvas.height = this.height;
//     let ctx = canvas.getContext('2d');
//     ctx.drawImage(this, 0,0, this.width, this.height);
// }

function validateForm() {
    var image = document.getElementById("container-image").getAttribute("src");
    if (image == null) {
        alert("Please upload an image!");
        return false;
    }
    return true;
}

$(document).ready( function() {


    document.getElementById('input-image').onchange = function(e) {
    
        let img = new Image();
        // img.onload = draw;
        img.src = URL.createObjectURL(this.files[0]);
        $('#container-image').attr('src', img.src);
        // var fullPath = document.getElementById("img1").src;
        // var filename = img.src.replace(/^.*[\\\/]/, '');
    };


    $('input[type=range]').on('input', function () {
        $(this).trigger('change');
    });

    document.getElementById('noice-threshold').onchange = function(e) {
        const value = $('#noice-threshold').val();
        console.log(value);
        $('#range-label').text('Noise threshold (' + value + '%)');
    };
    
    document.getElementById('button-read-text').onclick = function(e) {
        
        if (!validateForm()) {
            return;
        }
        
        // disable input
        $('#button-read-text').text('Processing..');
        $('#button-read-text').prop('disabled', true);
        $('#input-image').prop('disabled', true);

        // Get image data from canvas
        // let canvas = document.getElementById("myCanvas");
        // let ctx = canvas.getContext("2d");
        // let imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);

        var formData = new FormData();
        formData.append('file', $('#input-image')[0].files[0]);
        let noiseThreshold = $('#noice-threshold').val() / 100;
        formData.append('noise', noiseThreshold);

        $.ajax({
            url : '/thinning-process',
            type : 'POST',
            data : formData,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success : function(data) {
                $("#result").attr("src",data.path);
                $("#result-pred").text(data.prediction);
            },
            error: function() {
                alert ('Oops, Something went wrong');
            },
            complete: function() {
                // enable input
                $('#button-read-text').text('Identify Image');
                $('#button-read-text').prop('disabled', false);
                $('#input-image').prop('disabled', false);
            }
        });
    };
});
