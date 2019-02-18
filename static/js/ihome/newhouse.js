function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $('#form-house-info').submit(function(e){
        e.preventDefault();
//        异步提交ajax
        $(this).ajaxSubmit({
            url:'/house/newhouse_info/',
            type:'POST',
            dataType:'json',
            success:function(data){
                if(data.code == '200'){
                    $('#form-house-info').hide()
                    $('#form-house-image').show()
                    $('#house-id').attr('value',data.data)
                }
                if(data.code == '1001'){
                    $('.error-msg span').html(data.msg)
                    $('.error-msg').show()
                }
            }
        })
    })

    $.get('/house/area/', function(data){
        if(data.code == '200'){
            for(var n in data.data){
                var optNode = $('<option>')
                optNode.html(data.data[n].name)
                optNode.attr('value', ++n)
                $('#area-id').append(optNode)
            }
            for(var n in data.faci){
                var optNode1 = $('<li><div class="checkbox"><label><input type="checkbox" name="facility" value="' + data.faci[n].id + '">' + data.faci[n].name + '</label></div></li>')
                $('.house-facility-list').append(optNode1)
            }
        }
    })

    $('#form-house-image').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/house_image/',
            type:'PATCH',
            dataType: 'json',
            success:function(data){
                if(data.code == '200'){
                    var optNode = $('<div class="house-image-change" style="background-color:white" ><img id="house-image-my" src="/static/imgs/' + data.data + '/"></div>')
                    $('.house-title').after(optNode)
                    $(".house-image-change img").css("width","100%")
                    $(".house-image-change img").css("height","600px")
                }
            }
        })
    })
})