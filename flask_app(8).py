import random
import string
from flask import Flask, render_template, request

app = Flask(__name__)

LETTERS_BIG = string.ascii_uppercase
LETTERS_SMALL = string.ascii_lowercase
NUMBERS = string.digits
SYMBOLS = "~!@#$%^&*:;<=>-?+)(/[]{}_"
SPACE = " "
ALL_CHARS = LETTERS_BIG + LETTERS_SMALL + NUMBERS + SYMBOLS + SPACE


def generate_password(length: int) -> str:
    """Генерирует пароль. Возвращает строку."""
    if length < 5:
        raise ValueError("Длина должна быть не менее 5.")

    password = [
        random.choice(LETTERS_BIG),
        random.choice(LETTERS_SMALL),
        random.choice(NUMBERS),
        random.choice(SYMBOLS),
        SPACE
    ]

    if length > 5:
        password.extend(random.choices(ALL_CHARS, k=length - 5))

    while True:
        random.shuffle(password)
        if password[0] != SPACE and password[-1] != SPACE:
            break

    return "".join(password)


@app.route("/", methods=["GET", "POST"])
def index():
    """Обработчик главной страницы."""
    generated_password = None
    error_message = None

    if request.method == "POST":
        try:
            user_input = request.form.get("length")
            length = int(user_input)

            if length < 5:
                error_message = "Ошибка: длина должна быть не менее 5 символов."
            else:
                generated_password = generate_password(length)

        except (ValueError, TypeError):
            error_message = "Ошибка: пожалуйста, введите целое число."

    return render_template(
        "index.html",
        password=generated_password,
        error=error_message
    )


if __name__ == "__main__":
    app.run(debug=True)