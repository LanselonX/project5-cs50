import { getCSRFToken } from "./csrf.js"

document.addEventListener('DOMContentLoaded', () => {
    const userDiv = document.getElementById('user-task-div')
    const teamDiv = document.getElementById('team-task-div')
    const infoDiv = document.getElementById('index-info')
    const containerDiv = document.getElementById('main-container')
    
    function fetchDataTask(url, callback) {
        const csrfToken = getCSRFToken()
        fetch(url, {
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(callback)
        .catch(error => console.log("error is: ", error))
    }

    function renderTask(data) {
        containerDiv.style.display = 'none'
        infoDiv.style.display = 'block'
        infoDiv.innerHTML = `
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header text-center">
                                <h5 class="card-title">${data.title}</h5>
                            </div>
                            <div class="card-body">
                                <img src="${data.image}" alt="Task Image" class="img-fluid">
                                <p class="card-text">${data.description}</p>
                            </div>
                            <div class="card-footer">
                                <button id="close" class="btn btn-primary">Close</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    }

    if(teamDiv) {
        teamDiv.addEventListener('click', (event) => {
            const taskElem = event.target.closest('.card.h-100.shadow-sm')
            const taskId = taskElem.getAttribute('data-task-id')
            const teamId = taskElem.getAttribute('data-team-id')

            if(taskId && teamId) {
                fetchDataTask(`/team/${teamId}/task/${taskId}`, renderTask)
            }
        })
    }

    if(userDiv) {
        userDiv.addEventListener('click', (event) => {
            const taskElem = event.target.closest('.card.h-100.shadow-sm')
            const taskId = taskElem.getAttribute('data-task-id')
            
            if(event.target.classList.contains('delete-task')) {
                if (!confirm('Are you sure you want to delete?')){
                    return
                }
                const cardInfo = document.getElementById('card-info') 
                if(taskId) {
                    fetchDataTask(`/task/${taskId}/delete/`, () => {
                        const deleteButton = cardInfo.querySelector('.delete-task')
                        if(deleteButton) deleteButton.remove()
                        cardInfo.remove()
                    })
                }
                return
            }

            if(taskId) {
                fetchDataTask(`/task/${taskId}/`, renderTask)
            }
        })
    }

    infoDiv.addEventListener('click', (event) => {
        if (event.target.matches('#close')) {
            infoDiv.style.display = 'none'
            containerDiv.style.display = 'block'
        }
    })
})
