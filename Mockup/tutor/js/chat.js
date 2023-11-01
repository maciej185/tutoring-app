class ChatController {
    static searchInputDivs = document.querySelectorAll("div.chat-left_top-main-chat_search")
    static searchInputs = Array.from(ChatController.searchInputDivs).map(searchInputDiv => searchInputDiv.querySelector('input'))

    constructor() {
        ChatController.searchInputs.forEach(searchInput => searchInput.addEventListener('focus', this.searchInputsListenerFactory('focus').bind(this)))
        ChatController.searchInputs.forEach(searchInput => searchInput.addEventListener('blur', this.searchInputsListenerFactory('blur').bind(this)))
        
    }

    _removeBottomBorderRadius(inputElement) {
        inputElement.style.borderRadius = "0.25rem 0.25rem 0 0"
    }

    _addBottomBorderRadius(inputElement) {
        inputElement.style.borderRadius = "0.25rem"
    }

    searchInputsListenerFactory(eventType) {
        return function(e) {
            const inputElement = e.currentTarget;
            const resultsDiv = inputElement.nextElementSibling;


            if (eventType == 'focus') {
                resultsDiv.style.display = 'block'
                this._removeBottomBorderRadius(inputElement)
            } else {
                resultsDiv.style.display = 'none'
                this._addBottomBorderRadius(inputElement)
            }
            
        }
    }
    

}

const chat_controller = new ChatController()