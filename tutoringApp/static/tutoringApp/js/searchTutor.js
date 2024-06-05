class SearchTutorHandler {
    static firstNameInput = document.querySelector("input#header-left-search-first_name")
    static lastNameInput = document.querySelector("input#header-left-search-last_name")

    static searchButtonInputLink = document.querySelector("button#header-left-search-button").querySelector("a")

    constructor() {
        SearchTutorHandler.firstNameInput.addEventListener("input", this.firstNameInputInputListener.bind(this))
        SearchTutorHandler.lastNameInput.addEventListener("input", this.lastNameInputInputListener.bind(this))

        this.searchButtonInputLinkInitialURL = SearchTutorHandler.searchButtonInputLink.getAttribute("href")
        this.searchButtonInputLinkParams = new URLSearchParams({})
        SearchTutorHandler.searchButtonInputLink.setAttribute("href", this.searchButtonInputLinkInitialURL.concat(`?${this.searchButtonInputLinkParams.toString()}`))
    }

    firstNameInputInputListener(e) {
        if (e.currentTarget.value == '') {
            this.searchButtonInputLinkParams.delete("first_name")
        } else {
            this.searchButtonInputLinkParams.set("first_name", e.currentTarget.value)
        }
        SearchTutorHandler.searchButtonInputLink.setAttribute("href", this.searchButtonInputLinkInitialURL.concat(`?${this.searchButtonInputLinkParams.toString()}`))
    }


    lastNameInputInputListener(e) {
        if (e.currentTarget.value == '') {
            this.searchButtonInputLinkParams.delete("last_name")
        } else {
            this.searchButtonInputLinkParams.set("last_name", e.currentTarget.value)
        }
        SearchTutorHandler.searchButtonInputLink.setAttribute("href", this.searchButtonInputLinkInitialURL.concat(`?${this.searchButtonInputLinkParams.toString()}`))
    }    
}

const search_tutor_handler = new SearchTutorHandler()