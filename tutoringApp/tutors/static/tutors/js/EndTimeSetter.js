class EndTimeSetter {
    constructor() {
        this.sessionsDuration = Number(document.querySelector("div#info-duration").innerHTML)

        this.popupMainDivs = Array.from(document.querySelectorAll("div.popup-main"))
        this.addAvailabilityForms = this.popupMainDivs.map(popupMainDiv => popupMainDiv.querySelector("div.popup-main-availabilites-availability_form"))
        this.addAvailabilityStartInputs = this.addAvailabilityForms.map(addAvailabilityForm => addAvailabilityForm.querySelector("input.time-input"))
        this.addAvailabilityEndInputs = this.addAvailabilityForms.map(addAvailabilityForm => addAvailabilityForm.querySelector("input.time-input_readonly"))

        this.addAvailabilityStartInputs.forEach(addAvailabilityStartInput => addAvailabilityStartInput.addEventListener("input", this.startInputInputListener.bind(this)))

    }

    static calculateEndTime(startTime, sessionsDuration) {
        const date = new Date(`1970-01-01 ${startTime}`)
        const newDate = new Date(date.getTime() + sessionsDuration*60000)

        return new Intl.DateTimeFormat(undefined, {
            hour: '2-digit',
            minute: '2-digit',
            hourCycle: "h24"
          }).format(newDate)

        
    }

    startInputInputListener(e) {
        if (e.currentTarget.value == "") return

        const inputIndex = e.currentTarget.id.split("-").at(-1)

        const newTime = EndTimeSetter.calculateEndTime(e.currentTarget.value, this.sessionsDuration)

        this.addAvailabilityEndInputs[inputIndex].value = newTime
    }

}

const end_time_setter = new EndTimeSetter()
