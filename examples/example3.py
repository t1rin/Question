from quizbank import QuestionBank
from quizbank.types import SimpleWrongAnswers


def show(title: str, stored) -> None:
    print(f"\n=== {title} ===")
    for group, questions in stored.data.items():
        for q, answers in questions.items():
            right = [a for a, ok in answers if ok]
            wrong = [a for a, ok in answers if not ok]
            print(f"{group} | {q}: верно={right}, неверно={wrong}")


qd = QuestionBank()
qd.add_question("Столицы", "Франция", "Париж")
qd.add_question("Столицы", "Япония", "Токио")
qd.add_question("Столицы", "Германия", "Берлин")

show("Авто", qd.to_stored(fill_missing=2))

wrong: SimpleWrongAnswers = {"Столицы": {"Франция": "Лондон"}}
show("Ручные + автодобивка", qd.to_stored(wrong_answers=wrong, fill_missing=2))
