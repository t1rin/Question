from data import Data
from question import Question


active_loop = True
question = None
data = None

def show_question(question, *answers):
    print(question)
    print(*answers, sep="\t|\t")

def main_loop():
    while active_loop:
        data_question = data.get_data(key_is_main=True)
        if data_question is None:
            print("Добавьте вопросов!")
            return
        question.load(data_question)
        show_question(question.get_title(), *question.get_answers())
        print("Каков ответ?")
        while not question.is_right(input(">> ")):
            print("Ответ неверный! Попробуй снова")
        else:
            print("Молодец! Ответ верный! \n")


if __name__ == "__main__":
    data = Data().load_json()
    question = Question()
    main_loop()

