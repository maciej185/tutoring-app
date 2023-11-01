class TutorLearningController {
    static addStudentBtns = document.querySelectorAll('div.learnign-left-assigned-main-student-add');

    constructor() {
        this.popup = new PopUp()
        TutorLearningController.addStudentBtns.forEach(addBtn => addBtn.addEventListener('click', this.addStudentBtnClickListener.bind(this)))
    }

    addStudentBtnClickListener(e) {
        this.popup.show()
    }
}

const tutor_learning_controller = new TutorLearningController()