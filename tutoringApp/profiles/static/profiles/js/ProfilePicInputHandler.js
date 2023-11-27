class ProfilePicInputHandler {
    static profilePicOuterContainer = document.querySelector('div.profile-info-main-left_top')
    static profilePicContainer = document.querySelector('div.profile-info-main-left_top-picture')
    static profilePicInputContainer = document.querySelector('div.profile-info-main-left_top-picture-input')
    static profilePicInput = document.querySelector('input#profile-info-main-left_top-picture-input-input')
    static profilePicImgElement = document.querySelector('img.profile-info-main-left_top-picture-img')
    static profilePicInputLabel = document.querySelector('label.profile-info-main-left_top-picture-input_label')
    static profilePicPreviewDeleteBtn = document.querySelector('div.profile-info-main-left_top-delete')
    static profilePicErrorsDiv = document.querySelector('div.profile-info-main-left_top-picture-errors')

    constructor() {
        ProfilePicInputHandler.profilePicInput.addEventListener('input', this.profilePicInputListener.bind(this))
        ProfilePicInputHandler.profilePicPreviewDeleteBtn.addEventListener('click', this.profilePicPreviewDeletebtnListener.bind(this))
    }

    profilePicInputListener(e) {
        const [file] = ProfilePicInputHandler.profilePicInput.files
        if (file) ProfilePicInputHandler.profilePicImgElement.setAttribute('src', URL.createObjectURL(file))
        ProfilePicInputHandler.profilePicImgElement.style.display = 'block'

        ProfilePicInputHandler.profilePicPreviewDeleteBtn.style.display = 'block'
        ProfilePicInputHandler.profilePicInputLabel.style.display = 'none'

    }

    profilePicPreviewDeletebtnListener(e) {
        ProfilePicInputHandler.profilePicImgElement.setAttribute('src', '')
        ProfilePicInputHandler.profilePicImgElement.style.display = "none"
        if (ProfilePicInputHandler.profilePicErrorsDiv) ProfilePicInputHandler.profilePicErrorsDiv.style.display = "none"
        ProfilePicInputHandler.profilePicInput.value = null

        ProfilePicInputHandler.profilePicPreviewDeleteBtn.style.display = 'none'
        ProfilePicInputHandler.profilePicInputLabel.style.display = 'block'
    } 



}
