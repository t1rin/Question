from questions import *

KEY_IS_MAIN = True


def show_question(title, answers):
    print(title)
    for i, answer in enumerate(answers):
        print(f"{i}. {answer}")


def get_answer_index(max_index):
    while True:
        raw = input(">> ")
        if not raw.isdigit() and not (raw.startswith('-') and raw[1:].isdigit()):
            print("Пожалуйста, введите число!")
            continue
        index = int(raw)
        if 0 <= index < max_index:
            return index
        print("Некорректный номер ответа!")


def ask_question(question, data):
    data_question = data.get_rand_question(key_is_main=KEY_IS_MAIN)
    if data_question is None:
        print("Добавьте вопросов!")
        return False

    question.load(data_question)
    answers = question.get_answers()

    show_question(question.get_title(), answers)
    print("Каков ответ?" if KEY_IS_MAIN else "Каков вопрос?")

    while True:
        index = get_answer_index(len(answers))
        if question.is_right(answers[index]):
            print("Молодец! Ответ верный! \n")
            return True
        print("Ответ неверный! Попробуй снова")


def main_loop(question, data):
    while ask_question(question, data):
        if input("Продолжить? (да/нет): ").lower() != 'да':
            break
    print("Игра завершена!")


if __name__ == "__main__":
    main_loop(Question(), QuestionsData("data.example.json"))