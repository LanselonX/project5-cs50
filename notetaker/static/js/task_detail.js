import { getCSRFToken } from "./csrf.js"

document.addEventListener('DOMContentLoaded', () => {
    const modalBody = document.getElementById('modal-invitation-link')
    const openModalButton = document.querySelector('[data-bs-target="#exampleModal"]')
    const copyBtn = document.getElementById('copy-btn')
    const mainDiv = document.getElementById("task-container")
    const infoDiv = document.getElementById("task-info")
    const csrf = getCSRFToken()

    openModalButton.addEventListener('click', () => {
        fetch(createInvitationUrl, {
          headers: {
            'X-CSRFToken': csrf,
            'Content-Type': 'application/json'
          }
        })
        .then(response => response.json())
        .then(data => {
          modalBody.innerHTML = `<input type="text" class="form-control" id="invitationLink" value="${data.invitation_link}" readonly />`
        })
        .catch(error => {
            console.log(error, "error of Open Modal Button")
        })
    })

    copyBtn.addEventListener('click', async () => {
      const invitationInput = document.getElementById('invitationLink')
      if (invitationInput) {
        try {
          await navigator.clipboard.writeText(invitationInput.value)
        } catch (err) {
          console.log('error: ', err)
        }
      } else {
        console.log('error')
      }
    })

    mainDiv.addEventListener('click', (event) => {
      const taskElem = event.target.closest(".task-elem")
      const taskId = taskElem.getAttribute("data-task-id")
      const optionsHtml = document.getElementById('members-options').innerHTML

      if(event.target.classList.contains('mark-done')) {
        fetch(`/task/${taskId}/mark_done/`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrf,
              'Content-Type': 'application/json'
            }
          })
        .then(response => response.json())
        .then(data => {
            const doneButton = taskElem.querySelector('.mark-done')
            if (doneButton) doneButton.remove()
            taskElem.remove()
            location.reload()
        })
        .catch(error => {
            console.log("Error:", error)
        })
        return
      }

      if(event.target.classList.contains('delete-task')) {
        fetch(`/task/${taskId}/delete/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrf,
            'Content-Type': 'application/json'
          }
        })
        .then(response => response.json())
        .then(data => {
          const deleteButton = taskElem.querySelector('.task-delete')
          if (deleteButton) deleteButton.remove()
          taskElem.remove()
          location.reload()
        })
        .catch(error => {
          consol.log("error is: ", error)
        })
        return
      }

      mainDiv.style.display = 'none'

      fetch(`/team/${teamId}/task/${taskId}/`, {
        headers: {
          'X-CSRFToken': csrf,
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        infoDiv.style.display = 'block'
        infoDiv.innerHTML = `
          <div class="container mt-4">
              <div class="card">
                  <div class="card-header text-center">
                      <h5 class="card-title text-dark fw-bold">${data.title}</h5>
                  </div>
                  <div class="card-body">
                      ${data.image ? `<img src="${data.image}" class="card-img-top img-fluid rounded-3" alt="Task Image">` : ''}
                      <p class="card-text">${data.description}</p>                              
                      <div class="mb-3">
                          <label for="assignTo" class="form-label fw-bold">Assign to:</label>
                          <select id="assignTo" class="form-select">
                            ${optionsHtml}
                          </select>
                      </div>
                      <button id="assignBtn" class="btn btn-success w-100">Assign</button>
                  </div>
              </div>
          </div>
        `
        document.getElementById("assignBtn").addEventListener('click', () => {
          const selectedUser = document.getElementById("assignTo").value
          assignToTask(teamId, taskId, selectedUser)
        })
      })
      .catch(error => {
        console.log("error is: " ,error)
      })
    })

    function assignToTask(teamId, taskId, userId) {
      fetch(`/team/${teamId}/task/${taskId}/assign/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrf,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId }),
      })
      .then(response => response.json())
      .then(data => {
        infoDiv.style.display = 'none'
        mainDiv.style.display = 'block'
        location.reload()
      })
      .catch(error => {
        console.log("It's error of assign to task", error)
      })
    }
})