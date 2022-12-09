from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from .. import db
from .models import Task, Category, Comment
from ..account.models import User
from .forms import Taskform, CategoryForm, CommentForm, AssignUserForm

from . import to_do_bp


@to_do_bp.route('/task/create', methods=['GET', 'POST'])
@login_required
def task_create():
    form = Taskform()

    if form.validate_on_submit():

        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data
        category = form.category.data
        task_info = Task(title=title,
                         description=description,
                         deadline=deadline,
                         priority=priority,
                         progress=progress,
                         category_id=category,
                         owner=current_user)
        task_info.users.append(current_user)
        db.session.add(task_info)
        db.session.commit()

        flash(f"Task created: {form.title.data}", category='success')
        return redirect(url_for("to_do.task_create"))

    elif request.method == 'POST':
        flash("Не пройшла валідація з Post", category='warning')
        return redirect(url_for("to_do.task_create"))
    
    return render_template('task_create.html', form=form)

@to_do_bp.route('/task', methods=['GET'])
@login_required
def tasks():

    tasks_ = Task.query.order_by(Task.priority.desc(),
                                 Task.deadline.asc()
                                 ).all()   
    return render_template('tasks.html', tasks=tasks_)

@to_do_bp.route('/task/<int:id>',methods=['GET', 'POST'])
@login_required
def task(id):
    task = Task.query.filter_by(id=id).first()
    task_detail = {
        'Title': task.title,
        'Description': task.description,
        'Created': task.created,
        'Modified': task.modified,
        'Deadline': task.deadline.date(),
        'Priority': task.priority,
        'Progress': task.progress
    }
    form = Taskform()
    form_comment = CommentForm()
    comments = Comment.query.filter_by(task_id=id).all()
    data = {
        'form_comment': form_comment,
        'comments': comments
    }
    return render_template('task.html', task_detail=task_detail,
                           id=task.id,
                           form=form,
                           assigned=task.users,
                           data=data,
                           user=current_user)

@to_do_bp.route('/task/<int:id>/update', methods=['GET', 'POST'])
@login_required
def task_update(id):
    
    form = Taskform()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data

        task = Task.query.filter_by(id=id).first()
        task.title = title
        task.description = description
        task.deadline = deadline
        task.priority = priority
        task.progress = progress
        db.session.add(task)
        db.session.commit()

        flash(f"Task successfully updated", category='success')
        return redirect(url_for("to_do.task", task_id=id))

    elif request.method == 'POST':
        print(form.errors, form.description.data)
        flash("Не пройшла валідація з Post", category='warning')
        return redirect(url_for("to_do.task", task_id=id))

    return render_template('task_update.html', title="Update task", form=form, task_id=id)

@to_do_bp.route('/task/<int:id>/delete', methods=['GET'])
@login_required
def task_delete(id):
    task_ = Task.query.get_or_404(id)
    
    try:
        db.session.delete(task_)
    except:
        db.session.rollback()
    else:
        db.session.commit()
        flash("Task deleted", category='success')
        current_app.logger.info("Task deleted")
    
    return redirect(url_for('tasks.tasks'))


@to_do_bp.route('/categories', methods=['GET'])
@login_required
def categories():
    categories_ = Category.query.all()
    return render_template('categories.html', categories=categories_)

@to_do_bp.route('/category/create', methods=['GET', 'POST'])
@login_required
def category_add():
    form = CategoryForm()
    
    if form.validate_on_submit():
        if current_user.is_authenticated:
            category = Category(name=form.name.data) 

            try:
                db.session.add(category)
            except:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Category added", category='success')
        else:
            return redirect(url_for('account.login'))
  
    
    if request.method == 'POST':
        return redirect(url_for('to_do.categories')) 
    
    return render_template('category_form.html', form=form)


@to_do_bp.route('/category/<int:id>/update', methods=['GET', 'POST'])
@login_required
def category_update(id):
    category_ = Category.query.get_or_404(id)
    
    form = CategoryForm(name=category_.name)
    
    if form.validate_on_submit():
        if current_user.is_authenticated:
            try:
                category_.name = form.name.data
            except:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Category updated", category='success')
                current_app.logger.info("Category updated")
        else:
            return redirect(url_for('account.login'))
  
    if request.method == 'POST':
        return redirect(url_for('to_do.categories', id=category_.id)) 
    
    return render_template('category_form.html', form=form)

@to_do_bp.route('/categories/<int:id>/delete', methods=['GET'])
@login_required
def category_delete(id):
    category_ = Category.query.get_or_404(id)
    
    try:
        db.session.delete(category_)
    except:
        db.session.rollback()
    else:
        db.session.commit()
        flash("Category deleted", category='success')
        current_app.logger.info("Category deleted")
    
    return redirect(url_for('to_do.categories'))


@to_do_bp.route('/task/add_comment/<int:task_id>', methods=['GET', 'POST'])
@login_required
def add_comment(task_id):
    task = current_user.tasks.filter_by(id=task_id).first()
    if not task:
        flash("You cannot add comment to this task", category='warning')
        return redirect(url_for("to_do.task", id=task_id))
    form = CommentForm()
    if form.validate_on_submit():
        text = form.text.data
        comment = Comment(content=text,
                          owner_id=current_user.id,
                          task_id=task_id)
        db.session.add(comment)
        db.session.commit()

        flash(f"Comment successfully added", category='success')
        return redirect(url_for("to_do.task", id=task_id))

    elif request.method == 'POST':
        flash("Не пройшла валідація з Post", category='warning')

    return render_template('comment_form.html', title="Task", task_id=task_id, form=form)


@to_do_bp.route('/task/<int:task_id>/assign/user', methods=['GET', 'POST'])
@login_required
def assign_user_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    form = AssignUserForm()
    if form.validate_on_submit():
        if task.owner_id != current_user.id:
            flash("You cannot assign users to this task", category='warning')
            return redirect(url_for("to_do.task", id=task_id))
        if not request.form.get('email'):
            flash("Fill the email field", category='warning')
            return redirect(url_for("to_do.task", id=task_id))
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("No user with such email", category='warning')
            return redirect(url_for("to_do.task", id=task_id))
        task.users.append(user)
        db.session.add(task)
        db.session.commit()
        flash("Successfully assigned user", category='success')

    elif request.method == 'POST':
        flash("Не пройшла валідація з Post", category='warning')
        return redirect(url_for("to_do.assign_user_task", id=task_id))

    return render_template('assign_user.html', id=task_id, form=form)

@to_do_bp.route('/user/profile/<int:user_id>')
@login_required
def user_profile(user_id):
    user_info = User.query.filter_by(id=user_id).first()
    task_list = user_info.tasks
    return render_template('user.html', user_info=user_info, task_list=task_list)