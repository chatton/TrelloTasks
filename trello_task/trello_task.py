from trello import TrelloClient

DESIRED_LISTS = ("TODO", "In Progress", "Done")


class TrelloTask:
    def __init__(self, client: TrelloClient, board_name: str):
        self.client = client
        self.active_board = self._get_board_by_name(board_name)
        self._ensure_lists()

    def _get_board_by_name(self, name: str):
        return next(board for board in self.client.list_boards() if board.name == name)

    def _get_list_by_name(self, name: str):
        return next(trello_list for trello_list in self.active_board.list_lists() if
                    trello_list.name == name and not trello_list.closed)

    @property
    def todo_list(self):
        return self._get_list_by_name("TODO")

    @property
    def in_progress_list(self):
        return self._get_list_by_name("In Progress")

    @property
    def done_list(self):
        return self._get_list_by_name("Done")

    def _ensure_lists(self):
        open_trello_lists = [trello_list for trello_list in self.active_board.list_lists() if not trello_list.closed]
        list_names = [tl.name for tl in open_trello_lists]
        for list_name in DESIRED_LISTS:
            if list_name not in list_names:
                self.active_board.add_list(name=list_name)
                continue

    def add_todo_card(self, name: str, **kwargs):
        return self._add_card(self.todo_list, name, **kwargs)

    def add_in_progress_card(self, name: str, **kwargs):
        return self._add_card(self.in_progress_list, name, **kwargs)

    def add_done_card(self, name: str, **kwargs):
        return self._add_card(self.done_list, name, **kwargs)

    @staticmethod
    def _add_card(trello_list, name: str, **kwargs):
        trello_list.add_card(name, **kwargs)
