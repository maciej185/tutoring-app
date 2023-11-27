class FormsetHandler {
    constructor(managmenetFormContainersClassName,
        formListContainersClassName,
        // both of these IDs end with an index, in case 
        // of the first empty form its zero
        emptyFormContainersID,
        emptyFormDeleteBtnID,
        addFormBtnsClassName,
        formContainersClassName,
        deleteFormContainerBtnClassName) {

        this.managementFormContainer = document.querySelector(`div.${managmenetFormContainersClassName}`)
        this.managementFormTotalFormsInput = this.managementFormContainer.querySelector(`input[id$="TOTAL_FORMS"]`)
        this.managementFormMinNumFormsInput = this.managementFormContainer.querySelector(`input[id$="MIN_NUM_FORMS"]`)

        this.formListContainer = document.querySelector(`div.${formListContainersClassName}`)

        this.emptyFormContainer = document.querySelector(`div#${emptyFormContainersID}`)
        this.emptyFormContainerTemplate = this.emptyFormContainer.cloneNode(true)

        // needed to later on update the `name` and `value` attribute of inputs when a form is deleted or added
        this.initialFormInputElements = this.emptyFormContainerTemplate.querySelectorAll('input')
        this.initialFormSelectElements = this.emptyFormContainerTemplate.querySelectorAll('select')

        this.emptyFormDeleteBtn = this.emptyFormContainer.querySelector(`div#${emptyFormDeleteBtnID}`)

        this.addFormBtn = document.querySelector(`div.${addFormBtnsClassName}`)

        this.getDeleteBtnId = (index) => emptyFormContainersID.replace('0', index)
        this.getFormContainerId = (index) => emptyFormDeleteBtnID.replace('0', index)

        this.initialTotalFormsValue = Number(this.managementFormTotalFormsInput.value) 
        this.totalFormsValue = Number(this.managementFormTotalFormsInput.value)
        this.minNumFormsValue = Number(this.managementFormMinNumFormsInput.value)

        this.formContainers = [this.emptyFormContainer]
        this.formDeleteBtns = [this.emptyFormDeleteBtn]

        this.numberOfEmptyForms = 1

        const formContainers = document.querySelectorAll(`div.${formContainersClassName}`)
        this.indexOfEmptyForm = formContainers.length
        this.numberOfNonEmptyForms = formContainers.length - 1

        this.addFormBtn.addEventListener('click', this.addFormBtnClickListener.bind(this))
        this.emptyFormDeleteBtn.addEventListener('click', this.deleteFormBtnClickListener.bind(this))

        this.deleteFormContainerBtnClassName = deleteFormContainerBtnClassName
    }

    updateManagementForm(increment) {
        this.totalFormsValue = increment ? this.totalFormsValue + 1 : this.totalFormsValue - 1
        this.minNumFormsValue = increment ? this.minNumFormsValue + 1 : this.minNumFormsValue - 1

        this.managementFormTotalFormsInput.setAttribute('value', this.totalFormsValue)
        this.managementFormMinNumFormsInput.setAttribute('value', this.minNumFormsValue)
    }

    updateInputIdsAndNames(formContainer, newIndex) {
        const newFormInputElements = formContainer.querySelectorAll('input')
        const newFormSelectElements = formContainer.querySelectorAll('select')

        newFormInputElements.forEach((inputElement, index) => {
            const correspondingInitialInput = this.initialFormInputElements[index]
            // empty form is always the last one and so the index of its inputs is the index
            // of the last form on the page from all forms (regardless if they are bound or not bound)
            inputElement.id = correspondingInitialInput.id.replace(this.initialTotalFormsValue - 1, newIndex)
            inputElement.name = correspondingInitialInput.name.replace(this.initialTotalFormsValue - 1, newIndex)
        });

        newFormSelectElements.forEach((selectElement, index) => {
            const correspondingInitialInput = this.initialFormSelectElements[index]
            selectElement.id = correspondingInitialInput.id.replace(this.initialTotalFormsValue - 1, newIndex)
            selectElement.name = correspondingInitialInput.name.replace(this.initialTotalFormsValue - 1, newIndex)
        });
    }

    addFormBtnClickListener(e) {
        const newFormContainer = this.emptyFormContainerTemplate.cloneNode(true)
        newFormContainer.id = newFormContainer.id.replace('0', this.numberOfEmptyForms)

        const newFormDeleteBtn = newFormContainer.querySelector(`div.${this.deleteFormContainerBtnClassName}`)
        newFormDeleteBtn.id = newFormDeleteBtn.id.replace('0', this.numberOfEmptyForms)
        newFormDeleteBtn.addEventListener('click', this.deleteFormBtnClickListener.bind(this))

        this.updateInputIdsAndNames(newFormContainer, this.indexOfEmptyForm)

        this.numberOfEmptyForms++
        this.indexOfEmptyForm++
        this.updateManagementForm(true)

        this.formContainers.push(newFormContainer)
        this.formDeleteBtns.push(newFormDeleteBtn)

        this.formListContainer.insertBefore(newFormContainer, this.addFormBtn)
    }

    updateDeleteBtnIndices() {
        this.formDeleteBtns.forEach((deleteBtn, index) => deleteBtn.id = this.getDeleteBtnId(index))
    }

    updateFormContainerIndices() {
        this.formContainers.forEach((formContainer, index) => formContainer.id = this.getFormContainerId(index))
    }

    updateFormInputIdsAndNames() {
        this.formContainers.forEach((formContainer, index) => this.updateInputIdsAndNames(formContainer, index + this.numberOfNonEmptyForms))
    }

    deleteFormBtnClickListener(e) {
        if (this.numberOfEmptyForms == 1) return

        const formIndex = e.currentTarget.id.split('-').at(-1)

        this.formContainers[formIndex].remove()

        this.formContainers.splice(formIndex, 1)
        this.formDeleteBtns.splice(formIndex, 1)

        this.updateDeleteBtnIndices()
        this.updateFormContainerIndices()
        this.updateFormInputIdsAndNames()
        this.updateManagementForm(false)

        this.numberOfEmptyForms--
        this.indexOfEmptyForm--
    }

}