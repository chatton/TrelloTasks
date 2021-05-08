#!/usr/bin/env python

import sys
import os
import json
import argparse

from trello import TrelloClient

from trello_task.trello_task import TrelloTask

CONFIG_PATH = os.path.expanduser("~/.trello-tasks")


def _parse_args():
    parser = argparse.ArgumentParser(prog='trello-task')
    parser.add_argument(
        "--list", help="List Tasks", type=str, choices=("todo", "done", "inprogress")
    )

    return parser.parse_args()


def _load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.loads(f.read())


def _list_tasks(trello_task: TrelloTask, task_type: str):
    if task_type == "todo":
        for card in trello_task.todo_list.list_cards():
            print(_card_str(card))

    if task_type == "inprogress":
        for card in trello_task.done_list.list_cards():
            print(_card_str(card))

    if task_type == "done":
        for card in trello_task.in_progress_list.list_cards():
            print(_card_str(card))


def _card_str(card) -> str:
    return f"{card.id}: {card.name} - {card.description}"


def main() -> int:
    config = _load_config()

    client = TrelloClient(
        api_key=config["api_key"],
        api_secret=config["api_secret"],
        token=config["token"],
        token_secret=config["token_secret"]
    )

    trello_task = TrelloTask(client, config["board"])

    args = _parse_args()
    _list_tasks(trello_task, args.list)

    return 0


if __name__ == "__main__":
    sys.exit(main())
