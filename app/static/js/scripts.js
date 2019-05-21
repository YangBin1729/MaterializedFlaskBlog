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

    // 删除文章
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
    });

    // 提交文章
    $('form.post_form').submit(function (e) {
        let r=$(this),
            t=$('ul.posts'),
            data=$(this).serialize();
        $.ajax({
            type: 'POST',
            data: data,
            success: function (data) {
                t.prepend(data.html);
                r.find('input#tags,textarea#body').each(function() {$(this).val('')});
            }
        });
        e.preventDefault();
    });

    // 删除评论
    $('a.delete-comment').click(function () {
        let r=$(this),
            t=r.parents('li.comment'),
            n=$('span.comment-num'),
            url= r.data('href');
        $.ajax({
            url:url,
            type:'DELETE',
            success: function (data) {
                t.remove();
                n.text(data.count)
            }
        })

    })

    // 增加评论


})