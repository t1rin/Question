


class Question:
    def __init__(self, title=None, answer=[], *answers):
        self._data = {
            "title": title,
            "right_answers": answer,
            "all_answers": answers
        }
    
    def load(self, data: tuple):
        right_answers, all_answers = [], []
        for answer, right in data[1]:
            all_answers.append(answer)
            if right: 
                right_answers.append(answer)
        self._data["title"] = data[0]
        self._data["right_answers"] = right_answers
        self._data["all_answers"] = all_answers
    
    def get_title(self):
        return self._data["title"]
    
    def get_answers(self):
        return self._data["all_answers"]
    
    def is_right(self, answer: str):
        return answer in self._data["right_answers"]
    

    


    