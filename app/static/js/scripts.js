$(document).ready(function () {

    $(".dropdown-trigger").dropdown();
    $('select').formSelect();
    $('.sidenav').sidenav();
    $('.tabs').tabs();
    $('.modal').modal({
        startingTop:'50%',
    });


    // 关闭提醒消息
    $('main').on('click', '.alert', function() {
        $(this).fadeOut(300,);
    });

    // 文章卡片中的点赞
    $("a#react").click(function(){
        let r=$(this),
            b=r.find('#react-btn'),
            n=r.find('#react-num');
        $.ajax({
            url: r.data('href'),
            type: 'POST',
            beforeSend: function(xhr) {
                console.log('before');
                console.log(xhr)
            },
            success: function(data){
                console.log('getting data');
                r.data('reaction_type', data.reaction_type);
                0===data.reaction_type?
                    b.text('favorite_border'):
                    b.text('favorite');
                n.text(data.count);
            },
            error: function (e) {
                console.log('error');
                console.log(e)
            }
        })
    });

    // 文章的收藏功能
    $("a#collect").click(function(){
        let r=$(this),
            b=r.find('#collect-btn'),
            n=r.find('#collect-num');
        $.ajax({
            url: r.data('href'),
            type: 'POST',
            beforeSend: function(xhr) {
                console.log('before');
                console.log(xhr)
            },
            success: function(data){
                console.log('getting data');
                r.data('collection_type', data.collection_type);
                0===data.collection_type?
                    b.text('star_border'):
                    b.text('star');
                n.text(data.count);
            },
            error: function () {
                console.log('error');
                console.log(e)
            },
            complete: function (xhr, m) {
                console.log(m);
                console.log(xhr);
                if (window.location.pathname.indexOf('user') != -1 && r.parents('div#collections')) {
                    r.parents('div.post-card').remove()
                }
            },
        })
    });

    // 文章的删除功能
        $('a#confirm-delete-post').click(function (event) {
        let r=$(this),
            p=r.parents('div.post-card'),
            t=r.parents('div#delete-post'),
            url=r.data('href');
        $.ajax({
            url:url,
            type:'DELETE',
            success: function (data) {
                p.remove();
                console.log(data.message);
            }
        })
    })



})