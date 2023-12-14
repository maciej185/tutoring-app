function getAvailabilityDiv(startTime, endTime, object_id, deleteListener) {
    const availabilityDiv = document.createElement("div")
    availabilityDiv.classList.add("popup-main-availabilites-availability", "popup-main-form", "box", "box-main" ,"adjacent-container")

    const availabilityInfoDiv = document.createElement("div")
    availabilityInfoDiv.classList.add("popup-main-form-info", "adjacent-container")

    const availabilityInfoStartDiv = document.createElement("div")
    availabilityInfoStartDiv.classList.add("popup-main-form-info-start")
    availabilityInfoStartDiv.innerHTML = `
                                    <div class="popup-main-form-info-start-top info-top">
                                        Start
                                    </div>
                                    <div class="popup-main-form-info-start-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-start-bottom-input time-input" id="popup-main-form-info-start-bottom-input-${object_id}" value="${startTime}">
                                    </div> 
    `

    const availabilityInfoEndDiv = document.createElement("div")
    availabilityInfoEndDiv.classList.add("popup-main-form-info-end")
    availabilityInfoEndDiv.innerHTML = `
                                    <div class="popup-main-form-info-end-top info-top">
                                        End
                                    </div>
                                    <div class="popup-main-form-info-end-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-end-bottom-input time-input_readonly" value="${endTime}"  readonly>
                                    </div>
    `

    availabilityInfoDiv.append(availabilityInfoStartDiv, availabilityInfoEndDiv)

    const availabilityDeleteDiv = document.createElement("div")
    availabilityDeleteDiv.classList.add("popup-main-availabilites-availability-delete","popup-main-form-delete", "icon_green")
    availabilityDeleteDiv.id = `popup-main-availabilites-availability-delete-${object_id}`
    availabilityDeleteDiv.innerHTML = `
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
                                </svg>
    `
    availabilityDeleteDiv.addEventListener("click", deleteListener)
    
    availabilityDiv.append(availabilityInfoDiv, availabilityDeleteDiv)

    return availabilityDiv
}