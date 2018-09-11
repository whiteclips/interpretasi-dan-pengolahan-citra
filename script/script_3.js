function draw() {
    let canvas = document.getElementById('myCanvas');
    canvas.width = this.width;
    canvas.height = this.height;
    let ctx = canvas.getContext('2d');
    ctx.drawImage(this, 0,0);
}

function validateForm() {
    var image = document.getElementById("container-image").getAttribute("src");
    if (image == null) {
        alert("Please upload an image!");
        return false;
    }

    return true;
}

function drawHistogram(red, green, blue, grayscale) {

    $('.chart-hint').show();
    $('#histogram-text').show();
    $('#histogram-boundary').show();
    $('#myChart').show();

    $('html,body').animate({scrollTop: document.body.scrollHeight},"medium");

    var ctx = document.getElementById("myChart").getContext('2d');
    let label = [];
    let redHist = [];
    let greenHist = [];
    let blueHist = [];
    let grayHist = [];

    for (let i=0; i<256; i++) {
        label[i] = i;
        redHist[i] = "rgba("+i+", 0, 0, 1)";
        greenHist[i] = "rgba(0, "+i+", 0, 1)";
        blueHist[i] = "rgba(0, 0, "+i+", 1)";
        grayHist[i] = "rgba(40, 40, 40, 1)";
    }

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: label,
            datasets: [
                {
                    label: 'Red',
                    data: red,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                    ],
                    borderColor: 'rgba(255, 0, 0, 1)',
                    borderWidth: 2,
                    pointRadius: 0,
                },
                {
                    label: 'Green',
                    data: green,
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                    ],
                    borderColor: 'rgba(0, 255, 0, 1)',
                    borderWidth: 1,
                    pointRadius: 0,
                    hidden: true,
                },
                {
                    label: 'Blue',
                    data: blue,
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.2)',
                    ],
                    borderColor: 'rgba(0, 0, 255, 1)',
                    borderWidth: 1,
                    pointRadius: 0,
                    hidden: true,
                },
                {
                    label: 'Grayscale',
                    data: grayscale,
                    backgroundColor: [
                        'rgba(54, 54, 54, 0.2)',
                    ],
                    borderColor: 'rgba(54, 54, 54, 1)',
                    borderWidth: 1,
                    pointRadius: 0,
                    hidden: true,
                },

            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}

$(document).ready( function() {

    $('.chart-hint').hide();
    $('#histogram-text').hide();
    $('#histogram-boundary').hide();
    
    document.getElementById('input-image').onchange = function(e) {
        let img = new Image();
        img.onload = draw;
        img.src = URL.createObjectURL(this.files[0]);
        $('#container-image').attr('src', img.src);

        $('#myChart').hide();
        $('.chart-hint').hide();
        $('#histogram-text').hide();
        $('#histogram-boundary').hide();
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

        coefficientRed = 0.333;
        coefficientGreen = 0.333;
        coefficientBlue = 0.333;
        
        let canvas = document.getElementById("myCanvas");
        let ctx = canvas.getContext("2d");
        let imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        // console.log(imgData);
        
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