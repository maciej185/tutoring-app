class AvailabilityPopupHandler {

    constructor() {
        this.popupDiv = document.querySelector("div.popup")
        this.popupCloseBtns = document.querySelectorAll("div.popup-main-header-close")

        this.popupMainDivs = document.querySelectorAll("div.popup-main")

        this.calendarDayTiles = document.querySelectorAll("div.availability-main-calendar-grid-grid-day-current")

        this.popupCloseBtns.forEach(popupCloseBtn => popupCloseBtn.addEventListener("click", this.closeAvailabilityPopupClickListener.bind(this)))
        this.calendarDayTiles.forEach(calendarDayTile => calendarDayTile.addEventListener("click", this.calendarDayTileClickListener.bind(this)))
    }

    calendarDayTileClickListener(e) {
        this.popupDiv.style.display = "flex"

        const popupIndex = Number(e.currentTarget.id.split("-").at(-1)) - 1
        this.popupMainDivs[popupIndex].style.display = "block"
    }

    closeAvailabilityPopupClickListener(e) {
        this.popupDiv.style.display = "none"

        const popupIndex = Number(e.currentTarget.id.split("-").at(-1))
        this.popupMainDivs[popupIndex].style.display = "none"
    }
    
}

const availability_popup_handler = new AvailabilityPopupHandler()
