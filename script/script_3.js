var myChart;
var redGlobal, blueGlobal, greenGlobal, grayscaleGlobal;
var editMode = false;

var imgDataGlobal;
var ctxGlobal;
var canvasGlobal;

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

function editHistogram(grayscale) {
    editMode = true;
    $('#btn-edit-histogram').text('Save Histogram');
    $('.chart-hint').text('Edit Mode (See preview above)');
    $('#myChart').hide();
    $('#myChartEditMode').show();

    var grayscale = [];
    //  Dont change this value for now
    var label = [0, 63, 127, 191, 255];

    for (let i=0; i<5; i++) {
        grayscale[i] = grayscaleGlobal[label[i]];
    }

    var ctx = document.getElementById("myChartEditMode").getContext('2d');
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: label,
            datasets: [{
                label: 'Grayscale',
                data: grayscale,
                backgroundColor: [
                    'rgba(54, 54, 54, 0.2)',
                ],
                borderColor: 'rgba(54, 54, 54, 1)',
                borderWidth: 1,
                // pointRadius: 1,
            }]
        },
        options: {
            dragData: true,
            dragX: false,
            onDragStart: function (event, element) {
    
            },
            onDrag: function (event, datasetIndex, index, value) {

            },
            onDragEnd: function (event, datasetIndex, index, value) {
                //  Updating value of histogram array
                // TODO: update grayscaleGlobal
                // TODO: update gambar
                grayscaleGlobal[label[index]] = value;
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true,
                        max: 10000,
                        min: 0,
                    }
                }]
            }
        }
    });
}

function saveHistogram() {
    editMode = false;
    $('#btn-edit-histogram').text('Edit Histogram');
    $('.chart-hint').text('Click on label below to show/hide chart');
    $('#myChart').show();
    $('#myChartEditMode').hide();

    //  Updating value of histogram array
    var label = [0, 63, 127, 191, 255];
    for (let i = 1; i < 5; i++) {
        var deltaY = grayscaleGlobal[label[i]] - grayscaleGlobal[label[i - 1]];
        var deltaX = label[i] - label[i - 1];
        var m = deltaY / deltaX;
        for (let j = label[i - 1] + 1; j < label[i]; j++) {
            grayscaleGlobal[j] = grayscaleGlobal[j - 1] + m;
        }
    }

    drawHistogram(redGlobal, greenGlobal, blueGlobal, grayscaleGlobal);

    //  Updating image
    var min = Math.min.apply(null, grayscaleGlobal);
    var max = Math.max.apply(null, grayscaleGlobal);
    var range = max - min;
    var unit = 256 / range;
    for (let i = 0; i < imgDataGlobal.data.length; i += 4) {
        var currentValue = imgDataGlobal.data[i];
        imgDataGlobal.data[i] = grayscaleGlobal[currentValue] * unit;
    }

    var canvasResult = document.getElementById("myCanvasResult");
    var imageSrc = document.getElementById("container-image");
    console.log(imageSrc.width, imageSrc.height);
    canvasResult.width = imageSrc.width;
    canvasResult.height = imageSrc.height;
    var contextResult = canvasResult.getContext("2d");
    contextResult.putImageData(imgDataGlobal, 0, 0);
    // var result = document.getElementById("container-image-result");
    // contextResult.drawImage(result, canvasResult.width, canvasResult.height);
}

function drawHistogram(red, green, blue, grayscale) {
    $('#btn-edit-histogram').show();
    $('.chart-hint').show();
    $('#histogram-text').show();
    $('#histogram-boundary').show();
    $('#myChart').show();
    $('#myChartEditMode').hide();

    $('html,body').animate({scrollTop: document.body.scrollHeight},"medium");

    let label = [];
    
    for (let i=0; i<256; i++) {
        label[i] = i;
    }
    
    var ctx = document.getElementById("myChart").getContext('2d');
    myChart = new Chart(ctx, {
        type: 'bar',
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
                    hidden: true,
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
                    // hidden: true,
                },

            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true,
                        max: 10000,
                        min: 0,
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
    $('#myChart').hide();
    $('#myChartEditMode').hide();
    $('#btn-edit-histogram').hide();
    
    document.getElementById('input-image').onchange = function(e) {
        let img = new Image();
        img.onload = draw;
        img.src = URL.createObjectURL(this.files[0]);
        $('#container-image').attr('src', img.src);

        $('#myChart').hide();
        $('#myChartEditMode').hide();
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
        canvasGlobal = canvas;
        let ctx = canvas.getContext("2d");
        ctxGlobal = ctx;
        let imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        console.log(imgData);
        imgDataGlobal = imgData;
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
        redGlobal = redHist;
        greenGlobal = greenHist;
        blueGlobal = blueHist;
        grayscaleGlobal = grayscaleHist;
        
        // enable input
        $('#button-generate-histogram').text('Generate Histogram');
        $('#button-generate-histogram').prop('disabled', false);
        $('#input-image').prop('disabled', false);
        $('.form-control').prop('disabled', false);
    };

    document.getElementById('btn-edit-histogram').onclick = function(e) {
        if (editMode)
            saveHistogram();
        else {
            editHistogram(grayscaleGlobal);
        }
    }
    
});
