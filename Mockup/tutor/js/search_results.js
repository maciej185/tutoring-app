class SearchResultsController {
    static AddStudentBtns = document.querySelectorAll('div.add_student_btn')

    constructor() {
        this.popup = new PopUp()
        SearchResultsController.AddStudentBtns.forEach(addStudentBtn => addStudentBtn.addEventListener('click', this.addStudentBtnListener.bind(this)))
    }

    addStudentBtnListener(e) {
        this.popup.show()
    }
}

const search_results_controller = new SearchResultsController()