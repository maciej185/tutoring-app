class AvailabilityFormsHandler {

    static baseURL = "http://127.0.0.1:8000"
    static createAvailabilityEndpointURL = "/tutors/availability/create"
    static deleteAvailabilityEndpointURL = "/tutors/availability/delete/"

    constructor() {
        this.servicePK = document.querySelector("div#info-service_pk").innerHTML
        
        this.popupMainDivs = Array.from(document.querySelectorAll("div.popup-main"))
        this.addAvailabilityBtns = this.popupMainDivs.map(popupMainDiv => popupMainDiv.querySelector("div.popup-main-add"))
        this.addAvailabilityForms = this.popupMainDivs.map(popupMainDiv => popupMainDiv.querySelector("div.popup-main-availabilites-availability_form"))
        this.addAvailabilityInputs = this.addAvailabilityForms.map(addAvailabilityForm => addAvailabilityForm.querySelector("input.time-input"))
        this.addAvailabilityEndInputs = this.addAvailabilityForms.map(addAvailabilityForm => addAvailabilityForm.querySelector("input.time-input_readonly"))
        this.popupMainDivsAvailabilitesContainers = this.popupMainDivs.map(popupMainDiv => popupMainDiv.querySelector("div.popup-main-availabilites"))

        this.addAvailabilityBtns.forEach(addAvailabilityBtn => addAvailabilityBtn.addEventListener("click", this.addBtnClickListener.bind(this)))

        this.dates = this.popupMainDivs.map(popupMainDiv => popupMainDiv.querySelector("div.popup-main-date").innerHTML)

        this.availiabilityDivsDeleteBtns = this.popupMainDivs.map(popupMainDiv => popupMainDiv.querySelectorAll("div.popup-main-form-delete"))
        this.availiabilityDivsDeleteBtns.forEach(availiabilityDivsDeleteBtnsSet => availiabilityDivsDeleteBtnsSet.forEach(availiabilityDivsDeleteBtn => availiabilityDivsDeleteBtn.addEventListener("click", this.deleteAvailabilityBtnClickListener.bind(this))))

        this.warningDivs = this.addAvailabilityForms.map(addAvailabilityForm => addAvailabilityForm.querySelector("div.popup-main-availabilites-availability_form-warning"))
    }

    addBtnClickListener(e) {
        (async function() {
            const btnsIndex = e.currentTarget.id.split("-").at(-1)
            const timeValue = this.addAvailabilityInputs[btnsIndex].value
            if (timeValue == "") return this.displayWarning(btnsIndex, "Incorrect time value!")
            const dateTimeValue = `${this.dates[btnsIndex]} ${timeValue}`
            const finalURL = AvailabilityFormsHandler.baseURL + AvailabilityFormsHandler.createAvailabilityEndpointURL
            const createAvailabilityObjectResponse = await fetch(
                finalURL,
                {
                    method: 'POST',
                    headers:{
                        'Content-Type':'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        "service": this.servicePK,
                        "start": dateTimeValue,
                    })
                }
            )
            if (createAvailabilityObjectResponse.status == 200) {
                const responseData = await createAvailabilityObjectResponse.json()
                const availabilityDiv = getAvailabilityDiv(timeValue, responseData.id, this.deleteAvailabilityBtnClickListener.bind(this))
                this.popupMainDivsAvailabilitesContainers[btnsIndex].insertBefore(availabilityDiv, this.addAvailabilityForms[btnsIndex])
                this.addAvailabilityInputs[btnsIndex].value = null
                this.addAvailabilityEndInputs[btnsIndex].value = null
                this.hideWarning(btnsIndex)
            } else {
                this.displayWarning(btnsIndex, "Server issue, try again!")
            }
        }).bind(this)()
    }

    deleteAvailabilityBtnClickListener(e) {
        (async function() {
            const parentDiv = e.currentTarget.parentNode
            const availabilityObjectPK = e.currentTarget.id.split("-").at(-1)
            const finalURL = AvailabilityFormsHandler.baseURL + AvailabilityFormsHandler.deleteAvailabilityEndpointURL + availabilityObjectPK
            const deleteAvailabilityObjectResponse = await fetch(
                finalURL,
                {
                    method: "DELETE",
                    headers:{
                        'Content-Type':'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                }
            )
            if (deleteAvailabilityObjectResponse.status == 204) {
                parentDiv.remove()
            }
        }).bind(this)()
        
    }

    displayWarning(formIndex, msg) {
        this.warningDivs[formIndex].innerHTML = msg
        this.warningDivs[formIndex].style.display = "block"
    }

    hideWarning(formIndex) {
        this.warningDivs[formIndex].style.display = "none"
    }
}

const availability_forms_handler = new AvailabilityFormsHandler()