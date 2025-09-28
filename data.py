
import json, os

from random import randint, choice



class Data:
    def __init__(self):
        self._json_name = "data.json"
        self._data_json = None

    def _is_normal_json(self) -> bool:
        if not os.path.exists(self._json_name):
            return False
        ... # TODO: добавить условия
        return True     

    def _create_json(self) -> None:
        
        index = 0
        name = self._json_name
        while os.path.exists(name):
            if os.path.exists(name+str(index)):
                index += 1
                continue
            os.rename(name, name+str(index))

        with open(self._json_name, "w", encoding="utf-8") as json_file:
            json_file.write("{}")

    def _update_json(self) -> None:
        with open(self._json_name, "w", encoding="utf-8") as json_file:
            data = json.dump(self._data_json)
            json_file.write(data)

    def load_json(self) -> 'Data':
        if not self._is_normal_json():
            self._create_json()
        with open(self._json_name, "r", encoding="utf-8") as json_file:
            self._data_json = json.loads(json_file.read())
        return self

    def add_data(self, key: str, value: str) -> 'Data':
        if not isinstance(key, str) or not isinstance(value, str):
            print("error: ожидается key->str, value->str")
            return
        data = self._data_json[key]
        if key not in self._data_json.keys():
            self._data_json[key] = value
        else:
            if isinstance(data, str):
                self._data_json[key] = (data, value)
            else:
                self._data_json[key] = (*data, value)
        
        self._update_json

        return self

    def get_data(self, key_is_main=True, quentity_items=3) -> tuple | None:
        if self._data_json is None or len(self._data_json) == 0:
            print("warning: вопросов нет")
            return

        indexes = [randint(0, len(self._data_json)-1) 
                   for _ in range(quentity_items)]
        keys = [*self._data_json.keys()]
        values = [*self._data_json.values()]
        main_index = choice(indexes)

        if key_is_main:
            return (
                keys[main_index],
                [(values[indexes[i]] if isinstance(values[indexes[i]], str) 
                 else choice(values[indexes[i]]), 
                 indexes[i] == main_index) for i in range(quentity_items)]
            )
        
        return (
            values[main_index] if isinstance(values[main_index], str)
            else choice(values[main_index]),
            [(keys[indexes[i]], indexes[i] == main_index)
            for i in range(quentity_items)]
        )
    
