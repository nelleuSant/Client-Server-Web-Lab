
// ========================================
// 1. Elementos da página
// ========================================

const taskForm = document.getElementById("task-form");
const titleInput = document.getElementById("title");
const descriptionInput = document.getElementById("description");
const taskList = document.getElementById("task-list");
const emptyMessage = document.getElementById("empty-message");

const API_URL = "/api/tasks";


// ========================================
// 2. Comunicação com a API
// ========================================

async function requestAPI(url, options = {}) {
    const response = await fetch(url, options);

    // Trata respostas sem conteúdo, como DELETE com HTTP 204.
    if (response.status === 204) {
        return null;
    }

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Não foi possível realizar a operação.");
    }

    return data;
}


// ========================================
// 3. Listar tarefas
// ========================================

async function loadTasks() {
    try {
        const data = await requestAPI(API_URL);

        // Aceita uma lista direta ou um objeto com a propriedade tasks.
        const tasks = Array.isArray(data) ? data : data.tasks;

        if (!Array.isArray(tasks)) {
            throw new Error("Formato de resposta da API não reconhecido.");
        }

        renderTasks(tasks);

    } catch (error) {
        showMessage(`Erro ao carregar tarefas: ${error.message}`);
    }
}


// ========================================
// 4. Renderizar tarefas na página
// ========================================

function renderTasks(tasks) {
    taskList.replaceChildren();

    if (tasks.length === 0) {
        showMessage("Nenhuma tarefa cadastrada.");
        return;
    }

    tasks.forEach(task => {
        const card = document.createElement("article");
        card.className = "task-card";

        const title = document.createElement("h3");
        title.textContent = task.title;

        const description = document.createElement("p");
        description.textContent = task.description || "Sem descrição.";

        const status = document.createElement("span");
        status.className = "task-status";
        status.textContent =
            task.status === "completed" ? "Concluída" : "Pendente";

        const actions = document.createElement("div");
        actions.className = "task-actions";

        const completeButton = document.createElement("button");
        completeButton.type = "button";
        completeButton.textContent =
            task.status === "completed" ? "Reabrir" : "Concluir";

        completeButton.addEventListener("click", () => {
            toggleTaskStatus(task);
        });

        const editButton = document.createElement("button");
        editButton.type = "button";
        editButton.textContent = "Editar";

        editButton.addEventListener("click", () => {
            editTask(task);
        });

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.textContent = "Excluir";

        deleteButton.addEventListener("click", () => {
            deleteTask(task.id);
        });

        actions.append(
            completeButton,
            editButton,
            deleteButton
        );

        card.append(
            title,
            description,
            status,
            actions
        );

        taskList.appendChild(card);
    });
}


// ========================================
// 5. Cadastrar tarefa
// ========================================

taskForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const task = {
        title: titleInput.value.trim(),
        description: descriptionInput.value.trim()
    };

    if (!task.title) {
        alert("Informe o título da tarefa.");
        return;
    }

    try {
        await requestAPI(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(task)
        });

        taskForm.reset();
        await loadTasks();

    } catch (error) {
        alert(`Erro ao cadastrar tarefa: ${error.message}`);
    }
});


// ========================================
// 6. Atualizar tarefa
// ========================================

async function editTask(task) {
    const newTitle = prompt("Novo título:", task.title);

    if (newTitle === null) return;

    const newDescription = prompt(
        "Nova descrição:",
        task.description || ""
    );

    if (newDescription === null) return;

    if (!newTitle.trim()) {
        alert("O título não pode ficar vazio.");
        return;
    }

    try {
        await requestAPI(`${API_URL}/${task.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: newTitle.trim(),
                description: newDescription.trim()
            })
        });

        await loadTasks();

    } catch (error) {
        alert(`Erro ao atualizar tarefa: ${error.message}`);
    }
}


// ========================================
// 7. Concluir ou reabrir tarefa
// ========================================

async function toggleTaskStatus(task) {
    const newStatus =
        task.status === "completed" ? "pending" : "completed";

    try {
        await requestAPI(`${API_URL}/${task.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                status: newStatus
            })
        });

        await loadTasks();

    } catch (error) {
        alert(`Erro ao atualizar status: ${error.message}`);
    }
}


// ========================================
// 8. Excluir tarefa
// ========================================

async function deleteTask(taskId) {
    const confirmed = confirm(
        "Tem certeza que deseja excluir esta tarefa?"
    );

    if (!confirmed) return;

    try {
        await requestAPI(`${API_URL}/${taskId}`, {
            method: "DELETE"
        });

        await loadTasks();

    } catch (error) {
        alert(`Erro ao excluir tarefa: ${error.message}`);
    }
}


// ========================================
// 9. Mensagens da interface
// ========================================

function showMessage(message) {
    taskList.replaceChildren();

    const paragraph = document.createElement("p");
    paragraph.id = "empty-message";
    paragraph.textContent = message;

    taskList.appendChild(paragraph);
}


// ========================================
// 10. Inicialização
// ========================================

// Carrega as tarefas assim que a página é aberta.
loadTasks();
