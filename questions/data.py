from random import randint, choice, shuffle
import json, os


class Data:
    def __init__(self):
        self._json_name = "data.json"
        self._data_json = None

    def _is_exist_json(self) -> bool:
        return os.path.exists(self._json_name)

    def _is_normal_structure_json(self) -> bool:
        try:
            with open(self._json_name, "r", encoding="utf-8") as json_file:
                data = json.loads(json_file.read())
        except: return False
        if not all(isinstance(group, str) for group in data.keys()):
            return False
        for item in data.values():
            if not isinstance(item, dict):
                return False
            for key, value in item:
                if isinstance(key, str) and isinstance(value, str):
                    continue
                return False
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
            data = json.dumps(self._data_json, ensure_ascii=False, indent=4)
            json_file.write(data)

    def load_json(self) -> 'Data':
        if not self._is_exist_json():
            self._create_json()
        if not self._is_normal_structure_json():
            print("error: некорректная структура json файла")
            return
        with open(self._json_name, "r", encoding="utf-8") as json_file:
            self._data_json = json.loads(json_file.read())
        return self

    def add_data(self, group: str, key: str, value: str) -> 'Data':
        if any(not isinstance(name, str) for name in [group, key, value]):
            print("error: ожидается group->str, key->str, value->str")
            return self
        if group not in self._data_json.keys():
            self._data_json[group] = {}

        if key not in self._data_json[group].keys():
            self._data_json[group][key] = value
        else:
            values = self._data_json[group][key]
            if isinstance(values, str):
                self._data_json[group][key] = (values, value)
            else:
                self._data_json[group][key] = (*values, value)
        
        self._update_json()

        return self

    def get_groups(self) -> list:
        return list(self._data_json.keys())
    
    def get_items(self, group: str, key_is_main=True) -> list | None:
        if not isinstance(group, str):
            print("error: ожидается group->str")
            return
        if group not in self._data_json.keys():
            print("error: не найдена группа " + group)
            return
        
        if key_is_main:
            return list(self._data_json[group])
        else:
            values = set()
            for value in self._data_json[group].values():
                if isinstance(value, str):
                    values.add(value)
                else:
                    values.update(value)
            return sorted(list(values))
    
    def get_question(self, group, title, 
                     key_is_main=True, quentity_items=3) -> tuple | None:
        if not isinstance(quentity_items, int) or quentity_items < 2:
            print("error: некорректное количество вариантов ответа")
            return 
        if any(not isinstance(name, str) for name in [title, group]):
            print("error: ожидается group->str, title->str")
            return 
        if group not in self.get_groups():
            print("error: не найдена группа " + group)
            return
        if title not in self.get_items(group, key_is_main=key_is_main):
            print("error: title \"" + title + "\" не найден")
            return
            
        items = self._data_json[group]
        keys = [*items.keys()]
        values = [*items.values()]

        main_index = None
        if key_is_main: main_index = keys.index(title)
        else:
            for value in values:
                if (isinstance(value, str) and title == value) or \
                    (not isinstance(value, str) and title in value):
                    main_index = values.index(value)
                    break
            else:
                print("error: не найдено title")
                return

        indexes = [randint(0, len(items)-1) 
                   for _ in range(quentity_items-1)] + [main_index] # TODO: добавить опред. процент, выше которого правильных ответов быть не должно
        shuffle(indexes)
        
        if key_is_main:
            return (
                group, keys[main_index],
                [(values[indexes[i]] if isinstance(values[indexes[i]], str) 
                 else choice(values[indexes[i]]), 
                 indexes[i] == main_index) for i in range(quentity_items)]
            )
            
        return (
            group,
            values[main_index] if isinstance(values[main_index], str)
            else choice(values[main_index]),
            [(keys[indexes[i]], indexes[i] == main_index)
            for i in range(quentity_items)]
        )


    def get_rand_question(self, group=None, 
                          key_is_main=True, quentity_items=3) -> tuple | None:
        if self._data_json is None or len(self._data_json) == 0:
            print("warning: вопросов нет")
            return
        
        if group is None:
            group = self.get_groups()[0]

        items = self._data_json[group]
        keys = [*items.keys()]
        values = [*items.values()]
        indexes = [randint(0, len(items)-1) 
                   for _ in range(quentity_items)] # TODO: добавить опред. процент, выше которого правильных ответов быть не должно
        
        main_index = choice(indexes)

        if key_is_main:
            return (
                group, keys[main_index],
                [(values[indexes[i]] if isinstance(values[indexes[i]], str) 
                 else choice(values[indexes[i]]), 
                 indexes[i] == main_index) for i in range(quentity_items)]
            )
        
        return (
            group,
            values[main_index] if isinstance(values[main_index], str)
            else choice(values[main_index]), 
            [(keys[indexes[i]], indexes[i] == main_index)
            for i in range(quentity_items)]
        )