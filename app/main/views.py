from datetime import datetime
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response, jsonify
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from .. import db
from ..models import Role, User, Permission, Post, Comment, Tag, Item
from ..decorators import admin_required, permission_required
from ..utils import generate_tags


@main.route('/', methods=['GET', 'POST'])
@main.route('/all', methods=['GET', 'POST'])
def index():
    form=PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=request.form['body'],
                    author=current_user._get_current_object())
        tagstring = request.form['tags']
        if tagstring:
            tags = [generate_tags(tagname) for tagname in tagstring.split(',')]
            post.tags = tags
        db.session.add(post)
        db.session.commit()
        return jsonify(html=render_template('_post.html', post=post))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination, endpoint='.index', title='全部')


@main.route('/mines', methods=['GET', 'POST'])
@login_required
def mines():
    form=PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=request.form['body'],
                    author=current_user._get_current_object())
        tagstring = request.form['tags']
        if tagstring:
            tags = [generate_tags(tagname) for tagname in tagstring.split(',')]
            post.tags = tags
        db.session.add(post)
        db.session.commit()
        return jsonify(html=render_template('_post.html', post=post))
    page = request.args.get('page', 1, type=int)
    query = current_user.posts
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination, endpoint='.mines', title='我的')


@main.route('/updates', methods=['GET', 'POST'])
@login_required
def updates():
    form=PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=request.form['body'],
                    author=current_user._get_current_object())
        tagstring = request.form['tags']
        if tagstring:
            tags = [generate_tags(tagname) for tagname in tagstring.split(',')]
            post.tags = tags
        db.session.add(post)
        db.session.commit()
        return jsonify(html=render_template('_post.html', post=post))
    page = request.args.get('page', 1, type=int)
    query = current_user.followed_posts
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination, endpoint='.updates', title="关注")


@main.route('/tag')
@main.route('/tag/<string:tagname>')
def tag(tagname=None):
    taglist = Tag.query.all()
    pagination = None
    posts = None
    if tagname:
        tag = Tag.query.filter_by(name=tagname).first()
        page = request.args.get('page', 1, type=int)
        pagination = tag.posts.order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        posts = pagination.items
    return render_template('tag.html', taglist=taglist, tagname=tagname, posts=posts, pagination=pagination)


@main.route('/recommended')
def recommended():
    Post.ranks()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.rank.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('recommended.html', posts=posts, pagination=pagination, endpoint='.recommended')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, current_time=datetime.utcnow())


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user, current_time=datetime.utcnow())


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=request.form['body'],
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        count = post.comments.count()
        flash('Your comment has been published.')
        return jsonify(html=render_template('_comment.html', comment=comment, post=post),
                       count=count,
                       message='fuck you')
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', post=post, form=form, comments=comments)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        tagstring = form.tags.data
        post.body = form.body.data
        if tagstring:
            tags = [generate_tags(tagname) for tagname in tagstring.split(',')]
            post.tags = tags
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    form.tags.data = post.tagstring
    return render_template('edit_post.html', form=form, current_time=datetime.utcnow())


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


# 点赞、收藏及删除
@main.route('/collect/<post_id>', methods=['POST'])
@login_required
def collect(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if current_user.is_collecting(post):
        current_user.uncollect(post)
        db.session.commit()
        return jsonify(count=post.collectors.count(), collection_type=0)
    current_user.collect(post)
    db.session.commit()
    return jsonify(count=post.collectors.count(), collection_type=1)


@main.route('/react/<post_id>', methods=['POST'])
@login_required
def react(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if current_user.is_liking(post):
        current_user.unlike(post)
        db.session.commit()
        return jsonify(count=post.likers.count(), reaction_type=0)
    current_user.like(post)
    db.session.commit()
    return jsonify(count=post.likers.count(), reaction_type=1)


@main.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return jsonify(message='done')

@main.route('/delete_comment/<int:id>', methods=['DELETE'])
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    db.session.delete(comment)
    db.session.commit()
    post=Post.query.filter_by(id=comment.post_id).first()
    count=post.comments.count()
    return jsonify(count=count)


@main.route('/app')
@login_required
def app():
    all_count = Item.query.with_parent(current_user).count()
    active_count = Item.query.with_parent(current_user).filter_by(done=False).count()
    completed_count = Item.query.with_parent(current_user).filter_by(done=True).count()
    return render_template('_todo.html', items=current_user.items,
                           all_count=all_count, active_count=active_count, completed_count=completed_count)


@main.route('/items/new', methods=['POST'])
@login_required
def new_item():
    data = request.get_json()
    print(data)
    if data is None or data['body'].strip() == '':
        return jsonify(message='Invalid item body'), 400
    item = Item(body=data['body'], author=current_user._get_current_object())
    db.session.add(item)
    db.session.commit()
    return jsonify(html=render_template('_item.html', item=item), message='+1')


@main.route('/item/<int:item_id>/edit', methods=['PUT'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message='Permission denied.'), 403

    data =request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='Invalid item body.'), 400
    item.body = data['body']
    db.session.commit()
    return jsonify(message='Item updated.')


@main.route('/item/<int:item_id>/toggle', methods=['PATCH'])
@login_required
def toggle_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message='Permission denied.'), 403

    item.done = not item.done
    db.session.commit()
    return jsonify(message='Item toggled.')


@main.route('/item/<int:item_id>/delete', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message='Permission denied.'), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify(message='Item deleted.')


@main.route('/item/clear', methods=['DELETE'])
@login_required
def clear_items():
    items = Item.query.with_parent(current_user).filter_by(done=True).all()
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return jsonify(message='All clear!')

