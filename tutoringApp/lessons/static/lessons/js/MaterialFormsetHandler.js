class MaterialFormsetHandler extends FormsetHandler {
    constructor(managmenetFormContainersClassName,
        formListContainersClassName,
        emptyFormContainersID,
        emptyFormDeleteBtnID,
        emptyFormContainerClassName,
        emptyFormContainerDeleteBtnClassName,
        addFormBtnsClassName,
        formContainersClassName,
        deleteFormContainerBtnClassName) {
            super(managmenetFormContainersClassName,
                formListContainersClassName,
                emptyFormContainersID,
                emptyFormDeleteBtnID,
                emptyFormContainerClassName,
                emptyFormContainerDeleteBtnClassName,
                addFormBtnsClassName,
                formContainersClassName,
                deleteFormContainerBtnClassName)

            const materialFileInput = document.querySelector("input.lesson-materials-main-form-wrap-input-input")
            materialFileInput.addEventListener("input", this.materialFileInputInputListener.bind(this))
        
        }

    materialFileInputInputListener(e) {
        const textPreviewDiv = e.currentTarget.parentElement.parentElement.querySelector("div.lesson-materials-main-form-file-input-element-preview")
        const inputLabel = e.currentTarget.parentElement.parentElement.querySelector("label")
        const [file] =  e.currentTarget.files
        if (file) textPreviewDiv.innerText = file.name

        inputLabel.style.display = "none"
        textPreviewDiv.style.display = "block"
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

        const newFileInput = newFormContainer.querySelector("input.lesson-materials-main-form-wrap-input-input")
        newFileInput.addEventListener("input", this.materialFileInputInputListener.bind(this))
    }

}

const material_formset_handler = new MaterialFormsetHandler(
    "lesson-materials-management_form",
    "lesson-materials-main",
    "lesson-materials-main-form_empty-0",
    "lesson-materials-main-form_empty-delete-0",
    "lesson-materials-main-form_empty",
    "lesson-materials-main-form_empty-delete",
    "lesson-materials-main-add",
    "lesson-materials-main-form",
    "lesson-materials-main-form-delete"
)