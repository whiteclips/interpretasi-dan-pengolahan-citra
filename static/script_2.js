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
    $("#btn-linearStretch").click(doLinearStretch);
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

function drawHistogram(rgbArray, afterRgbArray) {
    console.log(rgbArray);
    console.log(afterRgbArray);
    var x = [];
    var redColor = [];
    var greenColor = [];
    var blueColor = [];
    for (var i = 0; i < 255; i++) {
        x[i] = i;
        redColor[i] = 'rgb(' + i + ', 0, 0)';
        greenColor[i] = 'rgb(0,' + i + ', 0)';
        blueColor[i] = 'rgb(0, 0, ' + i + ')';
    }


    var trace = {
        x: x,
        y: rgbArray['red'],
        marker: { color: redColor },
        type: 'bar',
    };

    Plotly.newPlot('histogram-red-before', [{ ...trace, y: rgbArray['red'], marker: { color: redColor } }]);
    Plotly.newPlot('histogram-green-before', [{ ...trace, y: rgbArray['green'], marker: { color: greenColor } }]);
    Plotly.newPlot('histogram-blue-before', [{ ...trace, y: rgbArray['blue'], marker: { color: blueColor } }]);

    // Plotly.newPlot('histogram-red-after', [{ ...trace, y: rgbArray['red'], marker: { color: redColor } }]);
    // Plotly.newPlot('histogram-green-after', [{ ...trace, y: rgbArray['green'], marker: { color: greenColor } }]);
    // Plotly.newPlot('histogram-blue-after', [{ ...trace, y: rgbArray['blue'], marker: { color: blueColor } }]);

    Plotly.newPlot('histogram-red-after', [{ ...trace, y: afterRgbArray['red'], marker: { color: redColor } }]);
    Plotly.newPlot('histogram-green-after', [{ ...trace, y: afterRgbArray['green'], marker: { color: greenColor } }]);
    Plotly.newPlot('histogram-blue-after', [{ ...trace, y: afterRgbArray['blue'], marker: { color: blueColor } }]);
    // Plotly.newPlot('histogram-gray-after', [{ ...trace, y: afterRgbArray['gray'], marker: {color: 'rgb(70,70,70)'}}]);

}

function doCumulativeAlgo() {
    if (srcImgElmt.src == "") {
        console.log("TODO: Insert warning error bcs img not uploaded");
    } else {
        var rawImgArray = getImgDataFrom('before-canvas');
        var rgbArray = getRGBArray(rawImgArray);
        var rgbMapper = getRGBMapper(rgbArray, "cumulative");
        var mappedArray = mapArray(rawImgArray, rgbMapper);
        drawOnCanvasFromRGB('after-canvas', srcImgElmt.width, srcImgElmt.height, mappedArray);
        drawHistogram(rgbArray, getRGBArray(mappedArray));
    }
}

function doLinearStretch() {
    if (srcImgElmt.src == "") {
        console.log("TODO: Insert warning error bcs img not uploaded");
    } else {
        var rawImgArray = getImgDataFrom('before-canvas');
        var rgbArray = getRGBArray(rawImgArray);
        var rgbMapper = getRGBMapper(rgbArray, "linear-stretch");
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

function getRGBMapper(rgbArray, type) {
    var mapper = {}
    if (type == "cumulative") {
        mapper['red'] = getCumMapper(rgbArray['red']);
        mapper['green'] = getCumMapper(rgbArray['green']);
        mapper['blue'] = getCumMapper(rgbArray['blue']);
    } else if (type == "linear-stretch") {
        mapper['red'] = getLinearStretchMapper(rgbArray['red']);
        mapper['green'] = getLinearStretchMapper(rgbArray['green']);
        mapper['blue'] = getLinearStretchMapper(rgbArray['blue']);
    }
    return mapper;
}

function getLinearStretchMapper(imgChannelArray) {
    const NMIN = 0;
    const NMAX = 255;
    var OMIN = 0, OMAX = 255;
    // Get OMIN
    console.log("Will loop");
    while (imgChannelArray[OMIN] == 0) OMIN++;
    while (imgChannelArray[OMAX] == 0) OMAX--;
    console.log("OMIN ",OMIN," , OMAX ",OMAX);
    var space = (NMAX - NMIN) / (OMAX - OMIN);
    console.log("NMAX-NMIN: ",(NMAX-NMIN)," OMAX-OMIN: ",(OMAX-OMIN)," SPACE ",space);
    var bins = OMAX - OMIN;
    var cumMapper = imgChannelArray.slice();
    for (var i = 0; i <= bins; i++) {
        cumMapper[i + OMIN] = NMIN + Math.floor(i * space);
        console.log(cumMapper[i+OMIN]);
    }
    return cumMapper;
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