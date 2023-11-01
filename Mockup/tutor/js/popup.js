class PopUp {
    static popupDiv = document.querySelector('div.popup')
    static popupCloseBtn = document.querySelector('div.popup-main-header-close')

    constructor() {
        PopUp.popupCloseBtn.addEventListener('click', PopUp.closeBtnClickHandling)
    }

    static closeBtnClickHandling(e) {
        PopUp.popupDiv.style.display = 'none'
    }

    show(e) {
        PopUp.popupDiv.style.display = 'flex'
    }
}

const popup = new PopUp()