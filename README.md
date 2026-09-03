🌐 **RUSSIAN** | [ENGLISH](README_EN.md)

# Описание

<div align="center">
  <img src="src/1.png">
</div>

Модуль `quizbank` для создания и хранения наборов вопросов с ответами, объединённых в группы. Поддерживает два формата данных:

- **simple** — упрощённый: `{"Группа": {"Вопрос": "Ответ"}}` (или список ответов), удобен для ручного заполнения json;
- **stored** — полный: каждый ответ помечен как правильный/неправильный, поддерживается обратный режим (вопрос и ответ меняются местами) и автогенерация недостающих неправильных вариантов.

# Использование

## `QuestionBank`

```python
from quizbank import QuestionBank

bank = QuestionBank(
    path_to_simple="simple.json",
    path_to_stored="stored.json",
)
```

- `path_to_simple` — путь к JSON файлу в simple-формате;
- `path_to_stored` — путь к JSON файлу в stored-формате.

Оба параметра необязательны. Если указан `path_to_simple`, данные при инициализации автоматически конвертируются и сохраняются в stored-хранилище.

<details>
<summary>методы класса <u>QuestionBank</u></summary>
<p>

#### — метод `load_simple_json`

Загружает json файл simple-формата

```python
bank.load_simple_json("simple.json")
```

#### — метод `load_simple_data`

Загружает новые данные из словаря simple-формата (объединяются с уже имеющимися)

```python
bank.load_simple_data({
    "Набор4": {"Вопрос1": "Ответ1", "Вопрос2": ["Ответ2", "Ответ2.1"]}
})
```

#### — метод `add_question`

Добавляет один вопрос напрямую в stored-хранилище с явным указанием правильных и неправильных ответов

```python
bank.add_question(
    group="Набор1",
    title="Вопрос1",
    right_answers=["Ответ1"],
    wrong_answers=["Ответ2", "Ответ3"],
)
```

#### — метод `get_groups`

Возвращает список всех групп

```python
groups = bank.get_groups()
```

#### — метод `get_question`

Возвращает конкретный вопрос группы

```python
question = bank.get_question(
    group="Набор1",
    title="Вопрос1",
    quantity_ans=5,
)
```

Вернёт `QItem` для вопроса `"Вопрос1"` из группы `"Набор1"` с пятью вариантами ответа

#### — метод `get_rand_question`

Возвращает случайный вопрос

```python
question = bank.get_rand_question(
    group="Набор1",
    quantity_ans=5,
)
```

Если `group` не задан — вопрос выбирается из случайной группы

#### — метод `get_qitems`

Возвращает все вопросы группы

```python
items = bank.get_qitems(group="Набор1")
```

#### — метод `get_all_data_str` / `get_all_data_bytes`

Возвращает все данные stored-хранилища сериализованными в JSON (строкой или байтами)

```python
raw = bank.get_all_data_str()
```

</p>
</details>

## `QItem`

Отдельно взятый вопрос с вариантами ответов; создаётся не напрямую, а через `get_question` / `get_rand_question` / `get_qitems`

```python
question = bank.get_rand_question(group="Набор1")
```

<details>
<summary>свойства и методы <u>QItem</u></summary>
<p>

#### — свойство `title`

Заголовок вопроса

```python
question.title
```

#### — свойство `group`

Наименование группы вопроса

```python
question.group
```

#### — свойство `right_answers`

Список правильных ответов к вопросу

```python
question.right_answers
```

#### — свойство `wrong_answers`

Список неправильных ответов к вопросу

```python
question.wrong_answers
```

#### — свойство `all_answers`

Все ответы к вопросу (правильные + неправильные)

```python
question.all_answers
```

#### — метод `is_right`

Проверяет правильность выбранного ответа

```python
question.is_right(answer)
```

</p>
</details>

# Примеры

Примеры в `/examples`