# Task state API
- [Task state API](#task-state-api)
  - [Description](#description)
  - [The workflow of the task state:](#the-workflow-of-the-task-state)
  - [Prerequisites](#prerequisites)
  - [Endpoints](#endpoints)
    - [`GET /tasks`](#get-tasks)
    - [`GET /tasks/:id`](#get-tasksid)
    - [`POST /tasks/:id`](#post-tasksid)
    - [`PUT /tasks/:id`](#put-tasksid)
    - [`DELETE /tasks/:id`](#delete-tasksid)
  - [Tools & Technologies used 🛠](#tools--technologies-used-)
  - [Installation & Quick Start](#installation--quick-start)
  - [Testing](#testing)

## Description

A simple restfull Api powered by Flask and SQLALchemy, to
allow the user to do normal CRUD operation on tasks + changing state
based on API action with respect to a task state machine

## The workflow of the task state:

![Capture](https://user-images.githubusercontent.com/51873396/146055831-633353f5-d0fe-4ed7-9bd4-70592c5d1f53.PNG)


The task can not move from draft to done, can not move from active or done to draft, and can not
move from archived backward. But task can move from any state to archive.

## Prerequisites
Install requisite python packages and modules then you can use the command

```python
pip install -r requirements.txt
```

## Endpoints

### `GET /tasks`

to get all the tasks in the db

**Response**

`200 OK` on success

```json
{
  "task_id": 1,
  "task_title": "first task",
  "task_state": "draft"
}
```

### `GET /tasks/:id`

to get a single task with specific id

**Response to GET /tasks/1**

- `404 Not Found` if the task does not exist
- `200 OK` on success

```json
{
  "task_id": 1,
  "task_title": "first task",
  "task_state": "draft"
}
```

### `POST /tasks/:id`

**Arguments**

- `"task_title":string` represents the title of the task
- `"task_state":string` a represents the state of the task

**Response**

- `409 conflict` if the task id not unique
- `201 Created` on success

```json
{
  "task_id": 2,
  "task_title": "second task",
  "task_state": "done"
}
```

### `PUT /tasks/:id`

**Arguments**

- `"task_title":string` represents the title of the task
- `"task_state":string` a represents the state of the task

**Response**

- `404 Not Found` if the task does not exist
- `409 conflict` if the state not valid
- `200 OK` on success

```json
{
  "task_id": 2,
  "task_title": "second task updated",
  "task_state": "archived"
}
```

### `DELETE /tasks/:id`

**Response**

- `404 Not Found` if the task does not exist
- `204 No Content` on success

## Tools & Technologies used 🛠

- python programming language
- flask
- sql alchemy
- sqlite db
- docker

## Installation & Quick Start

Init the default SQLite database:

```
$> python Api.py -i
```

Run the development server

```
$> python Api.py -r
```

## Testing

To run unittest classes simply run them with nose:
```
python api_test.py
```
