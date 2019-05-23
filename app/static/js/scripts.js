$(document).ready(function () {

    $(".dropdown-trigger").dropdown();
    $('select').formSelect();
    $('.sidenav').sidenav();
    $('.user-tabs').tabs();
    $('.modal').modal({
        startingTop:'50%',
    });
    $('.collapsible').collapsible();


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
    });


    // 发布评论
    $('form.comment-form').submit(function (e) {
        e.preventDefault();
        let r=$(this),
            t=$('ul.comments'),
            n=$('span.comment-num'),
            data=$(this).serialize();
        $.ajax({
            type: 'POST',
            data: data,
            success: function (data) {
                t.prepend(data.html);
                n.text(data.count);
                r.find('input#body').val('');
            }
        })
    });

    // 计划
    let ENTER_KEY = 13;
    let ESC_KEY = 27;

    function display_dashboard() {
        var all_count = $('.item').length;
        if (all_count === 0) {
            $('#dashboard').hide();
        } else {
            $('#dashboard').show();
            $('ul.tabs').tabs();
        }
    }

    function activeM() {            // Materilize组件初始化
        $('.sidenav').sidenav();
        $('ul.tabs').tabs();
        $('.modal').modal();
        $('.tooltipped').tooltip();
        $('.dropdown-trigger').dropdown({
                constrainWidth: false,
                coverTrigger: false
            }
        );
    }

    function remove_edit_input() {
        var $edit_input = $('#edit-item-input');
        var $input = $('#item-input');

        $edit_input.parent().prev().show();
        $edit_input.parent().remove();
        $input.focus();
    }

    function refresh_count() {
        var $items = $('.item');
        var all_count = $items.length;
        var active_count = $items.filter(function () {
            return $(this).data('done') === false;
        }).length;
        var completed_count = $items.filter(function () {
            return $(this).data('done') === true;
        }).length;
        $('#all-count').text(all_count);
        $('#active-count').text(active_count);
        $('#completed-count').text(completed_count);
    }

    function new_item(e) {
        let $input = $('#item-input');
        let value = $input.val().trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $input.focus().val('');
        let url = $input.data('href');
        $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify({'body': value}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                M.toast({html: data.message, classed: 'rounded'});
                $('.items').append(data.html);
                refresh_count();
            },
        });
    }
    // add new item
    $(document).on('keyup', '#item-input', new_item.bind(this));


    function edit_item(e) {
        let $edit_input = $('#edit-item-input');
        let value = $edit_input.val().trim();
        if (e.which !== ENTER_KEY || !value) {      // Enter键
            return;
        }
        $edit_input.val('');
        if (!value) {
            M.toast({html: 'Your todos was empty!'});
            return;
        }
        let url = $edit_input.parent().prev().data('href');
        let id = $edit_input.parent().prev().data('id');
        $.ajax({
            type: 'PUT',
            data: JSON.stringify({'body' : value}),
            url: url,
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                $('#body' + id).html(value);
                $edit_input.parent().prev().data('body', value);
                remove_edit_input();
                M.toast({html: data.message})
            }
        })
    }



    // edit item
    $(document).on('keyup', '#edit-item-input', edit_item.bind(this));

    $(document).on('click', '.done-btn', function () {
        var $input = $('#item-input');

        $input.focus();
        var $item = $(this).parent().parent();
        var $this = $(this);

        if ($item.data('done')) {
            $.ajax({
                type: 'PATCH',
                url: $this.data('href'),
                success: function (data) {
                    $this.next().removeClass('inactive-item');
                    $this.next().addClass('active-item');
                    $this.find('i').text('check_box_outline_blank');
                    $item.data('done', false);
                    M.toast({html: data.message});
                    refresh_count();
                }
            })
        } else {
            $.ajax({
                type: 'PATCH',
                url: $this.data('href'),
                success: function (data) {
                    $this.next().removeClass('active-item');
                    $this.next().addClass('inactive-item');
                    $this.find('i').text('check_box');
                    $item.data('done', true);
                    M.toast({html: data.message});
                    refresh_count();
                }
            })

        }
    });

    // hide and show edit buttons
    $(document).on('mouseenter', '.item', function () {
        $(this).find('.edit-btns').removeClass('hide');
    })
        .on('mouseleave', '.item', function () {
            $(this).find('.edit-btns').addClass('hide');
        });

    // edit item
    $(document).on('click', '.edit-btn', function () {

        let $item = $(this).parent().parent();
        let itemId = $item.data('id');
        let itemBody = $('#body' + itemId).text();
        $item.hide();
        $item.after(' \
                <div class="row card-panel hoverable">\
                <input class="validate" id="edit-item-input" type="text" value="' + itemBody + '"\
                autocomplete="off" autofocus required> \
                </div> \
            ');

        let $edit_input = $('#edit-item-input');

        let strLength = $edit_input.val().length * 2;

        $edit_input.focus();
        $edit_input[0].setSelectionRange(strLength, strLength);

        // Remove edit form when ESC was pressed or focus out.
        $(document).on('keydown', function (e) {
            if (e.keyCode === ESC_KEY) {
                remove_edit_input();
            }
        });

        $edit_input.on('focusout', function () {
            remove_edit_input();
        })
    });

    $(document).on('click', '.delete-btn', function () {
        let $input = $('#item-input');
        let $item = $(this).parent().parent();

        $input.focus();
        $.ajax({
            type: 'DELETE',
            url: $(this).data('href'),
            success: function (data) {
                $item.remove();
                refresh_count();
                M.toast({html: data.message});
            }
        });
    });

    $(document).on('click', '#active-item', function () {
        var $input = $('#item-input');
        var $items = $('.item');

        $input.focus();
        $items.show();
        $items.filter(function () {
            return $(this).data('done');
        }).hide();
    });

    $(document).on('click', '#completed-item', function () {
        var $input = $('#item-input');
        var $items = $('.item');

        $input.focus();
        $items.show();
        $items.filter(function () {
            return !$(this).data('done');
        }).hide();
    });

    $(document).on('click', '#all-item', function () {
        $('#item-input').focus();
        $('.item').show();
    });

    $(document).on('click', '#clear-btn', function () {
        let $input = $('#item-input');
        let $items = $('.item');

        $input.focus();
        $.ajax({
            type: 'DELETE',
            url: $(this).data('href'),
            success: function (data) {
                $items.filter(function () {
                    return $(this).data('done');
                }).remove();
                M.toast({html: data.message, classes: 'rounded'});
                refresh_count();
            }
        });
    });

    // let ENTER_KEY = 13;
    // function new_item(e) {
    //     let $input = $('#item-input');
    //     let value = $input.val().trim();
    //     if (e.which !== ENTER_KEY || !value) {
    //         return;
    //     }
    //     $input.focus().val('');
    //     let url = $input.data('href');
    //     $.ajax({
    //         type: 'POST',
    //         url: url,
    //         data: JSON.stringify({'body': value}),
    //         contentType: 'application/json;charset=UTF-8',
    //         success: function (data) {
    //             $('.items').append(data.html);
    //         }
    //     });
    // }
    // $(document).on('keyup', '#item-input', new_item.bind(this));

})