from typing import List

from trello import TrelloClient
from datetime import date, timedelta

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

    def create_card(self, task_type: str, name: str, desc: str):
        f = {
            "todo": self.add_todo_card,
            "inprogress": self.add_in_progress_card,
            "done": self.add_done_card
        }[task_type]
        f(name, desc=desc)

    def list_tasks(self, task_type: str) -> List[str]:
        names = []
        if task_type == "todo":
            for card in self.todo_list.list_cards():
                names.append(self._card_str(card))

        if task_type == "inprogress":
            for card in self.in_progress_list.list_cards():
                names.append(self._card_str(card))

        if task_type == "done":
            for card in self.done_list.list_cards():
                names.append(self._card_str(card))
        return names

    def move_card(self, card_id: str, from_list_name: str, to_list_name: str):
        """
        move_card copies a card from one list to another and deletes the original.
        TODO: figure out how to move the card instead of cloning/deleting
        :param card_id: the id of the card to be added
        :param to_list_name: the list the card is currently in
        :param from_list_name: the list the card should be moved to
        :return: None
        """
        print(f"moving card {card_id} from {from_list_name} to {to_list_name}")

        from_list = self.list_from_name(from_list_name)
        to_list = self.list_from_name(to_list_name)

        t = date.today()

        # add the date of movement as a comment so we can extract this information as needed.
        to_list.add_card("", source=card_id).comment(date.today().strftime("%d/%m/%Y"))
        for c in from_list.list_cards():
            if c.id == card_id:
                c.delete()
                return

    def _fetch_completed_tasks_on_day(self, day):
        expected_comment = day.strftime("%d/%m/%Y")
        completed_cards = []
        for card in [c for c in self.done_list.list_cards() if not c.closed]:
            for comment in card.comments:
                if comment["data"]["text"] == expected_comment:
                    completed_cards.append(card)
        return completed_cards

    def get_previous_work_days_completed_tasks(self):
        days_to_check = 7
        count = 0
        today = date.today()
        prev_day = today - timedelta(days=1)
        res = self._fetch_completed_tasks_on_day(prev_day)
        while not res:
            if count >= days_to_check:
                break
            if not res:
                print("No completed tasks found on " + prev_day.strftime("%d/%m/%Y"))

            prev_day = prev_day - timedelta(days=1)
            res = self._fetch_completed_tasks_on_day(prev_day)
            count += 1

        if res:
            print("Found {} completed tasks from {}".format(len(res), prev_day.strftime("%d/%m/%Y")))

        return res

    @staticmethod
    def _add_card(trello_list, name: str, **kwargs):
        trello_list.add_card(name, **kwargs)

    @staticmethod
    def _card_str(card) -> str:
        return f"{card.id} : {card.name} - {card.description}"
