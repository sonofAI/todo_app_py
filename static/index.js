const title = document.getElementById("title");
const newTodo = document.getElementById("new-todo");
const addBtn = document.getElementById("add");
const todosContainer = document.getElementById("todos");

function addTodoItem(todo) {
	const newItem = document.createElement("div");
	newItem.classList.add("todo-items");
	newItem.innerHTML = `<input type="checkbox" class="checkboxes"> <p>${newTodo.value}</p> <button class="del"><i class="fa-solid fa-trash"></i></button>`;
	todosContainer.appendChild(newItem);
	newTodo.value = "";
	newTodo.focus();
}

function saveTodo() {
	const todo_title = newTodo.value.trim();
	const doc_title = title.value.trim();
	if (!todo_title) return;

	const todo = { todo_title, doc_title };
	fetch("/todos", {
		method: "POST",
		headers: {"Content-Type": "application/json"},
		body: JSON.stringify(todo)
	})
	.then((response) => response.json())
	.then((newTodo) => {
		addTodoItem(newTodo);
	})
	.catch((error) => console.error(error));
}

title.addEventListener("focusout", function () {
	let titleName = localStorage.getItem("titleName") || "";
    titleName = title.value;
    localStorage.setItem("titleName", titleName);
})

addBtn.addEventListener("click", saveTodo);

document.addEventListener("click", function(event) {
    if (event.target.classList.contains("checkboxes")) {
        if (event.target.parentElement.classList.contains("checked")) {
			fetch("/check", {
				method: "POST",
				headers: {"Content-Type": "application/json"},
				body: JSON.stringify({"status": "unchecked", "checked_item": event.target.parentElement.innerText})
			})
			.then(response => response.json())
        	.catch(error => console.error(error));
			event.target.parentElement.classList.remove("checked");
        }
        else {
			fetch("/check", {
				method: "POST",
				headers: {"Content-Type": "application/json"},
				body: JSON.stringify({"status": "checked", "checked_item": event.target.parentElement.innerText})
			})
			.then(response => response.json())
        	.catch(error => console.error(error));
			event.target.parentElement.classList.add("checked");
        }
    }
    else if (event.target.classList.contains("del")) {
        let todo = event.target.parentElement.textContent.slice(0, -1).trim();
        fetch("/todos", {
            method: 'DELETE',
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify(todo)
        })
        .then(response => response.json())
        .catch(error => console.error(error));
        event.target.parentElement.remove();
    }
});