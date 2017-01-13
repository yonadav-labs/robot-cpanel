$(document).ready(function() {
    var $uploadCrop;

    // read image file using FileReader API 
    var readFile = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $uploadCrop.show();     // show the hidden crop window
                $uploadCrop.croppie('bind', { url: e.target.result });
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            // FileReader is supported in all major browsers, IE10+
            swal("Sorry - you're browser doesn't support the FileReader API");
        }
    };

    // intialize croppie on div with id image, #image
    $uploadCrop = $('#image').croppie({
        enableZoom: false,  // enable if you want to zoom feature
        viewport: {
            width: 300,     // crop image width
            height: 250,    // crop image height
            type: 'square'
        },
        boundary: {
            width: 400,     // crop window width
            height: 400     // crop window height
        },
        enableExif: true
    });

    // on user uploading image call the above mentioned function: readFile
    $('#id_gist_image').on('change', function () { readFile(this); });

    // on user submitting form, get the co-ordinates of the crop and upate form input element
    $('form').submit(function() {
        $('#id_crop').val($uploadCrop.croppie('get')['points']);
        return true;
    });
});

