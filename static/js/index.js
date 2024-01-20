var todo = document.querySelectorAll('#todo .task');
var doing = document.querySelectorAll('#doing .task');
var done = document.querySelectorAll('#done .task');


todo.forEach((task) => {
  task.addEventListener('mouseover', (event) => {
    task.querySelector('.fa-arrow-right').style.visibility = 'visible';
  });
  task.addEventListener('mouseout', (event) => {
    task.querySelector('.fa-arrow-right').style.visibility = 'hidden';
  });
  task.querySelector('.fa-arrow-right').addEventListener('click', (event) => {
  });
});

doing.forEach((task) => {
  task.addEventListener('mouseover', (event) => {
    task.querySelector('.fa-arrow-right').style.visibility = 'visible';
    task.querySelector('.fa-arrow-left').style.visibility = 'visible';
  });
  task.addEventListener('mouseout', (event) => {
    task.querySelector('.fa-arrow-right').style.visibility = 'hidden';
    task.querySelector('.fa-arrow-left').style.visibility = 'hidden';
  });
  task.querySelector('.fa-arrow-right').addEventListener('click', (event) => {
  });
  task.querySelector('.fa-arrow-left').addEventListener('click', (event) => {
  });
});

done.forEach((task) => {
  task.addEventListener('mouseover', (event) => {
    task.querySelector('.fa-arrow-left').style.visibility = 'visible';
  });
  task.addEventListener('mouseout', (event) => {
    task.querySelector('.fa-arrow-left').style.visibility = 'hidden';
  });
  task.querySelector('.fa-arrow-left').addEventListener('click', (event) => {
  });
});
