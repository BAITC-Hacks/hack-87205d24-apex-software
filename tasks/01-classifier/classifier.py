"""Классификация обращений по простым правилам без внешних зависимостей."""

from pathlib import Path
import sys


def normalize_text(text):
    """Убираем различия в регистре, буквах е/ё и количестве пробелов."""
    return " ".join(text.lower().replace("ё", "е").split())


def classify_message(message):
    """Возвращаем категорию: справка, жалоба или другое."""
    text = normalize_text(message)

    # Проблема важнее вопросительной формы или просьбы выполнить действие.
    complaint_keywords = (
        "пропал", "не работает", "неисправ", "сломал", "проблем",
        "жалоб", "холодная", "холодную", "холодное", "очередь", "очереди",
        "нет интернета", "нет wi-fi", "нет wifi", "нет вай-фай",
        "отсутствует интернет", "плохое обслуживание", "грубят",
    )
    if any(keyword in text for keyword in complaint_keywords):
        return "жалоба"

    # Явные просьбы проверяем до информационных тем (например, справок).
    action_keywords = (
        "записаться", "запишите", "записать меня", "хочу консультацию",
        "перенесите", "отмените", "исправьте", "оформите", "выдайте",
    )
    if any(keyword in text for keyword in action_keywords):
        return "другое"

    information_keywords = (
        "как получить", "где найти", "справк", "расписан", "парковк",
        "информаци", "подскажите",
    )
    question_starts = (
        "где ", "как ", "когда ", "куда ", "какой ", "какая ",
        "какие ", "во сколько ",
    )
    if text.startswith(question_starts) or any(
        keyword in text for keyword in information_keywords
    ):
        return "справка"

    return "другое"


def generate_reply(message, category):
    """Подбираем черновик ответа с учётом категории и темы обращения."""
    text = normalize_text(message)

    if category == "жалоба":
        if "столов" in text or "еда" in text:
            return (
                "Здравствуйте! Спасибо, что сообщили о ситуации в столовой. "
                "Передадим информацию ответственным сотрудникам для проверки."
            )
        if any(word in text for word in ("wi-fi", "wifi", "вай-фай", "интернет")):
            return (
                "Здравствуйте! Спасибо, что сообщили о проблеме с Wi-Fi. "
                "Передадим информацию технической службе для проверки связи."
            )
        return (
            "Здравствуйте! Спасибо, что сообщили о проблеме. "
            "Передадим информацию ответственным сотрудникам для проверки."
        )

    if category == "справка":
        if "справк" in text:
            return (
                "Здравствуйте! Порядок получения справки можно уточнить "
                "в учебном отделе вашего учебного заведения."
            )
        if "парковк" in text:
            return (
                "Здравствуйте! Расположение гостевой парковки можно уточнить "
                "у администрации. Укажите, пожалуйста, нужный корпус."
            )
        return (
            "Здравствуйте! Поможем вам с необходимой информацией. "
            "Уточните, пожалуйста, детали вашего запроса."
        )

    if "консультац" in text:
        return (
            "Здравствуйте! Для записи на консультацию уточните, пожалуйста, "
            "специалиста и удобное время. Возможность записи нужно подтвердить."
        )
    return (
        "Здравствуйте! Спасибо за обращение. "
        "Передадим ваш запрос ответственному сотруднику."
    )


def main():
    messages_path = Path(__file__).resolve().parent / "messages.txt"
    try:
        messages = [
            line.strip()
            for line in messages_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except (OSError, UnicodeError) as error:
        sys.exit(f"Не удалось прочитать messages.txt в кодировке UTF-8: {error}")

    if not messages:
        sys.exit("Файл messages.txt не содержит обращений.")

    for number, message in enumerate(messages, start=1):
        category = classify_message(message)
        if number > 1:
            print("\n" + "-" * 50 + "\n")
        print(f"Обращение {number}:")
        print(message)
        print(f"Категория: {category}")
        print(f"Ответ: {generate_reply(message, category)}")


if __name__ == "__main__":
    main()
