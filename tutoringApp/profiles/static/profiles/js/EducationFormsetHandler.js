class EducationFormsetHandler {
    static managementFormContainer = document.querySelector('div.profile-education-main-management_form')

    static managementFormTotalFormsInput = EducationFormsetHandler.managementFormContainer.querySelector('input#id_education_set-TOTAL_FORMS')
    static managementFormMinNumFormsInput = EducationFormsetHandler.managementFormContainer.querySelector('input#id_education_set-MIN_NUM_FORMS')

    static formListContainer = document.querySelector('div.profile-education-main')

    static emptyFormContainer = document.querySelector('div#profile-education-main-school_empty-0')
    static emptyFormContainerTemplate = EducationFormsetHandler.emptyFormContainer.cloneNode(true)
    static emptyFormDeleteBtn = EducationFormsetHandler.emptyFormContainer.querySelector('div#profile-education-main-school_empty-delete-0')
    static addFormBtn = document.querySelector('div.profile-education-main-add')

    static getDeleteBtnId = (index) => `profile-education-main-school_empty-delete-${index}`
    static getFormContainerId = (index) => `profile-education-main-school_empty-${index}`

    constructor() {
        this.totalFormsValue = Number(EducationFormsetHandler.managementFormTotalFormsInput.value)
        this.minNumFormsValue = Number(EducationFormsetHandler.managementFormMinNumFormsInput.value)

        this.formContainers = [EducationFormsetHandler.emptyFormContainer]
        this.formDeleteBtns = [EducationFormsetHandler.emptyFormDeleteBtn]

        this.numberOfEmptyForms = 1
        // index of inputs in the last, empty form
        this.indexOfEmptyForm = document.querySelectorAll('div.profile-education-main-school').length
        this.numberOfNonEmptyForms = document.querySelectorAll('div.profile-education-main-school').length - 1

        EducationFormsetHandler.emptyFormDeleteBtn.addEventListener('click', this.deleteFormBtnClickListener.bind(this))
        EducationFormsetHandler.addFormBtn.addEventListener('click', this.addFormBtnClickListener.bind(this))
    }

    updateManagementForm(increment) {
        this.totalFormsValue = increment ? this.totalFormsValue + 1 : this.totalFormsValue - 1
        this.minNumFormsValue = increment ? this.minNumFormsValue + 1 : this.minNumFormsValue - 1

        EducationFormsetHandler.managementFormTotalFormsInput.setAttribute('value', this.totalFormsValue)
        EducationFormsetHandler.managementFormMinNumFormsInput.setAttribute('value', this.minNumFormsValue)
    }

    updateDeleteBtnIndices() {
        this.formDeleteBtns.forEach((deleteBtn, index) => deleteBtn.id = EducationFormsetHandler.getDeleteBtnId(index))
    }

    updateFormContainerIndices() {
        this.formContainers.forEach((formContainer, index) => formContainer.id = EducationFormsetHandler.getFormContainerId(index))
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

    updateInputIdsAndNames(formDiv, newIndex) {
        const schoolInput = formDiv.querySelector('select.education-form-school')
        schoolInput.id = `id_education_set-${newIndex}-school`
        schoolInput.name = `education_set-${newIndex}-school`

        const degreeInput = formDiv.querySelector('input.education-form-degree')
        degreeInput.id = `id_education_set-${newIndex}-degree`
        degreeInput.name = `education_set-${newIndex}-degree`

        const startDateInput = formDiv.querySelector('input.education-form-start_date')
        startDateInput.id = `id_education_set-${newIndex}-start_date`
        startDateInput.name = `education_set-${newIndex}-start_date`

        const endDateInput = formDiv.querySelector('input.education-form-end_date')
        endDateInput.id = `id_education_set-${newIndex}-end_date`
        endDateInput.name = `education_set-${newIndex}-end_date`
        
        const additionalInfoInput = formDiv.querySelector('input.education-form-additional_info')
        additionalInfoInput.id = `id_education_set-${newIndex}-additional_info`
        additionalInfoInput.name = `education_set-${newIndex}-additional_info`  
    }

    addFormBtnClickListener(e) {
        const newFormContainer = EducationFormsetHandler.emptyFormContainerTemplate.cloneNode(true)
        newFormContainer.id = newFormContainer.id.replace('0', this.numberOfEmptyForms)

        const newFormDeleteBtn = newFormContainer.querySelector('div.profile-education-main-school-delete')
        newFormDeleteBtn.id = newFormDeleteBtn.id.replace('0', this.numberOfEmptyForms)
        newFormDeleteBtn.addEventListener('click', this.deleteFormBtnClickListener.bind(this))

        this.updateInputIdsAndNames(newFormContainer, this.indexOfEmptyForm)
    
        this.numberOfEmptyForms++
        this.indexOfEmptyForm++
        this.updateManagementForm(true)

        this.formContainers.push(newFormContainer)
        this.formDeleteBtns.push(newFormDeleteBtn)

        EducationFormsetHandler.formListContainer.insertBefore(newFormContainer, EducationFormsetHandler.addFormBtn)
    }
}

const education_formset_handler = new EducationFormsetHandler()