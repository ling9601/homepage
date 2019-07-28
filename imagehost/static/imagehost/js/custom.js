
$(document).ready( function() {
    //for image upload and preview
    
    // set file name
    $('.custom-file :file').on('fileselect', function(event, label) {
        
        $(this).next('.custom-file-label').html(label)

    });

    // preview picture
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            
            reader.onload = function (e) {
                $('#img-upload').attr('src', e.target.result);
            }
            
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#id_picture").change(function(){
        readURL(this);

        // get file name
        var input = $(this),
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        input.trigger('fileselect', [label]);
    }); 	
});