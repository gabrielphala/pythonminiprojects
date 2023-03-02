const stdFetch = async (url, body) => {
    const response = await fetch(url, {
        method: 'POST',
        body
    })

    return JSON.parse(await response.text())
}

export const uploadOnClick = (url, cb, btnId = 'img-upload-btn') => {
    document.getElementById(btnId)
        .onclick = async () => {
            document.getElementsByClassName('loading-text')[0].innerText = 'Loading...';

            const file = document.getElementById('file')

            const data = new FormData()

            if (!file.files[0]) return;

            data.append('file', file.files[0])

            cb(await stdFetch(url, data))
        }
}

export default stdFetch