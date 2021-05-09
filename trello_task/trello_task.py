from trello import TrelloClient
from datetime import date

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

    def list_from_name(self, name: str):
        return {
            "todo": lambda: self.todo_list,
            "inprogress": lambda: self.in_progress_list,
            "done": lambda: self.done_list
        }[name]()

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

    def move_card(self, card_id: str, from_list_name: str, to_list_name: str):
        """
        move_card copies a card from one list to another and deletes the original.
        TODO: figure out how to move the card instead of cloning/deleting
        :param trello_task:
        :param args:
        :return:
        """
        print(f"moving card {card_id} from {from_list_name} to {to_list_name}")

        from_list = self.list_from_name(from_list_name)
        to_list = self.list_from_name(to_list_name)

        # add the date of movement as a comment so we can extract this information as needed.
        to_list.add_card("", source=card_id).comment("MovedAt: " + date.today().strftime("%d/%m/%Y"))
        for c in from_list.list_cards():
            if c.id == card_id:
                c.delete()
                return

    @staticmethod
    def _add_card(trello_list, name: str, **kwargs):
        trello_list.add_card(name, **kwargs)
