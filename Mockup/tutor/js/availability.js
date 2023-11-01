class AvaliabilityController {
    static popupDiv = document.querySelector('div.popup')
    static popupCloseBtn = document.querySelector('div.popup-main-header-close')

    static calendarDayDivs = document.querySelectorAll('div.availability-main-calendar-grid-grid-day-current')

    constructor() {
        AvaliabilityController.calendarDayDivs.forEach(day => day.addEventListener('click', AvaliabilityController.show))
        AvaliabilityController.popupCloseBtn.addEventListener('click', AvaliabilityController.closeBtnClickHandling)
    }

    static closeBtnClickHandling(e) {
        AvaliabilityController.popupDiv.style.display = 'none'
    }

    static show(e) {
        AvaliabilityController.popupDiv.style.display = 'flex'
    }
}

const availiability_controller = new AvaliabilityController()