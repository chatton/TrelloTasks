# TrelloTasks

Trello Tasks is a small wrapping around py-trello that is designed to maintain 3 lists within a single Trello board to
keep track of `TODO, In Progress, and Done` lists.

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

You can use these bash functions to interact with the application.

```bash
task_type() {
    echo "$(main.py --task-types | fzf | xargs)" 
}

card_id(){
    echo "$(main.py --list ${1} | fzf |  awk '{ print $1 }')"
}


# new task
nt(){
    task_type="todo"
    read -p "Name: " name
    read -p "Description: " desc
    main.py create -t ${task_type} -d "${desc}" -n "${name}"
}

# list tasks
lt(){
    task_type="$(task_type)"
    main.py --list ${task_type}
}

# complete task
ct(){
    card_id="$(card_id inprogress)"
    main.py move --from-list inprogress --to-list "done" --card-id ${card_id}
}

# show all the in progress tasks that need to be do
tasks(){
    main.py --list inprogress
}

# move card from one list to another
mt(){
    from="$(task_type)"
    to="$(task_type)"
    card_id="$(card_id ${from})"
    main.py move --from-list "${from}" --to-list "${to}" --card-id "${card_id}"
}

# start task
st(){
    card_id="$(card_id todo)"
    main.py move --from-list todo --to-list inprogress --card-id ${card_id}
}

standup(){
    main.py --standup
}

```