import os, time

from questions import Data
from questions import Question


color_codes = {
    "red": 41,
    "green": 42
}


class App:
    def __init__(self):
        self.height = 100
        self.width = 200

        self._data = Data().load_json()
        self._question = Question()

        self.active_loop = True  #
        self.key_is_main = False 

        self._active_warning = False
        self._index_warning = None
        self._q_warning = 2
         
    def run(self):
        while self.active_loop:
            data_question = self._data.get_rand_question(key_is_main=self.key_is_main)
            self._question.load(data_question)

            if data_question is None:
                self.show_message("Добавьте вопросов!")
                return
            
            right = None
            while not right:
                self.clear_screen()

                self.show_question(self._question.get_title(), 
                                   *self._question.get_answers())

                if self._active_warning:
                    if self._index_warning is None:
                        self._index_warning = 0
                    elif self._index_warning >= self._q_warning:
                        self._active_warning = False
                        self._index_warning = None
                    else:
                        time.sleep(0.08)
                        self.show_flash(color="red", time_=0.12)
                        self._index_warning += 1
                    continue

                try:
                    index = int(self.get_answer(msg="Ответ > ")) - 1
                    if not (0 <= index < len(self._question.get_answers())):
                        raise ValueError
                except ValueError:
                    self.show_warning()
                    continue

                right = self._question.is_right(
                    self._question.get_answers()[index])
                if right:
                    self.show_flash(color="green")
                    self.show_message("✅ Молодец! Ответ верный!")
                else:
                    self.show_flash(color="red")
                    self.show_message("❌ Увы... Ответ неверный, выберите другой")
                self.show_message("\nНажми Enter для продолжения...")
                input()
            
    def show_message(self, msg):
        print(msg)

    def show_question(self, question, *answers):
        print(question)
        for i in range(len(answers)):
            print(f"{i+1}. {answers[i]}")

    def show_flash(self, color="red", time_=0.8):
        self.clear_screen()
        self.update_size()

        for _ in range(self.height):
            print("\033[" + str(color_codes[color]) + "m" + " " * self.width + "\033[0m")

        time.sleep(time_)
        self.clear_screen()

    def show_warning(self):
        self._active_warning = True

    def get_answer(self, msg=None):
        return input(msg) if msg else input()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_size(self):
        tetminal_size = os.get_terminal_size()
        self.height = tetminal_size.lines
        self.width = tetminal_size.columns


if __name__ == "__main__":
    app = App()
    app.run()

