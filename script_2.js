// Declaring the source/original image as global variable
var srcImgElmt = new Image();
srcImgElmt.onload = function () {
    drawOnCanvasFromImage('before-canvas', srcImgElmt);
}

$(document).ready(function () {
    var $upload = document.getElementById('imageUpload');
    $upload.addEventListener('change', updateImage);
    $("input[type='radio']").click(processImageOnAlgo);
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

function processImageOnAlgo() {
    switch (Number(this.value)) {
        case 1:
            doCumulativeAlgo();
            break;
        case 2:
            doEqualizeAlgo();
            break;
        default:
            console.log("Wrong algo");
            break;
    }
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

    for (var i = 0; i < rawImgArr.length; i += 4) {
        rgb['red'][rawImgArr[i]]++;
        rgb['green'][rawImgArr[i + 1]]++;
        rgb['blue'][rawImgArr[i + 2]]++;
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