You can use these bash functions to interact with the application.

```bash

task_type() {
    echo "$(task-trello.py --task-types | fzf | xargs)" 
}

card_id(){
    echo "$(task-trello.py --list ${1} | fzf |  awk '{ print $1 }')"
}


# new task
nt(){
    task_type="todo"
    read -p "Name: " name
    read -p "Description: " desc
    trello-tasks.py create -t ${task_type} -d "${desc}" -n "${name}"
}

# list tasks
lt(){
    task_type="$(task_type)"
    trello-tasks.py --list ${task_type}
}

# complete task
ct(){
    card_id="$(card_id inprogress)"
    trello-tasks.py move --from-list inprogress --to-list "done" --card-id ${card_id}
}

# show all the in progress tasks that need to be do
tasks(){
    trello-tasks.py --list inprogress
}

# move card from one list to another
mt(){
    from="$(task_type)"
    to="$(task_type)"
    card_id="$(card_id ${from})"
    trello-tasks.py move --from-list "${from}" --to-list "${to}" --card-id "${card_id}"
}

# start task
st(){
    card_id="$(card_id todo)"
    trello-tasks.py move --from-list todo --to-list inprogress --card-id ${card_id}
}

standup(){
    trello-tasks.py --standup
}
```