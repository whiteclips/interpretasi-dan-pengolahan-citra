function draw() {
    let canvas = document.getElementById('myCanvas');
    canvas.width = this.width;
    canvas.height = this.height;
    let ctx = canvas.getContext('2d');
    ctx.drawImage(this, 0,0);
}

function validateForm() {
    var image = document.getElementById("container-image").getAttribute("src");
    console.log(image);
    if (image == null) {
        alert("Please upload an image!");
        return false;
    }

    return true;
}

function drawHistogram(red, green, blue, grayscale) {

    var x = [];
    var redColor = [];
    var greenColor = [];
    var blueColor = [];
    var grayColor = [];
    for (var i = 0; i < 255; i ++) {
        x[i] = i;
        redColor[i] = 'rgb('+i+', 0, 0)';
        greenColor[i] = 'rgb(0,'+i+', 0)';
        blueColor[i] = 'rgb(0, 0, '+i+')';
        grayColor[i] = 'rgb('+i+','+i+','+i+')';
    }



    var layout = {
        xaxis: {
            range: [0, 255]
        }
    };

    var redTrace = {
        x: x,
        y: red,
        marker: {color: redColor },
        type: 'bar',
    };

    var greenTrace = {
        x: x,
        y: green,
        marker: {color: greenColor},
        type: 'bar',
    };

    var blueTrace = {
        x: x,
        y: blue,
        marker: {color: blueColor },
        type: 'bar',
    };
    
    var grayscaleTrace = {
        x: x,
        y: grayscale,
        marker: {color: grayColor },
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

    var containers = document.getElementsByClassName("histogram-container");
    Array.prototype.forEach.call(containers, function(element) {
        element.style.display = "block";
    });

}

$(document).ready( function() {
    
    document.getElementById('input-image').onchange = function(e) {
        let img = new Image();
        img.onload = draw;
        img.src = URL.createObjectURL(this.files[0]);
        $('#container-image').attr('src', img.src);
    };
    
    document.getElementById('button-generate-histogram').onclick = function(e) {
        
        if (!validateForm()) {
            return;
        }
        
        // disable input
        $('#button-generate-histogram').text('Generating..');
        $('#button-generate-histogram').prop('disabled', true);
        $('#input-image').prop('disabled', true);
        $('.form-control').prop('disabled', true);

        var coefficientRed = document.getElementById("coefficient_red").value;
        var coefficientGreen = document.getElementById("coefficient_green").value;
        var coefficientBlue = document.getElementById("coefficient_blue").value;
        if (coefficientRed == "" || coefficientGreen == "" || coefficientBlue == "") {
            coefficientRed = 0.333;
            coefficientGreen = 0.333;
            coefficientBlue = 0.333;
        }
        
        let canvas = document.getElementById("myCanvas");
        let ctx = canvas.getContext("2d");
        let imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        console.log(imgData);
        
        //extract data
        let initArray = new Array(256);
        for (let i = 0; i<initArray.length; i++)
        initArray[i] = 0;
        let redHist = initArray.slice();
        let greenHist = initArray.slice();
        let blueHist = initArray.slice();
        let grayscaleHist = initArray.slice();
        
        for(let i=0; i<imgData.data.length; i++) {
            if (i%4==0) //redHist
            redHist[imgData.data[i]] += 1;
            else if (i%4==1) //greenHist
            greenHist[imgData.data[i]] += 1;
            else if (i%4==2) //blueHist
            blueHist[imgData.data[i]] += 1;
        }
        
        //grayscale
        let i = 0;
        while(i < imgData.data.length) {
            var red = coefficientRed * imgData.data[i];
            var green = coefficientGreen * imgData.data[i+1];
            var blue = coefficientBlue * imgData.data[i+2];
            let grayscale = Math.round(red + green + blue);
            grayscaleHist[grayscale] += 1;
            i += 4;
        }
        
        drawHistogram(redHist, greenHist, blueHist, grayscaleHist);
        
        // enable input
        $('#button-generate-histogram').text('Generate Histogram');
        $('#button-generate-histogram').prop('disabled', false);
        $('#input-image').prop('disabled', false);
        $('.form-control').prop('disabled', false);
    }
    
});
