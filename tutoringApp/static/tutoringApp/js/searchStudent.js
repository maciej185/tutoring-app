class SearchStudentHandler {
    static subjectSelect = document.querySelector("select#header-left-search-subject")
    static subjectSelectOptions = SearchStudentHandler.subjectSelect.querySelectorAll("option")
    static firstNameInput = document.querySelector("input#header-left-search-first_name")
    static lastNameInput = document.querySelector("input#header-left-search-last_name")

    static searchButtonInputLink = document.querySelector("button#header-left-search-button").querySelector("a")

    constructor() {
        SearchStudentHandler.subjectSelect.addEventListener("input", this.subjectSelectInputListener.bind(this))
        SearchStudentHandler.firstNameInput.addEventListener("input", this.firstNameInputInputListener.bind(this))
        SearchStudentHandler.lastNameInput.addEventListener("input", this.lastNameInputInputListener.bind(this))

        this.searchButtonInputLinkInitialURL = SearchStudentHandler.searchButtonInputLink.getAttribute("href")
        this.searchButtonInputLinkParams = new URLSearchParams({"subject": SearchStudentHandler.subjectSelectOptions[0].value})
        SearchStudentHandler.searchButtonInputLink.setAttribute("href", this.searchButtonInputLinkInitialURL.concat(`?${this.searchButtonInputLinkParams.toString()}`))
    }

    subjectSelectInputListener(e) {
        this.searchButtonInputLinkParams.set("subject", e.currentTarget.value)
        SearchStudentHandler.searchButtonInputLink.setAttribute("href", this.searchButtonInputLinkInitialURL.concat(`?${this.searchButtonInputLinkParams.toString()}`))
    }

    firstNameInputInputListener(e) {
        if (e.currentTarget.value == '') {
            this.searchButtonInputLinkParams.delete("first_name")
        } else {
            this.searchButtonInputLinkParams.set("first_name", e.currentTarget.value)
        }
        SearchStudentHandler.searchButtonInputLink.setAttribute("href", this.searchButtonInputLinkInitialURL.concat(`?${this.searchButtonInputLinkParams.toString()}`))
    }


    lastNameInputInputListener(e) {
        if (e.currentTarget.value == '') {
            this.searchButtonInputLinkParams.delete("last_name")
        } else {
            this.searchButtonInputLinkParams.set("last_name", e.currentTarget.value)
        }
        SearchStudentHandler.searchButtonInputLink.setAttribute("href", this.searchButtonInputLinkInitialURL.concat(`?${this.searchButtonInputLinkParams.toString()}`))
    }    
}

const search_student_handler = new SearchStudentHandler()