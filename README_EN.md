🌐 [RUSSIAN](README.md) | **ENGLISH**

# Description

<div align="center">
  <img src="src/1.png">
</div>

The `quizbank` module is designed to create and store sets of questions with answers, organized into groups. It supports two data formats:

- **simple** — simplified: `{"Group": {"Question": "Answer"}}` (or a list of answers), convenient for manually populating JSON files;
- **stored** — full: each answer is marked as correct or incorrect; supports reverse mode (the question and answer are swapped) and automatic generation of missing incorrect options.

# Usage

## `QuestionBank`

```python
from quizbank import QuestionBank

bank = QuestionBank(
    path_to_simple="simple.json",
    path_to_stored="stored.json",
)
```

- `path_to_simple` — path to a JSON file in the simple format;
- `path_to_stored` — path to a JSON file in the stored format.

Both parameters are optional. If `path_to_simple` is specified, the data is automatically converted and saved to the stored data file during initialization.

<details>
<summary><u>QuestionBank</u> class methods</summary>
<p>

#### — `load_simple_json` method

Loads a JSON file in the simple format.

```python
bank.load_simple_json("simple.json")
```

#### — `load_simple_data` method

Loads new data from a dictionary in the simple format. The data is merged with the existing data.

```python
bank.load_simple_data({
    "Set4": {"Question1": "Answer1", "Question2": ["Answer2", "Answer2.1"]}
})
```

#### — `add_question` method

Adds a single question directly to the stored data file, with the correct and incorrect answers specified explicitly.

```python
bank.add_question(
    group="Set1",
    title="Question1",
    right_answers=["Answer1"],
    wrong_answers=["Answer2", "Answer3"],
)
```

#### — `get_groups` method

Returns a list of all groups.

```python
groups = bank.get_groups()
```

#### — `get_question` method

Returns a specific question from a group.

```python
question = bank.get_question(
    group="Set1",
    title="Question1",
    quantity_ans=5,
)
```

Returns a `QItem` for `"Question1"` from the `"Set1"` group with five answer options.

#### — `get_rand_question` method

Returns a random question.

```python
question = bank.get_rand_question(
    group="Set1",
    quantity_ans=5,
)
```

If `group` is not specified, the question is selected from a random group.

#### — `get_qitems` method

Returns all questions in a group.

```python
items = bank.get_qitems(group="Set1")
```

#### — `get_all_data_str` / `get_all_data_bytes` methods

Returns all data from the stored data file serialized as JSON, either as a string or as bytes.

```python
raw = bank.get_all_data_str()
```

</p>
</details>

## `QItem`

A single question with answer options. It is not created directly; instead, it is obtained through `get_question`, `get_rand_question`, or `get_qitems`.

```python
question = bank.get_rand_question(group="Set1")
```

<details>
<summary><u>QItem</u> properties and methods</summary>
<p>

#### — `title` property

The question title.

```python
question.title
```

#### — `group` property

The name of the question's group.

```python
question.group
```

#### — `right_answers` property

A list of correct answers for the question.

```python
question.right_answers
```

#### — `wrong_answers` property

A list of incorrect answers for the question.

```python
question.wrong_answers
```

#### — `all_answers` property

All answers for the question, including both correct and incorrect answers.

```python
question.all_answers
```

#### — `is_right` method

Checks whether the selected answer is correct.

```python
question.is_right(answer)
```

</p>
</details>

# Examples

Examples are available in `/examples`.
