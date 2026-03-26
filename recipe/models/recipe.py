from models.database import db


class Recipe(db.Model):
    """Модель рецепта"""
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)  # В минутах
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, draft, archived
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    # Внешний ключ
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def get_ingredients_list(self):
        """Преобразование строки ингредиентов в список"""
        if self.ingredients:
            return [ing.strip() for ing in self.ingredients.split('\n') if ing.strip()]
        return []

    def get_instructions_list(self):
        """Преобразование инструкций в список"""
        if self.instructions:
            return [inst.strip() for inst in self.instructions.split('\n') if inst.strip()]
        return []

    def __repr__(self):
        return f'<Recipe {self.title}>'