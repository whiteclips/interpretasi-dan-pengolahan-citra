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

// function updateImageWithTreshold(treshold) {
//     // value below treshold = 0
//     var imgData = getImgDataFrom('before-canvas');
//     var newData = imgData.map(x => (x < treshold) ? 0 : 255);

//     drawOnCanvasFromArray('after-canvas', newData);
// }

$(document).ready( function() {

    document.getElementById('input-image').onchange = function(e) {
        isUploaded = true;
        img.src = URL.createObjectURL(e.target.files[0]);
        img.onload = function () {
            drawOnCanvasFromImage('before-canvas', img);
            // drawOnCanvasFromImage('after-canvas', img);
        }
    };

    document.getElementById('preprocess-method').onchange = function(e) {
        if ($('#preprocess-method').val() == 7) {
            $('#input-custom').css('display','block');
            $('#input-custom-2').css('display','block');
        }
    };

    // $('input[type=range]').on('input', function () {
    //     $(this).trigger('change');
    // });

    // document.getElementById('pixel-treshold').onchange = function(e) {
    //     const value = $('#pixel-treshold').val();
    //     $('#label-pixel-treshold').text('Noise threshold (' + value + ')');
    //     updateImageWithTreshold(value);
    // };
    
    // document.getElementById('noice-threshold').onchange = function(e) {
    //     const value = $('#noice-threshold').val();
    //     $('#range-label').text('Pixel threshold (' + value + ')');
    //     updateImageWithTreshold(value);
    // };
    
    document.getElementById('button-preprocess').onclick = function(e) {
        
        if (!validateForm()) {
            return;
        }
        
        // disable input
        $('#button-preprocess').text('Processing..');
        $('#button-preprocess').prop('disabled', true);
        $('#input-image').prop('disabled', true);

        // Get image data from canvas
        // let canvas = document.getElementById("myCanvas");
        // let ctx = canvas.getContext("2d");
        // let imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);

        var formData = new FormData();
        formData.append('file', $('#input-image')[0].files[0]);
        formData.append('method', $('#preprocess-method').val());

        console.log("PreprocessMethod val : ", $('#preprocess-method').val());
        if ($('#preprocess-method').val() == "7") {
            let matrix1 = $('.m1_val');
            let matrix2 = $('.m2_val');
            let m1 = [];
            let m2 = [];
            for (var i=0; i< matrix1.length;  i++) {
                m1.push(parseInt(matrix1[i].value));
                m2.push(parseInt(matrix2[i].value));
            }

            console.log("M1: ",m1)
            console.log("M2: ",m2)
            formData.append('matrix1', m1);
            formData.append('matrix2', m2);
        }

        // let pixelTreshold = $('#pixel-treshold').val();
        // formData.append('pixel-treshold', pixelTreshold);
        // let noiceTreshold = $('#noice-threshold').val() / 255;
        // formData.append('noise', noiceTreshold);
        $.ajax({
            url : '/preprocess_image',
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
                $('#button-preprocess').text('Identify Image');
                $('#button-preprocess').prop('disabled', false);
                $('#input-image').prop('disabled', false);
            }
        });
    };
});

// function getImgDataFrom(canvas_id) {
//     var canvas = document.getElementById(canvas_id);
//     var ctx = canvas.getContext("2d");
//     var imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
//     return imgData.data;
// }

// function drawOnCanvasFromArray(canvas_id, imgArray) {
//     var canvas = document.getElementById(canvas_id);
//     var ctx = canvas.getContext("2d");
//     ctx.clearRect(0, 0, canvas.width, canvas.height);
//     canvas.width = img.width;
//     canvas.height = img.height;
//     var imgData = ctx.createImageData(img.width, img.height);
//     // copy img byte-per-byte into our ImageData
//     var data = imgData.data;
//     for (var i = 0, len = img.width * img.height * 4; i < len; i++) {
//         data[i] = imgArray[i];
//     }
//     ctx.putImageData(imgData, 0, 0);
// }

function drawOnCanvasFromImage(canvas_id, img_elmt) {
    var canvas = document.getElementById(canvas_id);
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    console.log(img_elmt.width, img_elmt.height);
    canvas.width = img_elmt.width;
    canvas.height = img_elmt.height;
    ctx.drawImage(img_elmt, 0, 0);
}
