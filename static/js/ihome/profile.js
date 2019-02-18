function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('#form-avatar').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/profile/',
            dataType:'json',
            type:'PATCH',
            success:function(data){
                if(data.code == '200'){
                    $(location).attr('href', '/user/my/')
                }
            },
            error:function(data){
                alert('请求失败！')
            }
        })
    })
    $('#form-name').submit(function (e) {
        e.preventDefault();
        name = $("#user-name").html()
        $(this).ajaxSubmit({
            url:'/user/mm_profile/',
            type:'POST',
            dataType:'json',
            data:{'name':name},
            success:function(data){
                if(data.code == 200){
                    location.href = '/user/my/'
                }
                if(data.code == 1010){
                    $('#name-err span').html(data.msg)
                    $('#name-err').show()
                }
                if(data.code == 1011){
                    $('#name-err span').html(data.msg)
                    $('#name-err').show()
                }
            }
        })
    })
})
