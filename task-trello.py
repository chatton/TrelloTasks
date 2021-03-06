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
    parser.add_argument("--standup", help="Generate standup text for the day", action="store_true")

    sub_parsers = parser.add_subparsers(help='sub-command help')

    # Handle creation of cards
    create_parser = sub_parsers.add_parser("create", help="Create command")
    create_parser.add_argument("-t", "--type", type=str, choices=("todo", "done", "inprogress"))
    create_parser.add_argument("-d", "--description", type=str)
    create_parser.add_argument("-n", "--name", type=str)

    clone_parser = sub_parsers.add_parser("move", help="Move command")
    clone_parser.add_argument("--from-list", type=str, choices=("todo", "done", "inprogress"))
    clone_parser.add_argument("--to-list", type=str, choices=("todo", "done", "inprogress"))
    clone_parser.add_argument("--card-id", type=str)

    parser.add_argument(
        "--task-types", help="List Task Types", action="store_true"
    )

    return parser.parse_args()


def _load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.loads(f.read())


def _generate_standup_text(yesterdays_tasks, todays_tasks):
    standup_text = "#standup\n"
    standup_text += "Y\n"
    for yt in yesterdays_tasks:
        standup_text += "  * " + yt.desc + "\n"

    standup_text += "T\n"
    for tt in todays_tasks:
        standup_text += "  * " + tt.desc + "\n"
    return standup_text


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

    if args.standup:
        yesterdays_tasks = trello_task.get_previous_work_days_completed_tasks()
        todays_tasks = trello_task.in_progress_list.list_cards()
        print(_generate_standup_text(yesterdays_tasks, todays_tasks))
        return 0

    if hasattr(args, "from_list"):
        trello_task.move_card(args.card_id, args.from_list, args.to_list)
        return 0

    if hasattr(args, "name"):
        trello_task.create_card(args.type, args.name, args.description)
        return 0

    if args.list:
        for t in trello_task.list_tasks(args.list):
            print(t)
        return 0

    if args.task_types:
        for t in ("todo", "done", "inprogress"):
            print(t)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
