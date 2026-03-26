from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.database import db
from models.user import User
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    """Управление пользователями"""
    users = User.query.order_by(User.created_at.desc()).all()

    # Подсчет статистики
    total_users = User.query.count()
    admin_users = User.query.filter_by(role='admin').count()
    regular_users = User.query.filter_by(role='user').count()

    return render_template('admin/users.html',
                           users=users,
                           total_users=total_users,
                           admin_users=admin_users,
                           regular_users=regular_users)


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Редактирование пользователя"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.role = request.form.get('role')

        # Смена пароля (если указан)
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)

        db.session.commit()
        flash('Пользователь успешно обновлен!', 'success')
        return redirect(url_for('admin.manage_users'))

    return render_template('admin/edit_user.html', user=user)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Удаление пользователя"""
    user = User.query.get_or_404(user_id)

    # Нельзя удалить самого себя
    if user.id == current_user.id:
        flash('Вы не можете удалить свою собственную учетную запись', 'danger')
        return redirect(url_for('admin.manage_users'))

    db.session.delete(user)
    db.session.commit()
    flash('Пользователь успешно удален!', 'success')
    return redirect(url_for('admin.manage_users'))