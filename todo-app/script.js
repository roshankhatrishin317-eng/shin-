// DOM Elements
const taskInput = document.getElementById('taskInput');
const addBtn = document.getElementById('addBtn');
const taskList = document.getElementById('taskList');
const emptyState = document.getElementById('emptyState');
const taskCount = document.getElementById('taskCount');
const clearCompleted = document.getElementById('clearCompleted');
const filterBtns = document.querySelectorAll('.filter-btn');

// State
let tasks = [];
let currentFilter = 'all';

// Load tasks from localStorage on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    renderTasks();
});

// Event Listeners
addBtn.addEventListener('click', addTask);
taskInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTask();
    }
});

clearCompleted.addEventListener('click', clearCompletedTasks);

filterBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        currentFilter = e.target.dataset.filter;
        
        // Update active filter button
        filterBtns.forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        
        renderTasks();
    });
});

// Functions
function addTask() {
    const text = taskInput.value.trim();
    
    if (text === '') {
        taskInput.focus();
        return;
    }
    
    const task = {
        id: Date.now(),
        text: text,
        completed: false,
        createdAt: new Date().toISOString()
    };
    
    tasks.push(task);
    saveTasks();
    renderTasks();
    
    taskInput.value = '';
    taskInput.focus();
}

function deleteTask(id) {
    tasks = tasks.filter(task => task.id !== id);
    saveTasks();
    renderTasks();
}

function toggleTask(id) {
    const task = tasks.find(task => task.id === id);
    if (task) {
        task.completed = !task.completed;
        saveTasks();
        renderTasks();
    }
}

function clearCompletedTasks() {
    tasks = tasks.filter(task => !task.completed);
    saveTasks();
    renderTasks();
}

function getFilteredTasks() {
    switch(currentFilter) {
        case 'active':
            return tasks.filter(task => !task.completed);
        case 'completed':
            return tasks.filter(task => task.completed);
        default:
            return tasks;
    }
}

function renderTasks() {
    const filteredTasks = getFilteredTasks();
    
    // Clear task list
    taskList.innerHTML = '';
    
    // Show/hide empty state
    if (filteredTasks.length === 0) {
        emptyState.classList.remove('hidden');
        taskList.style.display = 'none';
    } else {
        emptyState.classList.add('hidden');
        taskList.style.display = 'block';
        
        // Render each task
        filteredTasks.forEach(task => {
            const li = document.createElement('li');
            li.className = `task-item ${task.completed ? 'completed' : ''}`;
            li.innerHTML = `
                <input 
                    type="checkbox" 
                    class="checkbox" 
                    ${task.completed ? 'checked' : ''}
                    onchange="toggleTask(${task.id})"
                >
                <span class="task-text">${escapeHtml(task.text)}</span>
                <button class="btn-delete" onclick="deleteTask(${task.id})">Delete</button>
            `;
            taskList.appendChild(li);
        });
    }
    
    // Update task count
    const activeCount = tasks.filter(task => !task.completed).length;
    taskCount.textContent = `${activeCount} task${activeCount !== 1 ? 's' : ''}`;
    
    // Show/hide clear completed button
    const completedCount = tasks.filter(task => task.completed).length;
    clearCompleted.style.display = completedCount > 0 ? 'block' : 'none';
}

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function loadTasks() {
    const savedTasks = localStorage.getItem('tasks');
    if (savedTasks) {
        tasks = JSON.parse(savedTasks);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Make functions available globally for inline event handlers
window.deleteTask = deleteTask;
window.toggleTask = toggleTask;