import imageUploader from "./image-uploader.js";

let dd = {};

const dragOverhandler = (e) => {
    e.preventDefault();

    const target = e.currentTarget;

    const className = target.classList[0]

    target.classList.add(`${className}--hover`)
}

const dragLeavehandler = (e) => {
    e.preventDefault();

    const target = e.currentTarget;

    const className = target.classList[0]

    target.classList.remove(`${className}--hover`)
}

const dropHandler = async (e) => {
    e.preventDefault();

    e.currentTarget.classList.remove(`${e.currentTarget.classList[0]}--hover`)

    const data = new FormData()

    data.append('file', e.dataTransfer.files[0]);

    const textHolder = document.getElementById(dd.outputOptions.id);

    if (dd.outputOptions.loading)
        textHolder.innerText = 'Loading...'

    const response = await imageUploader(dd.uploadUrl, data);

    if (dd.events.onResponse)
        dd.events.onResponse(response)

    if (!response.successful) return textHolder.innerText = 'Could not read try again or try a different image...'

    if (dd.outputOptions.output)
        textHolder.innerText =
            `${dd.outputOptions.outprefix ? dd.outputOptions.outprefix + ': ' : ''} ${response.text}`

}

const addEventListeners = () => {
    const elem = document.getElementById(dd.id);

    elem.addEventListener('dragover', dragOverhandler)
    elem.addEventListener('dragleave', dragLeavehandler)
    elem.addEventListener('drop', dropHandler)
}

const initDragDrop = (id, uploadUrl, outputOptions) => {
    dd = { id, uploadUrl, outputOptions, events: {} }

    addEventListeners()
}

const onResponse = (cb) => {
    dd.events.onResponse = cb
}

export default (id, uploadUrl, outputOptions) => {
    initDragDrop(id, uploadUrl, { ...{ id: 'read-image-text', loading: true, outprefix: '', output: true }, ...outputOptions});

    return {onResponse};
}