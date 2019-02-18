$(document).ready(function(){
    $(".auth-warn").show();
    $.get('/house/myhouse_info/', function(data){
        if(data.code == '200'){
            $('#houses-con-ul').hide()
        }
        if(data.code == '1001'){
            $('#houses-list').hide()
        }
    })

    $.get('/house/show_house/', function(data){
        if(data.code == '200')
            for(n in data.data){
                var optNode = $('<li><a href="/house/detail/' + data.data[n].id + '"><div class="house-title"><h3>房屋ID:' + data.data[n].id + ' —— ' + data.data[n].title + '</h3></div><div class="house-content"><img src="/static/imgs/' + data.data[n].image + '"><div class="house-text"><ul><li>位于：' + data.data[n].area + '</li><li>价格：￥' + data.data[n].price + '/晚</li><li>发布时间：' + data.data[n].create_time + '</li></ul></div></div></a></li>')
                $('.houses-list').append(optNode)
            }
    })
})