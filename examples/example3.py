from quizbank import SimpleQGroups
from quizbank.types import SimpleWrongAnswers, StoredMode


def show(title: str, stored) -> None:
    print(f"\n=== {title} ===")
    for group, modes in stored.data.items():
        questions = modes[StoredMode.QUESTION]
        for q, answers in questions.items():
            right = [a for a, ok in answers if ok]
            wrong = [a for a, ok in answers if not ok]
            print(f"{group} | {q}: верно={right}, неверно={wrong}")


sq = SimpleQGroups()
sq.load_data({
    "Столицы": {
        "Франция": "Париж",
        "Япония": "Токио",
        "Германия": "Берлин",
    }
})

show("Авто", sq.to_stored(fill_missing=2))

wrong: SimpleWrongAnswers = {"Столицы": {"Франция": "Лондон"}}
show("Ручные + автодобивка", sq.to_stored(wrong_answers=wrong, fill_missing=2))