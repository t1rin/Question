import logging
import json
import os
from random import randint, choice, shuffle

from .models import *


logger = logging.getLogger(__name__)


class QuestionsData:
    def __init__(self, path_to_json: str | None = None) -> None:
        self._json_name: str | None = path_to_json

        self._init_groups(data={})
        if path_to_json is not None:
            if not self._is_normal_json():
                self._create_json()
            self._read_json()

    def _init_groups(self, data: dict) -> None:
        self._groups = QuestionGroups(data=data)
        self._data = self._groups.data

    def _is_normal_json(self) -> bool:
        assert self._json_name is not None
        if not os.path.exists(self._json_name):
            return False
        try:
            with open(self._json_name, "r", encoding="utf-8") as json_file:
                data = json.loads(json_file.read())
        except:
            logger.error("Некорректная структура json файла")
            return False
        
        return self._is_normal_data(data)

    def _is_normal_data(self, data: dict) -> bool:
        try: QuestionGroups(data=data)
        except ValidationError:
            return False
        return True

    def _create_json(self) -> None:
        index = 0
        assert self._json_name is not None
        name = self._json_name.split(".")
        while os.path.exists(self._json_name):
            if os.path.exists((str(index)+".").join(name)):
                index += 1
                continue
            os.rename(self._json_name, (str(index)+".").join(name))

        with open(self._json_name, "w", encoding="utf-8") as json_file:
            json_file.write("{}")

        logger.info("Создан новый " + self._json_name)

    def _read_json(self) -> None:
        assert self._json_name is not None
        with open(self._json_name, "r", encoding="utf-8") as json_file:
            data = json.loads(json_file.read())
            self._init_groups(data=data)

    def _update_json(self) -> None:
        assert self._json_name is not None
        with open(self._json_name, "w", encoding="utf-8") as json_file:
            data = json.dumps(self._data, ensure_ascii=False, indent=4)
            json_file.write(data)

    def _merge(self, *dictionaries: dict) -> dict:
        if len(dictionaries) == 1: return dictionaries[0]
        groups_names = set().union(*[set(d.keys()) for d in dictionaries])
        if len(groups_names) == sum([len(i) for i in dictionaries]):
            return dict(((i[0], *i[1]) if isinstance(i[1], list) else (i[0], i[1]))
                        for j in dictionaries for i in j.items())
        new_dicts = {}
        for group_name in groups_names:
            values = []
            for dictionary in dictionaries:
                if group_name in dictionary.keys():
                    values.append(dictionary[group_name])
            if all(isinstance(i, str) for i in values):
                if len(values:=list(set(values))) == 1:
                    new_dicts[group_name] = values[0]
                else:
                    new_dicts[group_name] = values
            elif any(isinstance(i, list) for i in values):
                new_values = []
                for value in values:
                    if isinstance(value, list):
                        new_values += value
                    else:
                        new_values.append(value)
                if len(new_values := list(set(new_values))) == 1:
                    new_dicts[group_name] = new_values[0]
                else:
                    new_dicts[group_name] = new_values
            else:
                new_dicts[group_name] = self._merge(*values)
        return new_dicts

    def add_question(self, group: str, key: str, value: str) -> 'QuestionsData':
        if not self._is_normal_json():
            self._create_json()
        if any(not isinstance(name, str) for name in [group, key, value]):
            logger.error("Ожидается group -> [str], key -> [str], value -> [str]")
            return self
        if group not in self._data.keys():
            self._data[group] = {}

        if key not in self._data[group].keys():
            self._data[group][key] = value
        else:
            values = self._data[group][key]
            if isinstance(values, str):
                if value != values:
                    self._data[group][key] = [values, value]
            else:
                self._data[group][key] = list(set([*values, value]))
        
        if self._json_name:
            self._update_json()

        return self

    def load_data(self, data: dict) -> 'QuestionsData':
        if self._is_normal_data(data):
            new_data = self._merge(self._data, data)
            self._init_groups(data=new_data)
            if self._json_name:
                self._update_json()
        else:
            logger.error("json данные не имеют смысла")
        return self

    def get_groups(self) -> list:
        return list(self._data.keys())
    
    def get_items(self, group_name: str, key_is_main=True) -> list | None:
        if not isinstance(group_name, str):
            logger.error("Ожидается group_name -> [str]")
            return None
        if group_name not in self._data.keys():
            logger.error("Не найдена группа " + group_name)
            return None
        
        if key_is_main:
            return list(self._data[group_name])
        else:
            values = set()
            for value in self._data[group_name].values():
                if isinstance(value, str):
                    values.add(value)
                else:
                    values.update(value)
            return sorted(list(values))
    
    def get_all_data(self) -> dict:
        return self._data

    def get_question(self, group: str, title: str, 
                     key_is_main: bool = True, quentity_items: int = 3) -> tuple | None:
        if not isinstance(quentity_items, int) or quentity_items < 2:
            logger.error("Некорректное количество вариантов ответа")
            return None
        if any(not isinstance(name, str) for name in [title, group]):
            logger.error("Ожидается group -> [str], title -> [str]")
            return None
        if group not in self.get_groups():
            logger.error("Не найдена группа " + group)
            return None

        items_list = self.get_items(group, key_is_main=key_is_main)
        if items_list is None or title not in items_list:
            logger.error("title \"" + title + "\" не найден")
            return None
            
        items = self._data[group]
        keys = [*items.keys()]
        values = [*items.values()]

        main_index = None
        if key_is_main:
            main_index = keys.index(title)
        else:
            for value in values:
                if (isinstance(value, str) and title == value) or \
                    (not isinstance(value, str) and title in value):
                    main_index = values.index(value)
                    break
            else:
                logger.error("Не найдено title")
                return None

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
        if self._data is None or len(self._data) == 0:
            logger.warning("Вопросов нет")
            return None
        
        if group is None:
            group = choice(self.get_groups())

        items = self._data[group]
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
