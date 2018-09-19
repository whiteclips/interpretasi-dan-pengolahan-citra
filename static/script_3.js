var myChart, maxGlobal;
var redGlobal, blueGlobal, greenGlobal, grayscaleGlobal;
var editMode = false;
var isEdited;
var histEditTemp;
var imgDataEditTemp;

var imgDataGlobal;
var ctxGlobal;
var canvasGlobal;

function draw() {
    let canvas = document.getElementById('myCanvas');
    canvas.width = this.width;
    canvas.height = this.height;
    let ctx = canvas.getContext('2d');
    ctx.drawImage(this, 0,0, this.width, this.height);
}

function validateForm() {
    var image = document.getElementById("container-image").getAttribute("src");
    if (image == null) {
        alert("Please upload an image!");
        return false;
    }
    return true;
}

function editHistogram(histogram, color) {
    
    editMode = true;
    $('#btn-edit-histogram').text('Save Histogram');
    $('.chart-hint').text('Edit Mode (See preview above)');
    $('#myChart').hide();
    $('#myChartEditMode').show();
    $('#container-image-result').show();

    var chartData = [];
    histEditTemp = histogram;
    imgDataEditTemp = imgDataGlobal;
    //  Dont change this value for now
    var label = [0, 63, 127, 191, 255];

    for (let i=0; i<5; i++) {
        chartData[i] = histogram[label[i]];
    }

    var datasetLabel, backgroundColor, borderColor, initVal;
    if (color == 'Red') {
        datasetLabel = 'Red';
        backgroundColor = 'rgba(255, 99, 132, 0.2)';
        borderColor = 'rgba(255, 0, 0, 1)';
        initVal = 0;
    } else if (color == 'Green') {
        datasetLabel = 'Green';
        backgroundColor = 'rgba(75, 192, 192, 0.2)';
        borderColor = 'rgba(0, 255, 0, 1)';
        initVal = 1;
    } else {// blue
        datasetLabel = 'Blue';
        backgroundColor = 'rgba(54, 162, 235, 0.2)';
        borderColor = 'rgba(0, 0, 255, 1)';
        initVal = 2;
    }

    var ctx = document.getElementById("myChartEditMode").getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: label,
            datasets: [{
                label: datasetLabel,
                data: chartData,
                backgroundColor: backgroundColor,
                borderColor: borderColor,
                borderWidth: 1,
                pointRadius: 5,
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
    
                //edited flag
                isEdited = true;

                //update hist temp
                histEditTemp[label[index]] = value;

                //update another value & update imgData temp with hist temp
                var min = Math.min.apply(null, histEditTemp);
                var max = Math.max.apply(null, histEditTemp);
                var range = max - min;
                var unit = 256 / range;
                //update the content of histEditTemp
                for (let i = 1; i < 5; i++) {
                    var deltaY = histEditTemp[label[i]] - histEditTemp[label[i - 1]];
                    if (i == 1) {
                        deltaY += 1;
                    }
                    var deltaX = label[i] - label[i - 1];
                    var m = deltaY / deltaX;
                    for (let j = label[i - 1] + 1; j < label[i]; j++) {
                        histEditTemp[j] = histEditTemp[j - 1] + m;
                    }
                }
                for (let i = initVal; i < imgDataEditTemp.data.length; i += 4) {
                    var currentValue = imgDataEditTemp.data[i];
                    imgDataEditTemp.data[i] = histEditTemp[currentValue] * unit;
                }

                //update image preview with imgData temp
                var canvasResult = document.getElementById("myCanvasResult");
                var canvasSrc = document.getElementById("myCanvas");
                var imageSrc = document.getElementById("container-image");
                canvasResult.width = canvasSrc.width;
                canvasResult.height = canvasSrc.height;
                var contextResult = canvasResult.getContext("2d");
                contextResult.putImageData(imgDataEditTemp, 0, 0);
                
                //canvas to image-result preview
                let imgResult = new Image();
                imgResult.src = canvasResult.toDataURL("image/png");
                let imgResultContainer = $('#container-image-result')
                imgResultContainer.attr('src', imgResult.src);
                imgResultContainer.width = imageSrc.width;
                imgResultContainer.height = imageSrc.height;

            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true,
                        max: maxGlobal + 1000,
                        min: 0,
                    }
                }]
            }
        }
    });
}

function saveHistogram(color) {
    editMode = false;
    $('#btn-edit-histogram').text('Edit Histogram');
    $('.chart-hint').text('Click on label below to show/hide chart');
    $('#myChart').show();
    $('#myChartEditMode').hide();
    $('#colorSelector').hide();

    // TODO: hide edit mode component
    $('#container-image-result').hide();

    if (isEdited) {
        //update rgb global with edited hist
        if (color == 'Red') {
            redGlobal = histEditTemp;
        } else if (color == 'Green') {
            greenGlobal = histEditTemp;
        } else {// blue
            blueGlobal = histEditTemp;
        }
    
        //update imgdata global with imgdata temp
        imgDataGlobal = imgDataEditTemp;
    
        // TODO: update main image with new imgData
        
        var canvasResult = document.getElementById("myCanvasResult");
        // var canvasSrc = document.getElementById("myCanvas");
        // var imageSrc = document.getElementById("container-image");
        // canvasResult.width = canvasSrc.width;
        // canvasResult.height = canvasSrc.height;
        // var contextResult = canvasResult.getContext("2d");
        // contextResult.putImageData(imgDataEditTemp, 0, 0);
        
        //canvas to image-result preview
        let img = new Image();
        img.src = canvasResult.toDataURL("image/png");
        let imgContainer = $('#container-image')
        imgContainer.attr('src', img.src);
        // imgContainer.width = imageSrc.width;
        // imgContainer.height = imageSrc.height;
    }

    drawHistogram(redGlobal, greenGlobal, blueGlobal);
}

function drawHistogram(red, green, blue) {
    $('#btn-edit-histogram').show();
    $('.chart-hint').show();
    $('#histogram-text').show();
    $('#histogram-boundary').show();
    $('#colorSelector').show();
    $('#myChart').show();
    $('#myChartEditMode').hide();

    $('html,body').animate({scrollTop: document.body.scrollHeight},"medium");

    let label = [];
    
    for (let i=0; i<256; i++) {
        label[i] = i;
    }

    var maxRed = Math.max.apply(null, red);
    var maxGreen = Math.max.apply(null, green);
    var maxBlue = Math.max.apply(null, blue);

    maxGlobal = maxRed;
    if (maxGlobal < maxGreen) maxGlobal = maxGreen;
    if (maxGlobal < maxBlue) maxGlobal = maxBlue;
    
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
                    // hidden: true,
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
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true,
                        max: maxGlobal + 1000,
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
    $('#container-image-result').hide();
    $('#colorSelector').hide();
    
    document.getElementById('input-image').onchange = function(e) {
        isEdited = false;
        let img = new Image();
        img.onload = draw;
        img.src = URL.createObjectURL(this.files[0]);
        $('#container-image').attr('src', img.src);

        $('#myChart').hide();
        $('#myChartEditMode').hide();
        $('.chart-hint').hide();
        $('#histogram-text').hide();
        $('#histogram-boundary').hide();
        $('#container-image-result').hide();
        $('#colorSelector').hide();
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
        imgDataGlobal = imgData;
        
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
        
        drawHistogram(redHist, greenHist, blueHist);
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
        var color = $('#input-component').val();
        var histogram;
        if (color == 'Red') {
            histogram = redGlobal;
        } else if (color == 'Green') {
            histogram = greenGlobal;
        } else {// blue
            histogram = blueGlobal;
        }
        if (editMode)
            saveHistogram(color);
        else {
            editHistogram(histogram, color);
        }
    }
    
});
