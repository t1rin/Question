


class Question:
    def __init__(self, title=None, answer=None, *answers):
        self._data = {
            "title": title,
            "answer": answer,
            "answers": answers
        }
    
    def load(self, data: tuple):
        self._data["title"] = data[0]
        answers = []
        for answer, right in data[1]:
            answers.append(answer)
            if right:
                self._data["answer"] = answer
        self._data["answers"] = answers
    
    def get_title(self):
        return self._data["title"]
    
    def get_answers(self):
        return self._data["answers"]
    
    def is_right(self, answer: str):
        return self._data["answer"] == answer
    

    


    