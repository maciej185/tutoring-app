class LessonAPIHandler {

    static CSRFToken = getCookie('csrftoken')

    static baseURL = "http://127.0.0.1:8000"
    static getUpdateLessonsAbsenceEndpointURL = (pk) => `/lessons/absence/update/${pk}`

    constructor() {
        this.absenceBtns = document.querySelectorAll("div.absence-btn")
        this.presenceBtns = document.querySelectorAll("div.presence-btn")

        this.absenceBtns.forEach(absenceBtn => absenceBtn.addEventListener("click", this.getUpdateLessonsAbsenceClickListener(true).bind(this)))
        this.presenceBtns.forEach(presenceBtn => presenceBtn.addEventListener("click", this.getUpdateLessonsAbsenceClickListener(false).bind(this)))
    }
    
    getUpdateLessonsAbsenceClickListener(absence) {
        return function(e) {
            (async function() {
                const currentBtn = e.currentTarget
                const lessonPK = currentBtn.dataset.lesson
                const finalURL = LessonAPIHandler.baseURL + LessonAPIHandler.getUpdateLessonsAbsenceEndpointURL(lessonPK)
                const updateLessonAbsenseResponse = await fetch(
                    finalURL,
                    {
                        method: "PUT",
                        headers: {
                            'Content-Type':'application/json',
                            'X-CSRFToken': LessonAPIHandler.CSRFToken
                        },
                        body: JSON.stringify(
                            {
                                absence: absence
                            }
                        )
                    }
                )
                const errorDiv = currentBtn.parentNode.querySelector("div.lesson-left-status-main-entry-errors")
                if (updateLessonAbsenseResponse.status == 200) {
                    errorDiv.style.display = 'none'
                    const otherButton = absence ? currentBtn.parentNode.querySelector("div.presence-btn") : currentBtn.parentNode.querySelector("div.absence-btn")
                    otherButton.style.display = 'block'
                    currentBtn.style.display = 'none'
                } else {
                    errorDiv.innerHTML = 'There was an error.'
                    errorDiv.style.display = "block"
                }
            }).bind(this)()
        }.bind(this)
    }
}

const lesson_api_handler = new LessonAPIHandler()