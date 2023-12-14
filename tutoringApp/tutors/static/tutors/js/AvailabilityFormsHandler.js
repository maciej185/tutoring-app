class AvailabilityFormsHandler {

    static baseURL = "http://127.0.0.1:8000"
    static createAvailabilityEndpointURL = "/tutors/availability/create"

    constructor() {
        this.servicePK = document.querySelector("div#info-service_pk").innerHTML
        
        this.popupMainDivs = Array.from(document.querySelectorAll("div.popup-main"))
        this.addAvailabilityBtns = this.popupMainDivs.map(popupMainDiv => popupMainDiv.querySelector("div.popup-main-add"))
        this.addAvailabilityForms = this.popupMainDivs.map(popupMainDiv => popupMainDiv.querySelector("div.popup-main-availabilites-availability_form"))
        this.addAvailabilityInputs = this.addAvailabilityForms.map(addAvailabilityForm => addAvailabilityForm.querySelector("input.time-input"))
        this.popupMainDivsAvailabilitesContainers = this.popupMainDivs.map(popupMainDiv => popupMainDiv.querySelector("div.popup-main-availabilites"))

        this.addAvailabilityBtns.forEach(addAvailabilityBtn => addAvailabilityBtn.addEventListener("click", this.addBtnClickListener.bind(this)))

        this.dates = this.popupMainDivs.map(popupMainDiv => popupMainDiv.querySelector("div.popup-main-date").innerHTML)
    }

    addBtnClickListener(e) {
        (async function() {
            const btnsIndex = e.currentTarget.id.split("-").at(-1)
            const timeValue = this.addAvailabilityInputs[btnsIndex].value
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
                const availabilityDiv = getAvailabilityDiv(timeValue, responseData.id)
                this.popupMainDivsAvailabilitesContainers[btnsIndex].insertBefore(availabilityDiv, this.addAvailabilityForms[btnsIndex])
                this.addAvailabilityInputs[btnsIndex].value = null
                
            } else {
                console.log("FAIL")
                const resData = await createAvailabilityObjectResponse.json() 
                console.log(resData)
            }
        }).bind(this)()
    }
}

const availability_forms_handler = new AvailabilityFormsHandler()