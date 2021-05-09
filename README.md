# TrelloTasks

TrelloTasks is a small wrapping around py-trello that is designed to maintain 3 lists within a single Trello board to
keep track of `TODO, In Progress, and Done` lists.

TrelloTasks can generate a snippet of text which contains information about which tasks were completed on the last working
day and which tasks are to be completed today.

```bash
usage: trello-task [-h] [--list {todo,done,inprogress}] [--standup] [--task-types] {create,move} ...

positional arguments:
  {create,move}         sub-command help
    create              Create command
    move                Move command

optional arguments:
  -h, --help            show this help message and exit
  --list {todo,done,inprogress}
                        List Tasks
  --standup             Generate standup text for the day
  --task-types          List Task Types
```
