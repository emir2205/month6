from datetime import date

from rest_framework.exceptions import ValidationError


def _calculate_age(birthdate: date) -> int:
    today = date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age


def validate_birthdate_for_product_create(request) -> None:
    token_birthdate = request.auth.get("birthdate") if hasattr(request.auth, "get") else None

    if not token_birthdate:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")

    try:
        birthdate = date.fromisoformat(token_birthdate)
    except (TypeError, ValueError):
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")

    if _calculate_age(birthdate) < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")
