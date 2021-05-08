import sys
import os
import json

from trello import TrelloClient

CONFIG_PATH = os.path.expanduser("~/.trello-tasks")


class TrelloTask:
    def __init__(self, client: TrelloClient, board_name: str):
        self.client = client
        self.active_board = self._get_board_by_name(board_name)

    def _get_board_by_name(self, name: str):
        return next(board for board in self.client.list_boards() if board.name == name)


def _load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.loads(f.read())


def main() -> int:
    config = _load_config()

    client = TrelloClient(
        api_key=config["api_key"],
        api_secret=config["api_secret"],
        token=config["token"],
        token_secret=config["token_secret"]
    )

    trello_task = TrelloTask(client, config["board"])
    return 0



if __name__ == "__main__":
    sys.exit(main())
