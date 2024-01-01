class FormsetHandler {
    constructor(managmenetFormContainersClassName,
        formListContainersClassName,
        // both of these IDs end with an index, in case 
        // of the first empty form its zero
        emptyFormContainersID,
        emptyFormDeleteBtnID,
        emptyFormContainerClassName,
        emptyFormContainerDeleteBtnClassName,
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
        this.initialFormTextareaElements = this.emptyFormContainerTemplate.querySelectorAll('textarea')
        this.initialLabelElements = this.emptyFormContainer.querySelectorAll("label[for]")

        this.emptyFormDeleteBtn = this.emptyFormContainer.querySelector(`div#${emptyFormDeleteBtnID}`)

        this.addFormBtn = document.querySelector(`div.${addFormBtnsClassName}`)

        this.getDeleteBtnId = (index) => emptyFormContainersID.replace('0', index)
        this.getFormContainerId = (index) => emptyFormDeleteBtnID.replace('0', index)

        this.initialTotalFormsValue = Number(this.managementFormTotalFormsInput.value) 
        this.totalFormsValue = Number(this.managementFormTotalFormsInput.value)
        this.minNumFormsValue = Number(this.managementFormMinNumFormsInput.value)

        this.formContainers = Array.from(document.querySelectorAll(`div.${emptyFormContainerClassName}`))
        this.formDeleteBtns = Array.from(document.querySelectorAll(`div.${emptyFormContainerDeleteBtnClassName}`))

        this.numberOfEmptyForms = this.formContainers.length
        this.initialNumberOfEmptyForms = this.formContainers.length

        const formContainers = document.querySelectorAll(`div.${formContainersClassName}`)
        this.indexOfEmptyForm = formContainers.length
        this.numberOfNonEmptyForms = this.initialTotalFormsValue - this.initialNumberOfEmptyForms

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

    updateInputLabels(formContainer, newIndex) {
        const newLabelElements = formContainer.querySelectorAll("label[for]")
        
        newLabelElements.forEach((labelElement, index) => {
            const correspondingInitialLabel = this.initialLabelElements[index]
            labelElement.setAttribute("for", correspondingInitialLabel.getAttribute("for").replace(this.initialTotalFormsValue - this.initialNumberOfEmptyForms, newIndex))
            labelElement.id = correspondingInitialLabel.id.replace(this.initialTotalFormsValue, newIndex)
        });
    }

    updateInputIdsAndNames(formContainer, newIndex) {
        const newFormInputElements = formContainer.querySelectorAll('input')
        const newFormSelectElements = formContainer.querySelectorAll('select')
        const newFormTextareaElements = formContainer.querySelectorAll('textarea')

        newFormInputElements.forEach((inputElement, index) => {
            const correspondingInitialInput = this.initialFormInputElements[index]
            // empty form is always the last one and so the index of its inputs is the index
            // of the last form on the page from all forms (regardless if they are bound or not bound)
            inputElement.id = correspondingInitialInput.id.replace(this.initialTotalFormsValue - this.initialNumberOfEmptyForms, newIndex)
            inputElement.name = correspondingInitialInput.name.replace(this.initialTotalFormsValue - this.initialNumberOfEmptyForms, newIndex)
        });

        newFormSelectElements.forEach((selectElement, index) => {
            const correspondingInitialInput = this.initialFormSelectElements[index]
            selectElement.id = correspondingInitialInput.id.replace(this.initialTotalFormsValue - this.initialNumberOfEmptyForms, newIndex)
            selectElement.name = correspondingInitialInput.name.replace(this.initialTotalFormsValue - this.initialNumberOfEmptyForms, newIndex)
        });

        newFormTextareaElements.forEach((textareaElement, index) => {
            const correspondingInitialInput = this.initialFormTextareaElements[index]
            textareaElement.id = correspondingInitialInput.id.replace(this.initialTotalFormsValue - this.initialNumberOfEmptyForms, newIndex)
            textareaElement.name = correspondingInitialInput.name.replace(this.initialTotalFormsValue - this.initialNumberOfEmptyForms, newIndex)
        })
    }

    addFormBtnClickListener(e) {
        const newFormContainer = this.emptyFormContainerTemplate.cloneNode(true)
        newFormContainer.id = newFormContainer.id.replace('0', this.numberOfEmptyForms)

        const newFormDeleteBtn = newFormContainer.querySelector(`div.${this.deleteFormContainerBtnClassName}`)
        newFormDeleteBtn.id = newFormDeleteBtn.id.replace('0', this.numberOfEmptyForms)
        newFormDeleteBtn.addEventListener('click', this.deleteFormBtnClickListener.bind(this))

        this.updateInputIdsAndNames(newFormContainer, this.indexOfEmptyForm)
        this.updateInputLabels(newFormContainer, this.indexOfEmptyForm)

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

    updateFormLabels() {
        this.formContainers.forEach((formContainer, index) => this.updateInputLabels(formContainer, index + this.numberOfNonEmptyForms))
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
        this.updateFormLabels()
        this.updateManagementForm(false)

        this.numberOfEmptyForms--
        this.indexOfEmptyForm--
    }

}