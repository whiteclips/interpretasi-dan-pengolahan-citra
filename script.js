$(document).ready( function() {
    $(document).on('change', '.btn-file :file', function() {
    var input = $(this),
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [label]);
    });

    $('.btn-file :file').on('fileselect', function(event, label) {
        
        var input = $(this).parents('.input-group').find(':text'),
            log = label;
        
        if( input.length ) {
            input.val(log);
        } else {
            if( log ) alert(log);
        }
    
    });
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            
            reader.onload = function (e) {
                $('#container-image').attr('src', e.target.result);
            }
            
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#input-image").change(function(){
        readURL(this);
    }); 	
});

function drawHistogram(red, green, blue, grayscale) {

    var x = [];
    // var y = [];
    for (var i = 0; i < 255; i ++) {
        x[i] = i;
        // y[i] = Math.random() * 100;
    }

    var layout = {
        xaxis: {
            range: [0, 255]
        }
    };

    var redTrace = {
        x: x,
        y: red,
        type: 'bar',
    };

    var greenTrace = {
        x: x,
        y: green,
        type: 'bar',
    };

    var blueTrace = {
        x: x,
        y: blue,
        type: 'bar',
    };

    var grayscaleTrace = {
        x: x,
        y: grayscale,
        type: 'bar',
    };

    var data = [redTrace];
    Plotly.newPlot('histogram-red', data, layout);
    var data = [greenTrace];
    Plotly.newPlot('histogram-green', data);
    var data = [blueTrace];
    Plotly.newPlot('histogram-blue', data);
    var data = [grayscaleTrace];
    Plotly.newPlot('histogram-grayscale', data);
}
