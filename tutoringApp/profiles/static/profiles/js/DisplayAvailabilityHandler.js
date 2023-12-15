class DisplayAvailabilityHandler {
    constructor() {
        this.serviceCalendarMapping = {}
        this.calendars = document.querySelectorAll("div.tutor-right-availability-main-calendar")
        this.calendars.forEach(calendar => {
            const serviceId = calendar.id.split("-").at(-1)
            this.serviceCalendarMapping[serviceId] = calendar
        })
        console.log(this.serviceCalendarMapping)
        
        this.currentlyDisplayed = this.calendars[0]
        
        this.serviceSelect = document.querySelector("select.tutor-right-availability-main-service-select")
        this.serviceSelect.addEventListener("change", this.serviceSelectEventListener.bind(this))

    }

    serviceSelectEventListener(e) {
        this.currentlyDisplayed.style.display = "none"
        this.currentlyDisplayed = this.serviceCalendarMapping[e.currentTarget.value]
        this.currentlyDisplayed.style.display = "block"
    }
}

const display_availability_handler = new DisplayAvailabilityHandler()