import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from quizbank import QuestionBank

REVERSE = False


def show_question(title, answers):
    print(title)
    for i, answer in enumerate(answers):
        print(f"{i+1}. {answer}")


def get_answer_index(max_index):
    while True:
        raw = input(">> ")
        if not raw.isdigit():
            print("Пожалуйста, введите число!")
            continue
        index = int(raw) - 1
        if 0 <= index < max_index:
            return index
        print("Некорректный номер ответа!")


def ask_question(data):
    question = data.get_rand_question(reverse=REVERSE, quantity_ans=3)
    if question is None:
        print("Добавьте вопросов!")
        return False

    answers = question.all_answers

    show_question(question.title, answers)
    print("Каков вопрос?" if REVERSE else "Каков ответ?")

    while True:
        index = get_answer_index(len(answers))
        if question.is_right(answers[index]):
            print("Молодец! Ответ верный! \n")
            return True
        print("Ответ неверный! Попробуй снова")


def main_loop(data):
    while ask_question(data):
        if input("Продолжить? (да/нет): ").lower() != 'да':
            break
    print("Игра завершена!")


if __name__ == "__main__":
    main_loop(QuestionBank(path_to_simple="simple.example.json"))