function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $.get('/user/auth_info/',function(data){
        if(data.code == '200'){
            $('#real-name').val(data.data.real_name)
            $('#real-name').attr('disabled','true')
            $('#id-card').val(data.data.id_card)
            $('#id-card').attr('disabled','true')
            $('.btn').hide()
        }
    })
    $('#form-auth').submit(function(e){
        e.preventDefault();
        real_name = $("#real-name").val()
        id_card = $("#id-card").val()
//        异步提交ajax
        $.ajax({
            url: '/user/my_auth/',
            type: 'POST',
            dataType: 'json',
            data:{'real_name': real_name, 'id_card': id_card},
            success:function(data){
                if(data.code == '200'){
                    $(location).attr('href', '/user/my/')
                }
                if(data.code == '1001'){
                    $('.error-msg span').html(data.msg)
                    $('.error-msg').show()
                }
                if(data.code == '1002'){
                    $('.error-msg span').html(data.msg)
                    $('.error-msg').show()
                }
                if(data.code == '1003'){
                    $('.error-msg span').html(data.msg)
                    $('.error-msg').show()
                }
                if(data.code == '1004'){
                    $('.error-msg span').html(data.msg)
                    $('.error-msg').show()
                }
            }
        })
    })
})