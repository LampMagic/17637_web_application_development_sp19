function save_tuned(id) {
    console.log("save image");
    var dataURI = document.getElementById('tuned_photo').toDataURL('image/png');
    var fd = new FormData();
    var img_file = dataURItoFile(dataURI, "tuned_photo_"+id+".png");
    console.log(img_file);
    fd.append('photo', img_file);
    fd.append('csrfmiddlewaretoken', getCSRFToken());

    $.ajax({
        url: "/imagenation/save_photo/"+id,
        type: "POST",
        data: fd,
        processData: false,
        contentType: false,
        success: function() {
            console.log("img sent");
        }
    });

    console.log("save");
}

function download() {
    var tuned_img = document.getElementById('tuned_photo').toDataURL('image/png');
    document.getElementById("download").href = tuned_img;
    console.log("download");
}

function dataURItoFile(dataURI, fileName) {
    var byteString = atob(dataURI.split(',')[1]);
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new File([ab], fileName, {type: 'image/png',
                                     lastModified: new Date()});
}

function reset(){
    var img = document.getElementById("uploaded_photo");
    var canvas = document.getElementById('tuned_photo');
    var downloadFile = document.getElementById('download');
    var ctx = canvas.getContext('2d');

    canvas.width = img.width;
    canvas.height = img.height;
    brightness = 100;
    blur  = 0;
    contrast = 100;
    saturation = 100;
    grayscale = 0;
    hue_rotate = 0;
    opacity = 100;
    invert = 0;
    sepia = 0;

    document.getElementById('photo_brightness').value = brightness;
    document.getElementById('photo_blur').value = blur;
    document.getElementById('photo_contrast').value = contrast;
    document.getElementById('photo_saturation').value = saturation;
    document.getElementById('photo_grayscale').value = grayscale;
    document.getElementById('photo_hue_rotate').value = hue_rotate;
    document.getElementById('photo_opacity').value = opacity;
    document.getElementById('photo_invert').value = invert;
    document.getElementById('photo_sepia').value = sepia;

    ctx.filter = "brightness("+brightness.toString()+"%) " + 
                 "blur("+blur.toString()+"px) " + 
                 "contrast("+contrast.toString()+"%) " + 
                 "saturate("+saturation.toString()+"%) " + 
                 "grayscale("+grayscale.toString()+"%) " + 
                 "opacity("+opacity.toString()+"%) " + 
                 "invert("+invert.toString()+"%) " + 
                 "sepia("+sepia.toString()+"%) " + 
                 "hue-rotate("+hue_rotate.toString()+"deg ";

    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    downloadFile.addEventListener('click', download, false);
    console.log("reset");
}

function filter(){
    var img = document.getElementById("uploaded_photo");
    var canvas = document.getElementById('tuned_photo');
    var downloadFile = document.getElementById('download');
    var ctx = canvas.getContext('2d');

    canvas.width = img.width;
    canvas.height = img.height;

    brightness = document.getElementById('photo_brightness').value;
    blur  = document.getElementById('photo_blur').value;
    contrast = document.getElementById('photo_contrast').value;
    saturation = document.getElementById('photo_saturation').value;
    grayscale = document.getElementById('photo_grayscale').value;
    hue_rotate = document.getElementById('photo_hue_rotate').value;
    opacity = document.getElementById('photo_opacity').value;
    invert = document.getElementById('photo_invert').value;
    sepia = document.getElementById('photo_sepia').value;
    
    ctx.filter= "brightness("+brightness.toString()+"%) " + 
                "blur("+blur.toString()+"px) "+
                "contrast("+ contrast.toString()+"%) " + 
                "saturate("+saturation.toString()+"%) " + 
                "grayscale("+grayscale.toString()+"%) "+ 
                "opacity("+opacity.toString()+"%) "+
                "invert("+invert.toString()+"%) "+
                "sepia("+sepia.toString()+"%) "+
                "hue-rotate("+hue_rotate.toString()+"deg " ;

    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    downloadFile.addEventListener('click', download, false);
}

function random(){
    var img = document.getElementById("uploaded_photo");
    var canvas = document.getElementById('tuned_photo');
    var downloadFile = document.getElementById('download');
    var ctx = canvas.getContext('2d');

    canvas.width = img.width;
    canvas.height = img.height;

    brightness = Math.floor((Math.random() * 100.0)+50);
    blur  = Math.floor((Math.random() * 2.0));
    contrast = Math.floor((Math.random() * 50.0)+75);
    saturation = Math.floor((Math.random() * 100.0)+50);
    grayscale = Math.floor((Math.random() * 10.0));
    hue_rotate = Math.floor((Math.random() * 10.0));
    opacity = Math.floor(100-(Math.random() * 15.0));
    invert = Math.floor((Math.random() * 25.0));
    sepia = Math.floor((Math.random() * 30.0));

    document.getElementById('photo_brightness').value = brightness;
    document.getElementById('photo_blur').value = blur;
    document.getElementById('photo_contrast').value = contrast;
    document.getElementById('photo_saturation').value = saturation;
    document.getElementById('photo_grayscale').value = grayscale;
    document.getElementById('photo_hue_rotate').value = hue_rotate;
    document.getElementById('photo_opacity').value = opacity;
    document.getElementById('photo_invert').value = invert;
    document.getElementById('photo_sepia').value = sepia;
        
    ctx.filter = "brightness("+brightness.toString()+"%) " + 
                 "blur("+blur.toString()+"px) " + 
                 "contrast("+contrast.toString()+"%) " + 
                 "saturate("+saturation.toString()+"%) " + 
                 "grayscale("+grayscale.toString()+"%) "+ 
                 "opacity("+opacity.toString()+"%) " + 
                 "invert("+invert.toString()+"%) " + 
                 "sepia("+sepia.toString()+"%) " + 
                 "hue-rotate("+hue_rotate.toString()+"deg ";

    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    downloadFile.addEventListener('click', download, false);
}

function aggressive_random(){
    var img = document.getElementById("uploaded_photo");
    var canvas = document.getElementById('tuned_photo');
    var downloadFile = document.getElementById('download');
    var ctx = canvas.getContext('2d');

    canvas.width = img.width;
    canvas.height = img.height;

    brightness = Math.floor((Math.random() * 100.0)+50);
    blur  = Math.floor((Math.random() * 4.0));
    contrast = Math.floor((Math.random() * 100.0)+50);
    saturation = Math.floor((Math.random() * 100.0)+50);
    grayscale = Math.floor((Math.random() * 100.0));
    hue_rotate = Math.floor((Math.random() * 10.0));
    opacity = Math.floor(100-(Math.random() * 50.0));
    invert = Math.floor((Math.random() * 100.0));
    sepia = Math.floor((Math.random() * 100.0));

    document.getElementById('photo_brightness').value = brightness;
    document.getElementById('photo_blur').value = blur;
    document.getElementById('photo_contrast').value = contrast;
    document.getElementById('photo_saturation').value = saturation;
    document.getElementById('photo_grayscale').value = grayscale;
    document.getElementById('photo_hue_rotate').value = hue_rotate;
    document.getElementById('photo_opacity').value = opacity;
    document.getElementById('photo_invert').value = invert;
    document.getElementById('photo_sepia').value = sepia;
    
    ctx.filter = "brightness("+brightness.toString()+"%) "+ 
                 "blur("+blur.toString()+"px) " + 
                 "contrast("+contrast.toString()+"%) " + 
                 "saturate("+saturation.toString()+"%) " + 
                 "grayscale("+grayscale.toString()+"%) " + 
                 "opacity("+opacity.toString()+"%) " + 
                 "invert("+invert.toString()+"%) " + 
                 "sepia("+sepia.toString()+"%) " + 
                 "hue-rotate("+hue_rotate.toString()+"deg ";

    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    downloadFile.addEventListener('click', download, false);
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}

window.setTimeout(reset, 1000);
