from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.database import db
from models.recipe import Recipe
from sqlalchemy import or_

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')


@recipe_bp.route('/')
@login_required
def list_recipes():
    """Список рецептов с фильтрацией"""
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    status = request.args.get('status', 'active')
    search = request.args.get('search')

    # Базовый запрос
    query = Recipe.query.filter_by(user_id=current_user.id)

    # Применение фильтров
    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if status:
        query = query.filter_by(status=status)
    if search:
        query = query.filter(
            or_(
                Recipe.title.ilike(f'%{search}%'),
                Recipe.description.ilike(f'%{search}%'),
                Recipe.ingredients.ilike(f'%{search}%')
            )
        )

    recipes = query.order_by(Recipe.created_at.desc()).all()

    # Получение уникальных категорий для фильтра
    categories = db.session.query(Recipe.category).distinct().all()
    categories = [c[0] for c in categories]

    # Подсчет статистики
    total_recipes = Recipe.query.filter_by(user_id=current_user.id).count()
    active_recipes = Recipe.query.filter_by(user_id=current_user.id, status='active').count()
    draft_recipes = Recipe.query.filter_by(user_id=current_user.id, status='draft').count()

    return render_template('recipes/list.html',
                           recipes=recipes,
                           categories=categories,
                           total_recipes=total_recipes,
                           active_recipes=active_recipes,
                           draft_recipes=draft_recipes)


@recipe_bp.route('/<int:recipe_id>')
@login_required
def recipe_detail(recipe_id):
    """Просмотр деталей рецепта"""
    recipe = Recipe.query.get_or_404(recipe_id)

    # Проверка прав доступа
    if recipe.user_id != current_user.id and not current_user.is_admin():
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('recipe.list_recipes'))

    return render_template('recipes/detail.html', recipe=recipe)


@recipe_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_recipe():
    """Создание нового рецепта"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        cooking_time = request.form.get('cooking_time')
        difficulty = request.form.get('difficulty')
        category = request.form.get('category')
        status = request.form.get('status', 'draft')

        # Валидация
        if not all([title, description, ingredients, instructions, cooking_time, category]):
            flash('Все обязательные поля должны быть заполнены', 'danger')
        else:
            # Создание рецепта
            recipe = Recipe(
                title=title,
                description=description,
                ingredients=ingredients,
                instructions=instructions,
                cooking_time=int(cooking_time),
                difficulty=difficulty,
                category=category,
                status=status,
                user_id=current_user.id
            )

            db.session.add(recipe)
            db.session.commit()

            flash('Рецепт успешно создан!', 'success')
            return redirect(url_for('recipe.list_recipes'))

    return render_template('recipes/create.html')


@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    """Редактирование рецепта"""
    recipe = Recipe.query.get_or_404(recipe_id)

    # Проверка прав доступа
    if recipe.user_id != current_user.id and not current_user.is_admin():
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('recipe.list_recipes'))

    if request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.description = request.form.get('description')
        recipe.ingredients = request.form.get('ingredients')
        recipe.instructions = request.form.get('instructions')
        recipe.cooking_time = int(request.form.get('cooking_time'))
        recipe.difficulty = request.form.get('difficulty')
        recipe.category = request.form.get('category')
        recipe.status = request.form.get('status')

        db.session.commit()
        flash('Рецепт успешно обновлен!', 'success')
        return redirect(url_for('recipe.recipe_detail', recipe_id=recipe.id))

    return render_template('recipes/edit.html', recipe=recipe)


@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    """Удаление рецепта"""
    recipe = Recipe.query.get_or_404(recipe_id)

    # Проверка прав доступа
    if recipe.user_id != current_user.id and not current_user.is_admin():
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('recipe.list_recipes'))

    db.session.delete(recipe)
    db.session.commit()
    flash('Рецепт успешно удален!', 'success')
    return redirect(url_for('recipe.list_recipes'))