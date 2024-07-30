$("#flw").click(function() {
    var t = $("#flw").text();
    if(t == "Follow") {
        $.post($SCRIPT_ROOT + "/follow", 
        { 
            usuario: $("#user").text() 
        }, 
        function(data, success) {
            // alert(data.result + " status: " + success);
            $("#flw").text('Following');
            $("#flw").removeClass('btn-primary');
            $("#flw").addClass('btn-secondary');
        });
    }
    else if(t == "Following") {
        $.post($SCRIPT_ROOT + "/unfollow", 
        { 
            usuario: $("#user").text() 
        }, 
        function(data, success) {
            // alert(data.result + " status: " + success);
            $("#flw").text('Follow');
            $("#flw").removeClass('btn-secondary');
            $("#flw").addClass('btn-primary');
        });
    }
});