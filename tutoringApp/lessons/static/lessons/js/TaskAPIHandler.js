class TaskAPIHandler {

    static CSRFToken = getCookie('csrftoken')
    static baseURL = "http://127.0.0.1:8000"
    static getUpdateTaskEndpointURL = (pk) => `/lessons/task/update/${pk}`

    constructor() {
        this.approveBtns = document.querySelectorAll("div.solution-approve")
        this.rejectBtns = document.querySelectorAll("div.solution-reject")

        this.approveBtns.forEach(approveBtn => approveBtn.addEventListener("click", this.getBtnClickListener("approve").bind(this)))
        this.rejectBtns.forEach(rejectBtn => rejectBtn.addEventListener("click", this.getBtnClickListener("reject").bind(this)))
    }

    getStatusDiv(status) {
        return `<div class="lesson-left-tasks-main-task-header-text-status status_green">
                    Done
                </div>` ? status == "accepted" : `<div class="lesson-left-tasks-main-task-header-text-status status_red">
                            Solution pending
            </div>`
    }

    getBtnClickListener(status) {
         return function(e) {
            (async function() {
                const parentDiv = e.currentTarget.parentNode
                const solutionPK = parentDiv.dataset.solution
                const finalURL = TaskAPIHandler.baseURL + TaskAPIHandler.getUpdateTaskEndpointURL(solutionPK)
                const updateTaskResponse = await fetch(
                    finalURL,
                    {
                        method: "PUT",
                        headers:{
                            'Content-Type':'application/json',
                            'X-CSRFToken': TaskAPIHandler.CSRFToken
                        },
                        body: JSON.stringify({
                            "status": status == "approve" ? 1 : -1
                        })
                    }
                )
                if (updateTaskResponse.status == 200) {
                    const errorDiv = parentDiv.parentNode.parentNode.querySelector("div.lesson-left-tasks-main-task-student_solution-errors")
                    const statusDiv = errorDiv.parentNode.parentNode.querySelector("div.lesson-left-tasks-main-task-header-text-status")
                    const approveBtn = parentDiv.querySelector("div.solution-approve")
                    const rejectBtn = parentDiv.querySelector("div.solution-reject")
                    if (status == "approve") {
                        errorDiv.style.display = "none"
                        approveBtn.style.color = "var(--bluegreen-medium)"
                        rejectBtn.style.color = "gray"
                        statusDiv.setAttribute("class", "lesson-left-tasks-main-task-header-text-status status_green")
                        statusDiv.innerHTML = "Done"
                    } else {
                        errorDiv.style.display = "none"
                        approveBtn.style.color = "gray"
                        rejectBtn.style.color = "var(--gray-red-medium)"
                        statusDiv.setAttribute("class", "lesson-left-tasks-main-task-header-text-status status_red")
                        statusDiv.innerHTML = "Solution dismissed"
                    }
                } else {
                    const errorDiv = parentDiv.parentNode.parentNode.querySelector("div.lesson-left-tasks-main-task-student_solution-errors")
                    errorDiv.style.display = "block"
                    errorDiv.innerHTML = "There was an error."
                }
            }).bind(this)()
         }.bind(this)
    }

}

const task_api_handler = new TaskAPIHandler()