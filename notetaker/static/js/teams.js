import { getCSRFToken } from "./csrf.js"

document.addEventListener('DOMContentLoaded', () => {
    const deleteBtn = document.querySelectorAll('.delete_team')
    const csrf = getCSRFToken()

    deleteBtn.forEach(button => {
        button.addEventListener('click', function() {
            if (!window.confirm("Are you sure you want to delete?")) {
                return
            }

            const teamId = this.dataset.teamId

            fetch(`/team/${teamId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf,
                    'Content-Type': 'application/json'
                  }        
            })
            .then(response => response.json())
            .then(data => {
                const teamCard = document.getElementById(`team-${teamId}`)
                if (teamCard) { 
                    teamCard.remove();
                }
            })
            .catch(error => {
                console.log('error is: ', error)
            })
        })
    })
})