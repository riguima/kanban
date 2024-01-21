function deleteTask(task){
  tasks.forEach((task_json) => {
    if (task_json.id == task.querySelector('.task__id').innerHTML){
      fetch(task_url, {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: task_json.id, token}),
      }).then((response) => {
        task.remove();
      });
    }
  })
}


function onMouseOver(task){
  if (task.parentElement.id !== 'todo'){
    task.querySelector('.fa-arrow-left').style.visibility = 'visible';
  }
  if (task.parentElement.id !== 'done'){
    task.querySelector('.fa-arrow-right').style.visibility = 'visible';
  }
  task.querySelector('.fa-trash').style.visibility = 'visible';
}


function onMouseOut(task){
  task.querySelector('.fa-arrow-left').style.visibility = 'hidden';
  task.querySelector('.fa-arrow-right').style.visibility = 'hidden';
  task.querySelector('.fa-trash').style.visibility = 'hidden';
}


const TASKS_STATUS = ['todo', 'doing', 'done'];


function moveTaskToRight(task){
  tasks.forEach((task_json) => {
    if (task_json.id == task.querySelector('.task__id').innerHTML){
      task_json.status = TASKS_STATUS[TASKS_STATUS.findIndex(status => status == task.parentElement.id) + 1];
      task_json.token = token;
      updateTask(task, task_json);
    }
  });
}


function moveTaskToLeft(task){
  tasks.forEach((task_json) => {
    if (task_json.id == task.querySelector('.task__id').innerHTML){
      task_json.status = TASKS_STATUS[TASKS_STATUS.findIndex(status => status == task.parentElement.id) - 1];
      task_json.token = token;
      updateTask(task, task_json);
    }
  });
}


function updateTask(task, task_json){
  task.querySelector('.fa-trash').style.visibility = 'hidden';
  task.querySelector('.fa-arrow-right').style.visibility = 'hidden';
  task.querySelector('.fa-arrow-left').style.visibility = 'hidden';
  fetch(task_url, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(task_json),
  }).then((response) => {
    document.querySelector(`#${task_json.status}`).appendChild(task);
    addEventListeners();
  });
}


function addEventListeners(){
  let all_tasks = document.querySelectorAll('.task');
  all_tasks.forEach((task) => {
    task.querySelector('.fa-trash').addEventListener('click', event => deleteTask(task));
    task.addEventListener('mouseover', event => onMouseOver(task));
    task.addEventListener('mouseout', event => onMouseOut(task));
    task.querySelector('.fa-arrow-right').addEventListener('click', event => moveTaskToRight(task));
    task.querySelector('.fa-arrow-left').addEventListener('click', event => moveTaskToLeft(task));
  })
}

addEventListeners();
