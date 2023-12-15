class DisplayAvailabilityHandler {
    constructor() {
        this.serviceCalendarMapping = this.getServiceCalendarMapping()
        
        this.currentService = Object.keys(this.serviceCalendarMapping)[0]
        this.currentlyDisplayed = this.serviceCalendarMapping[this.currentService]["current"]
        
        this.serviceSelect = document.querySelector("select.tutor-right-availability-main-service-select")
        this.serviceSelect.addEventListener("change", this.serviceSelectEventListener.bind(this))

        this.arrows = document.querySelectorAll("div.tutor-right-availability-main-calendar-top-arrow")
        this.arrows.forEach(arrow => arrow.addEventListener("click", this.arrowClickEventListener.bind(this)))

        this.week = "current" 
    }

    getServiceCalendarMapping() {
        const serviceCalendarMapping = {}
        const calendars = document.querySelectorAll("div.tutor-right-availability-main-calendar")

        calendars.forEach(calendar => {
            const serviceId = calendar.id.split("-").at(-1)
            try {
                serviceCalendarMapping[serviceId].push(calendar)
            } catch(e) {
                if (e.name == "TypeError") {
                    serviceCalendarMapping[serviceId] = []
                    serviceCalendarMapping[serviceId].push(calendar)
                }
            }  
        })
        for (let service in serviceCalendarMapping) {
            const weekCalendarMapping = {}
            serviceCalendarMapping[service].forEach(calendar => {
                const week = calendar.getAttribute("data-week")
                weekCalendarMapping[week] = calendar
            })
            serviceCalendarMapping[service] = weekCalendarMapping
        }

        return serviceCalendarMapping
    }

    serviceSelectEventListener(e) {
        this.currentlyDisplayed.style.display = "none"
        this.currentService = e.currentTarget.value
        this.currentlyDisplayed = this.serviceCalendarMapping[this.currentService]["current"]
        this.week = "current"
        this.currentlyDisplayed.style.display = "block"
    }

    arrowClickEventListener(e) {
        const direction = e.currentTarget.getAttribute("data-direction")
    
        if (direction == "previous") {
            if (this.week == "previous") return
            this.currentlyDisplayed.style.display = "none"
            if (this.week == "current") {
                this.currentlyDisplayed = this.serviceCalendarMapping[this.currentService]["previous"]
                this.week = "previous"
            } else if (this.week == "next") {
                this.currentlyDisplayed = this.serviceCalendarMapping[this.currentService]["current"]
                this.week = "current"
            } 
        } else {
            if (this.week == "next") return 
            this.currentlyDisplayed.style.display = "none"
            if (this.week == "current") {
                this.currentlyDisplayed = this.serviceCalendarMapping[this.currentService]["next"]
                this.week = "next"
            } else if (this.week == "previous") {
                this.currentlyDisplayed = this.serviceCalendarMapping[this.currentService]["current"]
                this.week = "current"
            } 
        }
    
        this.currentlyDisplayed.style.display = "block"
    }
}

const display_availability_handler = new DisplayAvailabilityHandler()