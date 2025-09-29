from questions import Data
from questions import Question


active_loop = True  # вспомогательная переменная
key_is_main = True  # при значении False вопросы поменяются с ответами
question = None     # объявление имени для будущего экземпляра
data = None         # объявление имени для будущего экземпляра

def show_question(question, *answers):
    print(question)
    for i in range(len(answers)):
        print(f"{i}. {answers[i]}")

def main_loop():
    while active_loop:
        data_question = data.get_rand_question(key_is_main=key_is_main)
        if data_question is None:
            print("Добавьте вопросов!")
            return
        question.load(data_question)
        show_question(question.get_title(), *question.get_answers())
        print("Каков ответ?" if key_is_main else "Каков вопрос?")
        while not question.is_right(question.get_answers()[int(input(">> "))]):
            print("Ответ неверный! Попробуй снова")
        else:
            print("Молодец! Ответ верный! \n")


if __name__ == "__main__":
    data = Data().load_json()
    question = Question()
    while True:
        try:
            main_loop()
        except Exception:
            pass

