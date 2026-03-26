document.addEventListener('DOMContentLoaded', function() {
    // Автоматическое скрытие flash сообщений через 5 секунд
    setTimeout(function() {
        const flashMessages = document.querySelectorAll('.alert');
        flashMessages.forEach(function(message) {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        });
    }, 5000);

    // Обработка форм удаления - ОДИН РАЗ
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(form => {
        // Удаляем любые предыдущие обработчики
        form.onsubmit = null;

        // Добавляем новый обработчик
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Предотвращаем стандартную отправку

            // Получаем текст подтверждения
            let confirmMessage = 'Вы уверены?';
            if (this.dataset.confirm) {
                confirmMessage = this.dataset.confirm;
            } else {
                // Для рецептов - получаем название из ближайшего контейнера
                const recipeTitle = this.closest('.recipe-card')?.querySelector('h3')?.textContent;
                if (recipeTitle) {
                    confirmMessage = `Удалить рецепт "${recipeTitle.trim()}"?`;
                }
            }

            // Показываем подтверждение
            if (confirm(confirmMessage)) {
                this.submit(); // Отправляем форму
            }
        });
    });

    // Подсказки для форм
    const inputs = document.querySelectorAll('input[required], textarea[required], select[required]');
    inputs.forEach(input => {
        input.addEventListener('invalid', function() {
            this.classList.add('invalid');
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('invalid')) {
                this.classList.remove('invalid');
            }
        });
    });
});