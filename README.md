# Описание

<div align="center">
  <img src="src/2.png">
</div>


Пару скриптов для создания тестов с вопросами и ответами

# Использование

В файле `data.json` хранятся вопросы и ответы, расформированные по группам (ответов может быть несколько). С помощью модуля `questions` можно создавать целые опросники всего в несколько десятков строк кода в `main.py`

> Пример этого приведен в `/examples`

## Модуль `questions`

### класс QuestionBank

\- отвечает за хранение данных о всех вопросах

```python
# Инициализация:
data = QuestionBank(path_to_json="my_json.json")
```

загрузка данных из файла `my_json.json`. Если `path_to_json` не указан, то работа с json файлом произоводится не будет

<details>
<summary>методы класса <u>QuestionBank</u></summary>
<p>

#### — метод `load_data`

позволяет загрузить новые данные из словаря

```python
data = QuestionBank()

data_dict = {"Набор4": {"Вопрос1": "Ответ1", "Вопрос2": "Ответ2"}}
data.load_data(data_dict)
```

#### — метод `add_question`

позволяет добавлять вопросы (поддерживается только по отному вопросу и ответу за раз)

```python
data = QuestionBank()
data.add_question(
  group="Набор4",
  key="Вопрос1",
  value="Ответ1"
)
```

#### — метод `get_groups`

позволяет получить список всех групп

```python
data = QuestionBank()
groups = data.get_groups()
```

#### — метод `get_items`

позволяет получить элементы группы

```python
data = QuestionBank()
items = data.get_items(group="Набор1")
```

получим элементы группы `Набор1`

#### — метод `get_all_data`

позволяет получить все данные

```python
data = QuestionBank()
all_data = data.get_all_data()
```


#### — метод `get_question`

позволяет получить вопрос из файла json

```python
data = QuestionBank()
question = data.get_guestion(
  group="Набор1",
  title="Вопрос1",
  quentity_items=5
)
```

получим вопрос `Вопрос1` из группы `Набор1` с количеством вариантов ответа равным пяти

#### — метод `get_rand_question`

позволяет получить случайный вопрос из файла json

```python
data = QuestionBank()
question = data.get_rand_question(
  group="Набор1",
  quentity_items=5
)
```

получим случайный вопрос из группы `"Набор1"` с количеством вариантов ответа равным пяти (если `group` не задан, вопрос будет выбран из случайной группы)

#### — метод `to_stored`

позволяет получить данные в формате `StoredQuestionGroups`

```python
data = QuestionBank()
stored = data.to_stored(
  wrong_answers={"Набор1": {"Вопрос1": ["Ответ2", "Ответ3"]}},
  fill_missing=3
)
```

получим `StoredQuestionGroups`, где для каждого вопроса собраны правильные и неправильные ответы; `wrong_answers` задаёт неправильные ответы вручную (необязательно), `fill_missing` — минимальное количество неправильных ответов на вопрос (недостающие подбираются автоматически)

</details>
</p>

### класс QItem

\- отвечает за отдельно взятый вопрос

```python
# Инициализация:
question = QItem()

# или

data = QuestionBank(path_to_json="my_json.json")
question = data.data.get_question(...)

# или

data = QuestionBank(path_to_json="my_json.json")
question = data.data.get_rand_question(...)
```

<details>
<summary>свойства и методы <u>Question</u></summary>
<p>

#### — свойство `title`

заголовок вопроса

```python
question.title
```

#### — свойство `group`

наименование группы вопроса

```python
question.group
```

#### — свойство `answers`

список всех ответов к вопросу

```python
question.answers
```

#### — свойство `right_answers`

список правильных ответов к вопросу

```python
question.right_answers
```

#### — метод `is_right`

позволяет проверить правильность выбранного ответа (`answer`)

```python
question.is_right(answer)
```

</details>
</p>

# Примеры:

примеры в `/examples`