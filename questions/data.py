import logging
import os
from random import randint, choice, shuffle, sample

import orjson

from .models import (ValidationError, JSONWrongAnswers,
                     StoredQGroupsModel, JSONQGroupsModel,
                     QItemModel)


logger = logging.getLogger(__name__)


class QuestionBank:
    def __init__(self, path_to_json: str | None = None) -> None:
        self._json_name: str | None = path_to_json
        self._json_cache: bytes | None = None
        
        self._init_groups(data={})
        if path_to_json is not None:
            if not self._is_normal_json():
                self._create_json()
            self._read_json()

    def _init_groups(self, data: dict) -> None:
        self._groups = JSONQGroupsModel(data=data)
        self._data = self._groups.data
        self._invalidate_cache()

    def _is_normal_json(self) -> bool:
        assert self._json_name is not None
        if not os.path.exists(self._json_name):
            return False
        try:
            with open(self._json_name, "rb") as json_file:
                data = orjson.loads(json_file.read())
        except Exception as e:
            logger.error(f"Некорректная структура json файла: {e}")
            return False
        
        return self._is_normal_data(data)

    def _is_normal_data(self, data: dict) -> bool:
        try: JSONQGroupsModel(data=data)
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

        with open(self._json_name, "wb") as json_file:
            json_file.write(orjson.dumps({}))

        logger.info("Создан новый " + self._json_name)

    def _read_json(self) -> None:
        assert self._json_name is not None
        with open(self._json_name, "rb") as json_file:
            data = orjson.loads(json_file.read())
            self._init_groups(data=data)

    def _update_json(self) -> None:
        assert self._json_name is not None
        with open(self._json_name, "wb") as json_file:
            data = orjson.dumps(
                self._data, 
                option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)
            json_file.write(data)
        self._invalidate_cache()

    def _invalidate_cache(self) -> None:
        self._json_cache = None

    def _merge(self, *dictionaries: dict) -> dict:
        if len(dictionaries) == 1:
            return dictionaries[0]
        groups_names = set().union(*[set(d.keys()) for d in dictionaries])
        if len(groups_names) == sum([len(i) for i in dictionaries]):
            return dict((i[0], i[1]) for j in dictionaries for i in j.items())
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

    def add_question(self, group: str, key: str, value: str) -> 'QuestionBank':
        if self._json_name and not self._is_normal_json():
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

    def load_data(self, data: dict) -> 'QuestionBank':
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
        """Получить все данные в виде словаря"""
        return self._data

    def get_all_data_bytes(self) -> bytes:
        """Получить все данные в виде сериализованного JSON (с кэшированием)"""
        if self._json_cache is not None:
            return self._json_cache
        
        self._json_cache = orjson.dumps(
            self._data,
            option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
        )
        return self._json_cache

    def get_all_data_str(self) -> str:
        """Получить все данные в виде JSON строки (с кэшированием)"""
        return self.get_all_data_bytes().decode('utf-8')

    def _choice_value(self, value):
        return value if isinstance(value, str) else choice(value)

    def _building_question(self, group, keys,
                           values, indexes, main_index,
                           key_is_main) -> QItemModel:
        all_answers = []
        right_answers = set()
        if key_is_main:
            title = keys[main_index]
            for idx in indexes:
                answer = self._choice_value(values[idx])
                all_answers.append(answer)
                if idx == main_index:
                    right_answers.add(answer)
        else:
            title = self._choice_value(values[main_index])
            for idx in indexes:
                answer = keys[idx]
                all_answers.append(answer)
                if idx == main_index:
                    right_answers.add(answer)

        return QItemModel(group=group, title=title,
                            right_answers=list(right_answers),
                            all_answers=all_answers)

    def _pick_wrong_indexes(self, quantity: int, main_index: int, count: int) -> list[int]:
        """Уникальные индексы неправильных ответов, не совпадающие с main_index."""
        available = [i for i in range(quantity) if i != main_index]
        if count > len(available):
            logger.warning(
                "Недостаточно уникальных вариантов ответа (нужно %s, доступно %s), "
                "возможны повторы", count, len(available))
            return [choice(available) for _ in range(count)] if available else []
        return sample(available, count)

    def get_question(self, group: str, title: str, 
                     key_is_main: bool = True, quentity_items: int = 3) -> QItemModel | None:
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

        indexes = self._pick_wrong_indexes(len(items), main_index, quentity_items - 1)
        indexes.append(main_index)
        shuffle(indexes)

        return self._building_question(group, keys, values, indexes, main_index, key_is_main)

    def get_rand_question(self, group=None, key_is_main=True,
                          quantity_option=3) -> QItemModel | None:
        if self._data is None or len(self._data) == 0:
            logger.warning("Вопросов нет")
            return None
        
        if group is None:
            group = choice(self.get_groups())

        items = self._data[group]
        quantity_items = len(items)
        count = min(quantity_option, quantity_items)
        if count < quantity_option:
            logger.warning(
                "В группе %s меньше вопросов (%s), чем запрошено вариантов (%s)",
                group, quantity_items, quantity_option)
        keys = [*items.keys()]
        values = [*items.values()]
        indexes = sample(range(quantity_items), count)
        main_index = choice(indexes)

        return self._building_question(group, keys, values,
                                       indexes, main_index, key_is_main)

    def _flatten_answers(self, values: list) -> list[str]:
        """Уникальный список всех правильных ответов группы (пул для дистракторов).
        Строится один раз на группу — O(len(group))."""
        seen: set[str] = set()
        flat: list[str] = []
        for value in values:
            for answer in (value if isinstance(value, list) else (value,)):
                if answer not in seen:
                    seen.add(answer)
                    flat.append(answer)
        return flat

    def _generate_wrong_answers(self, pool: list[str], pool_set: set[str],
                                exclude: set[str], count: int) -> list[str]:
        """Сэмплирует до `count` уникальных ответов из pool, не входящих в exclude"""
        if count <= 0 or not pool:
            return []

        available = len(pool) - len(exclude & pool_set)
        take = min(count, available)
        if take <= 0:
            return []

        buffer_size = min(len(pool), take + len(exclude))
        drawn = sample(pool, buffer_size)
        wrong = [a for a in drawn if a not in exclude][:take]

        if len(wrong) < take:
            wrong = [a for a in pool if a not in exclude][:take]

        return wrong

    def to_stored(self, wrong_answers: JSONWrongAnswers | None = None,
                  fill_missing: int = 3) -> StoredQGroupsModel:
        if not isinstance(fill_missing, int) or fill_missing < 0:
            logger.error("Ожидается fill_missing -> [int >= 0]")
            fill_missing = 0

        if wrong_answers is not None and not self._is_normal_data(wrong_answers):
            logger.error("wrong_answers имеет некорректную структуру, игнорируется")
            wrong_answers = None

        stored: dict[str, dict[str, list[tuple[str, bool]]]] = {}

        for group, items in self._data.items():
            values = list(items.values())
            pool = self._flatten_answers(values)
            pool_set = set(pool)

            group_wrong = wrong_answers.get(group, {}) if wrong_answers else {}
            group_stored: dict[str, list[tuple[str, bool]]] = {}

            for question, value in items.items():
                right = set(value) if isinstance(value, list) else {value}

                explicit = group_wrong.get(question)
                if explicit is not None:
                    wrong = list(dict.fromkeys(
                        explicit if isinstance(explicit, list) else [explicit]))
                    wrong = [a for a in wrong if a not in right]
                else:
                    wrong = []

                if len(wrong) < fill_missing:
                    exclude = right | set(wrong)
                    wrong += self._generate_wrong_answers(
                        pool, pool_set, exclude, fill_missing - len(wrong))

                entries: list[tuple[str, bool]] = [(a, True) for a in right]
                entries += [(a, False) for a in wrong]
                group_stored[question] = entries

            stored[group] = group_stored

        return StoredQGroupsModel(data=stored)