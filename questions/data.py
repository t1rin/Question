import logging
import json
import os
from random import randint, choice, shuffle

logger = logging.getLogger(__name__)


class Data:
    def __init__(self, path_to_json="data.json"):
        self._json_name = path_to_json
        self._data_json = None

        if not self._is_normal_file():
            self._create_json()
        with open(self._json_name, "r", encoding="utf-8") as json_file:
            self._data_json = json.loads(json_file.read())

    def _is_normal_data(self, data: dict) -> bool:
        if not all(isinstance(group, str) for group in data.keys()):
            logger.error("Ожидается наименование группы")
            return False
        for item in data.values():
            if not isinstance(item, dict):
                logger.error("Ожидалось значение по наименованию группы (dict)")
                return False
            for key, value in item.items():
                if isinstance(key, str) and (isinstance(value, str) or isinstance(value, list)):
                    continue
                logger.error("Ожидалось вопрос -> [str]; ответ -> [str | list]")
                return False
        return True

    def _is_normal_file(self) -> bool:
        if not os.path.exists(self._json_name):
            return False
        try:
            with open(self._json_name, "r", encoding="utf-8") as json_file:
                data = json.loads(json_file.read())
        except:
            logger.error("Некорректная структура json файла")
            return False
        
        return self._is_normal_data(data)

    def _create_json(self) -> None:
        index = 0
        name = self._json_name.split(".")
        while os.path.exists(self._json_name):
            if os.path.exists((str(index)+".").join(name)):
                index += 1
                continue
            os.rename(self._json_name, (str(index)+".").join(name))

        with open(self._json_name, "w", encoding="utf-8") as json_file:
            json_file.write("{}")

        logger.info("Создан новый " + self._json_name)

    def _update_json(self) -> None:
        with open(self._json_name, "w", encoding="utf-8") as json_file:
            data = json.dumps(self._data_json, ensure_ascii=False, indent=4)
            json_file.write(data)

    def _recursion_update(self, *dicts):
        if len(dicts) == 1: return dicts[0]
        keys = set().union(*[set(d.keys()) for d in dicts])
        if len(keys) == sum([len(i) for i in dicts]):
            return dict(((i[0], *i[1]) if isinstance(i[1], list) else (i[0], i[1]))
                        for j in dicts for i in j.items())
        new_dicts = {}
        for key in keys:
            values = []
            for d in dicts:
                if key in d.keys():
                    values.append(d[key])
            if all(isinstance(i, str) for i in values):
                if len(values:=list(set(values))) == 1:
                    new_dicts[key] = values[0]
                else:
                    new_dicts[key] = values
            elif any(isinstance(i, list) for i in values):
                new_values = []
                for value in values:
                    if isinstance(value, list):
                        new_values += value
                    else:
                        new_values.append(value)
                if len(new_values := list(set(new_values))) == 1:
                    new_dicts[key] = new_values[0]
                else:
                    new_dicts[key] = new_values
            else:
                new_dicts[key] = self._recursion_update(*values)
        return new_dicts

    def add_data(self, group: str, key: str, value: str) -> 'Data':
        if not self._is_normal_file():
            self._create_json()
        if any(not isinstance(name, str) for name in [group, key, value]):
            logger.error("Ожидается group -> [str], key -> [str], value -> [str]")
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

    def load_json(self, data: dict = {}) -> 'Data':
        logger.warning("С недавнего периода load_json поменял свой функционал (подробнее на https://github.com/t1rin/Question)")
        if self._is_normal_data(data):
            new_data = self._recursion_update(self._data_json, data)
            self._data_json = new_data
            self._update_json()
        else:
            logger.error("json данные не имеют смысла")

    def get_groups(self) -> list:
        return list(self._data_json.keys())
    
    def get_items(self, group: str, key_is_main=True) -> list | None:
        if not isinstance(group, str):
            logger.error("Ожидается group -> [str]")
            return
        if group not in self._data_json.keys():
            logger.error("Не найдена группа " + group)
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
            logger.error("Некорректное количество вариантов ответа")
            return 
        if any(not isinstance(name, str) for name in [title, group]):
            logger.error("Ожидается group -> [str], title -> [str]")
            return 
        if group not in self.get_groups():
            logger.error("Не найдена группа " + group)
            return
        if title not in self.get_items(group, key_is_main=key_is_main):
            logger.error("title \"" + title + "\" не найден")
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
                logger.error("Не найдено title")
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
            logger.warning("Вопросов нет")
            return
        
        if group is None:
            group = choice(self.get_groups())

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
