class chatHandler {
    static chatTextArea = document.querySelector("textarea#chat-right_bottom-main-message-text-textarea")
    static messageSendBtn = document.querySelector("div#chat-right_bottom-main-message-send-btn")

    static messagesMainDiv = document.querySelector("div.chat-right_bottom-main-chat")

    static getMessageDiv(text, sender = true) {
        `<div class="chat-right_bottom-main-chat-message">
                        <div class="chat-right_bottom-main-chat-message-text chat-right_bottom-main-chat-message-text_sender">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Excepturi unde earum magni, natus necessitatibus corrupti laboriosam consequuntur accusantium vel. Labore eligendi illum voluptate esse dolorem qui eaque similique, sapiente doloribus id, natus quisquam recusandae porro molestiae eum exercitationem voluptas pariatur iste fugit est maiores. Tenetur, expedita pariatur voluptatem, nemo maiores quam consequatur aut fugit atque vel laudantium quia temporibus sunt sint numquam provident consequuntur cupiditate, recusandae unde. Velit, atque, rem ducimus accusantium blanditiis molestiae id vero et mollitia modi quisquam aliquam at. Id, optio eius laboriosam harum molestias consequatur in suscipit reiciendis quis nesciunt, sapiente, fugiat obcaecati doloremque laborum provident.
                        </div>  
                    </div>`
        const messageDiv = document.createElement("div")
        messageDiv.setAttribute("class", "chat-right_bottom-main-chat-message")

        const messageTextDiv = document.createElement("div")
        const classToAdd = sender ? "chat-right_bottom-main-chat-message-text_sender" : "chat-right_bottom-main-chat-message-text_receiver"
        messageTextDiv.setAttribute("class", `chat-right_bottom-main-chat-message-text ${classToAdd}`)
        messageTextDiv.innerHTML = text

        messageDiv.appendChild(messageTextDiv)

        return messageDiv
    }

    constructor() {
        this.tutor_id = JSON.parse(document.getElementById('tutor_id').textContent);
        this.student_id = JSON.parse(document.getElementById('student_id').textContent);
        this.current_user_id = JSON.parse(document.getElementById('current_user_id').textContent)

        this.chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + this.tutor_id
            + '/'
            + this.student_id 
            + '/'
        );

        this.chatSocket.addEventListener("message", (e) => {
            const data = JSON.parse(e.data);            
            const messageDiv = chatHandler.getMessageDiv(data.message, data.user_id == this.current_user_id)
            chatHandler.messagesMainDiv.appendChild(messageDiv)
        })

        this.chatSocket.addEventListener("close", e => console.error('Chat socket closed unexpectedly'))

        chatHandler.messageSendBtn.addEventListener("click", this.messageSendBtnClickHandler.bind(this))
    }

    messageSendBtnClickHandler(e) {
        const message = chatHandler.chatTextArea.value
        this.chatSocket.send(JSON.stringify({
            "message": message,
            "user_id": this.current_user_id
        }));
        chatHandler.chatTextArea.value = ''
    }
}

const chat_handler = new chatHandler()