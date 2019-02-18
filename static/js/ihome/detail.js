function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){

    $(".book-house").show();

//    渲染详情页面
    $.get('/house/my_detail/',function(data){
        if(data.code == '200'){
//            1.轮播图
            for(img in data.data.images){
                var optNode_container = $('<li class="swiper-slide"><img src="/static/imgs/' + data.data.images[img] + '"></li>')
                $('.swiper-wrapper').append(optNode_container)
            }
                var mySwiper = new Swiper ('.swiper-container', {
                    loop: true,
                    autoplay: 2000,
                    autoplayDisableOnInteraction: false,
                    pagination: '.swiper-pagination',
                    paginationType: 'fraction'
                })

            var optNode_price = $('<div class="house-price">￥<span>' + data.data.price + '</span>/晚</div>')
            $('.swiper-container').append(optNode_price)

//            2.房屋标题
            var optNode_header = $('<h2 class="house-title">' + data.data.title + '</h2><div class="landlord-pic"><img src="/static/media/' + data.data.user_avatar + '"></div><h2 class="landlord-name">房东： <span>' + data.data.user_name + '</span></h2>')
            $('.detail-header').append(optNode_header)

//            3.房屋地址
            var optNode_list = $('<ul class="house-info-list text-center"><li>'+ data.data.address +'</li></ul>')
            $('#house_list').append(optNode_list)

//            4.房屋属性
            var optNode_type = $('<li><span class="icon-house"></span><div class="icon-text"><h3>' + data.data.room_count + '</h3><p>房屋面积:' + data.data.acreage + '平米</p> <p>房屋户型:' + data.data.unit + '</p></div></li><li><span class="icon-user"></span><div class="icon-text"><h3>' + data.data.capacity + '</h3></div></li><li><span class="icon-bed"></span><div class="icon-text"><h3>卧床配置</h3><p>' + data.data.beds + '</p></li>')
            $('.house-type').append(optNode_type)

//            5.房间详情
            var optNode_info = $('<ul class="house-info-list"><li>收取押金<span>' + data.data.deposit + '</span></li><li>最少入住天数<span>' + data.data.min_days + '</span></li><li>最多入住天数<span>' + data.data.max_days + '</span></li></ul>')
            $('#house_info').append(optNode_info)

//            6.房屋设施
            for(fac in data.data.facilities){
                var optNode_facility = $('<li><span class="'+ data.data.facilities[fac].css +'"></span>' + data.data.facilities[fac].name + '</li>')
                $('.house-facility-list').append(optNode_facility)
            }

            $('.book-house').attr('href', '/order/booking/' + data.data.id + '')
      }
    })
})