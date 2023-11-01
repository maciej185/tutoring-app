class ServicesController {
    static servicesContainer = document.querySelector('div.services-main-list')
    static addButton = document.querySelector('div.services-main-list-add') 

    constructor() {
        this.serviceDivs = Array.from(document.querySelectorAll('div.service-removable'))
        this.servicesDeleteBtns = this.serviceDivs.map(serviceDiv => serviceDiv.querySelector('div.services-main-list-service-delete'))
    
        this.numberOfServiceDivs = this.servicesDeleteBtns.length

        ServicesController.addButton.addEventListener('click', this.addServiceButtonListener.bind(this))
        this.servicesDeleteBtns.forEach(deleteBtn => deleteBtn.addEventListener('click', this.deleteServiceButtonListener.bind(this)))
    }

    _getServiceInfoPriceDiv() {
        const serviceInfoPriceDiv = document.createElement('div')
        serviceInfoPriceDiv.classList.add('services-main-list-service-info-price', 'stack-container_smaller')
        serviceInfoPriceDiv.innerHTML = `
                                    <div class="services-main-list-service-info-price-top info-top">
                                        Price per hour
                                    </div>
                                    <div class="services-main-list-service-info-price-bottom info-bottom">
                                        <input type="number" class="services-main-list-service-info-price-bottom-input number-input">
                                    </div>
        `
        return serviceInfoPriceDiv
    }

    _getServiceInfoHoursDiv() {
        const serviceInfoHoursDiv = document.createElement('div')
        serviceInfoHoursDiv.classList.add('services-main-list-service-info-hours', 'stack-container_smaller')
        serviceInfoHoursDiv.innerHTML = `
                                    <div class="services-main-list-service-info-hours-top info-top">
                                        No. of hours
                                    </div>
                                    <div class="services-main-list-service-info-hours-bottom info-bottom">
                                        <input type="number" class="services-main-list-service-info-hours-bottom-input number-input">
                                    </div>
        `
        return serviceInfoHoursDiv
    }

    _getServiceInfoDurationDiv() {
        const serviceInfoDurationDiv = document.createElement('div')
        serviceInfoDurationDiv.classList.add('services-main-list-service-info-duration', 'stack-container_smaller')
        serviceInfoDurationDiv.innerHTML = `
                                    <div class="services-main-list-service-info-duration-top info-top">
                                        Duration
                                    </div>
                                    <div class="services-main-list-service-info-duration-bottom info-bottom">
                                        <select class="services-main-list-service-info-duration-bottom-select options">
                                            <option>30 min</option>
                                            <option>45 min</option>
                                            <option>60 min</option>
                                            <option>75 min</option>
                                            <option>90 min</option>
                                            <option>105 min</option>
                                            <option>120 min</option>  
                                        </select>
                                    </div>
        `

        return serviceInfoDurationDiv
    }

    _getServiceInfoSubjectsDiv() {
        const serviceInfoSubjectDiv = document.createElement('div')
        serviceInfoSubjectDiv.classList.add('services-main-list-service-info-subject', 'stack-container_smaller')
        serviceInfoSubjectDiv.innerHTML = `
                                    <div class="services-main-list-service-info-subject-top info-top">
                                        Subject
                                    </div>
                                    <div class="services-main-list-service-info-subject-bottom info-bottom">
                                        <select class="services-main-list-service-info-subject-bottom-select options">
                                            <option>Math</option>
                                            <option>Physics</option>
                                        </select>
                                    </div>
        `

        return serviceInfoSubjectDiv
    }

    _getServiceInfoDiv() {
        const serviceInfoDiv = document.createElement('div')
        serviceInfoDiv.classList.add('services-main-list-service-info', 'stack-adjecent-container')

        serviceInfoDiv.append(this._getServiceInfoSubjectsDiv(), this._getServiceInfoDurationDiv(), this._getServiceInfoHoursDiv(), this._getServiceInfoPriceDiv())
    
        return serviceInfoDiv
    }

    _getDeleteServiceBtn(index) {
        const deleteBtn = document.createElement('div')
        deleteBtn.classList.add('services-main-list-service-delete', 'icon_green')
        deleteBtn.id = `services-main-list-service-delete-${index}`
        deleteBtn.innerHTML = `
                                <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
                                </svg>
        `
        deleteBtn.addEventListener('click', this.deleteServiceButtonListener.bind(this))
        this.servicesDeleteBtns.push(deleteBtn)

        return deleteBtn
    }

    _getServiceDiv(index) {
        const serviceDiv = document.createElement('div')
        serviceDiv.classList.add('services-main-list-service', 'service-removable', 'box', 'box-main_padded')
        serviceDiv.id = `service-removable-${index}`

        serviceDiv.append(this._getServiceInfoDiv(), this._getDeleteServiceBtn(index))

        return serviceDiv
    }

    _updateServiceDivIndexes() {
        this.serviceDivs.forEach((serviceDiv, index) => serviceDiv.id = `service-removable-${index}`)
    }

    _updateDeletBtnIndexes() {
        this.servicesDeleteBtns.forEach((deleteBtn, index) => deleteBtn.id = `services-main-list-service-delete-${index}`)
    }

    deleteServiceButtonListener(e) {
        const sericeDivIndex = e.currentTarget.id.split('-').at(-1)

        this.serviceDivs[sericeDivIndex].remove()
        this.servicesDeleteBtns[sericeDivIndex].remove()

        this.serviceDivs.splice(sericeDivIndex, 1)
        this.servicesDeleteBtns.splice(sericeDivIndex, 1)
        this.numberOfServiceDivs--

        this._updateServiceDivIndexes()
        this._updateDeletBtnIndexes() 

    }

    addServiceButtonListener(e) {
        const serviceDiv = this._getServiceDiv(this.numberOfServiceDivs)

        this.numberOfServiceDivs++
        this.serviceDivs.push(serviceDiv)
        ServicesController.servicesContainer.insertBefore(serviceDiv, ServicesController.addButton)
    }
}

const services_controller = new ServicesController()