// Declaring the source/original image as global variable
var srcImgElmt = new Image();
srcImgElmt.onload = function () {
    drawOnCanvasFromImage('before-canvas', srcImgElmt);
    console.log("Pre Executed");
    console.log(this.src);
    $('#before-image').attr('src', this.src);
    console.log("Executed");
}

$(document).ready(function () {
    var $upload = document.getElementById('imageUpload');
    $upload.addEventListener('change', updateImage);
    $("#btn-cumulative").click(doCumulativeAlgo);
});

function updateImage(evt) {
    var file = evt.target.files[0];
    srcImgElmt.src = URL.createObjectURL(file);
}

function getImgDataFrom(canvas_id) {
    var canvas = document.getElementById(canvas_id);
    var ctx = canvas.getContext("2d");
    var imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    return imgData.data;
}

function drawHistogram(rgbArray,afterRgbArray) {
    var x = [];
    var redColor = [];
    var greenColor = [];
    var blueColor = [];
    var grayColor = [];
    for (var i = 0; i < 255; i++) {
        x[i] = i;
        redColor[i] = 'rgb(' + i + ', 0, 0)';
        greenColor[i] = 'rgb(0,' + i + ', 0)';
        blueColor[i] = 'rgb(0, 0, ' + i + ')';
        grayColor[i] = 'rgb(' + i + ',' + i + ',' + i + ')';
    }


    var trace = {
        x: x,
        y: rgbArray['red'],
        marker: { color: redColor },
        type: 'bar',
    };

    Plotly.newPlot('histogram-red-before', [{ ...trace, y: rgbArray['red'], marker: { color: redColor }}]);
    Plotly.newPlot('histogram-green-before', [{ ...trace, y: rgbArray['green'], marker: { color: greenColor }}]);
    Plotly.newPlot('histogram-blue-before', [{ ...trace, y: rgbArray['blue'], marker: { color: blueColor }}]);
    Plotly.newPlot('histogram-gray-before', [{ ...trace, y: rgbArray['gray'], marker: { color: grayColor }}]);
    Plotly.newPlot('histogram-red-after', [{ ...trace, y: afterRgbArray['red'], marker: { color: redColor }}]);
    Plotly.newPlot('histogram-green-after', [{ ...trace, y: afterRgbArray['green'], marker: { color: greenColor }}]);
    Plotly.newPlot('histogram-blue-after', [{ ...trace, y: afterRgbArray['blue'], marker: { color: blueColor }}]);
    Plotly.newPlot('histogram-gray-after', [{ ...trace, y: afterRgbArray['gray'], marker: { color: grayColor }}]);

    // var greenTrace = {
    //     x: x,
    //     y: green,
    //     marker: {color: greenColor},
    //     type: 'bar',
    // };

    // var blueTrace = {
    //     x: x,
    //     y: blue,
    //     marker: {color: blueColor },
    //     type: 'bar',
    // };

    // var grayscaleTrace = {
    //     x: x,
    //     y: grayscale,
    //     marker: {color: grayColor },
    //     type: 'bar',
    // };


}

function doCumulativeAlgo() {
    if (srcImgElmt.src == "") {
        console.log("TODO: Insert warning error bcs img not uploaded");
    } else {
        var rawImgArray = getImgDataFrom('before-canvas');
        var rgbArray = getRGBArray(rawImgArray);
        var rgbMapper = getRGBMapper(rgbArray);
        var mappedArray = mapArray(rawImgArray, rgbMapper);
        drawOnCanvasFromRGB('after-canvas', srcImgElmt.width, srcImgElmt.height, mappedArray);
        drawHistogram(rgbArray, getRGBArray(mappedArray));
    }
}

function getRGBArray(rawImgArr) {
    var initArray = new Array(256);
    for (var i = 0; i < initArray.length; i++) {
        initArray[i] = 0;
    }
    var rgb = {};
    rgb['red'] = initArray.slice();
    rgb['green'] = initArray.slice();
    rgb['blue'] = initArray.slice();
    rgb['gray'] = initArray.slice();

    for (var i = 0; i < rawImgArr.length; i += 4) {
        rgb['red'][rawImgArr[i]]++;
        rgb['green'][rawImgArr[i + 1]]++;
        rgb['blue'][rawImgArr[i + 2]]++;
        var grayValue = Math.floor((rawImgArr[i] + rawImgArr[i + 1] + rawImgArr[i + 2]) / 3);
        rgb['gray'][grayValue]++;
    }
    return rgb;
}

function getRGBMapper(rgbArray) {
    var mapper = {}
    mapper['red'] = getCumMapper(rgbArray['red']);
    mapper['green'] = getCumMapper(rgbArray['green']);
    mapper['blue'] = getCumMapper(rgbArray['blue']);
    return mapper;
}

function getCumMapper(imgChannelArray) {
    var cumMapper = new Array(256);
    cumMapper[0] = imgChannelArray[0];
    for (var i = 1; i < cumMapper.length; i++) {
        cumMapper[i] = cumMapper[i - 1] + imgChannelArray[i];
    }
    // Transform
    for (var i = 0; i < cumMapper.length; i++) {
        cumMapper[i] = Math.floor(i * (cumMapper[i] / cumMapper[255]));
    }
    return cumMapper;
}

function mapArray(imgArray, mapper) {
    var mappedArr = imgArray.slice();
    for (var i = 0; i < mappedArr.length; i += 4) {
        mappedArr[i] = mapper['red'][imgArray[i]];
        mappedArr[i + 1] = mapper['green'][imgArray[i + 1]];
        mappedArr[i + 2] = mapper['blue'][imgArray[i + 2]];
        mappedArr[i + 3] = 255;
    }
    return mappedArr;
}

function drawOnCanvasFromRGB(canvas_id, width, height, rgbArray) {
    var canvas = document.getElementById(canvas_id);
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas.width = width;
    canvas.height = height;
    var imageData = new ImageData(rgbArray, width, height);
    ctx.putImageData(imageData, 0, 0);
}

function drawOnCanvasFromImage(canvas_id, img_elmt) {
    var canvas = document.getElementById(canvas_id);
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas.width = img_elmt.width;
    canvas.height = img_elmt.height;
    ctx.drawImage(img_elmt, 0, 0);
}