import fetch from "./fetch.js"

const attachMessage = (message, type = 'user-message') => {
    const formated = `
        <p class="container__content__functionality__chat__body__${type}">
            <span>${message}</span>
        </p>
    `

    document.getElementById('chat-body')
        .innerHTML += formated;
}

export const sendMessage = async () => {
    const response = await fetch('/chatbot/message', {
        body: {
            text: document.getElementById('new-message').value,
        }
    })

    if (response.successful) {
        attachMessage(document.getElementById('new-message').value)
        attachMessage(response.text, 'bot-message')

        document.getElementById('new-message').value = ''
    }
}