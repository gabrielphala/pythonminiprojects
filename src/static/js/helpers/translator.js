import fetch from "./fetch.js"

const langs = {
    'af': 'Afrikaans',
    'ga': 'Irish',
    'sq': 'Albanian',
    'it': 'Italian',
    'ar': 'Arabic',
    'ja': 'Japanese',
    'az': 'Azerbaijani',
    'kn': 'Kannada',
    'eu': 'Basque',
    'ko': 'Korean',
    'bn': 'Bengali',
    'la': 'Latin',
    'be': 'Belarusian',
    'lv': 'Latvian',
    'bg': 'Bulgarian',
    'lt': 'Lithuanian',
    'ca': 'Catalan',
    'mk': 'Macedonian',
    'zh-CN': 'Chinese Simplified',
    'ms': 'Malay',
    'zh-TW': 'Chinese Traditional',
    'mt': 'Maltese',
    'hr': 'Croatian',
    'no': 'Norwegian',
    'cs': 'Czech',
    'fa': 'Persian',
    'da': 'Danish',
    'pl': 'Polish',
    'nl': 'Dutch',
    'pt': 'Portuguese',
    'en': 'English',
    'ro': 'Romanian',
    'eo': 'Esperanto',
    'ru': 'Russian',
    'et': 'Estonian',
    'sr': 'Serbian',
    'tl': 'Filipino',
    'sk': 'Slovak',
    'fi': 'Finnish',
    'sl': 'Slovenian',
    'fr': 'French',
    'es': 'Spanish',
    'gl': 'Galician',
    'sw': 'Swahili',
    'ka': 'Georgian',
    'sv': 'Swedish',
    'de': 'German',
    'ta': 'Tamil',
    'el': 'Greek',
    'te': 'Telugu',
    'gu': 'Gujarati',
    'th': 'Thai',
    'ht': 'Haitian Creole',
    'tr': 'Turkish',
    'iw': 'Hebrew',
    'uk': 'Ukrainian',
    'hi': 'Hindi',
    'ur': 'Urdu',
    'hu': 'Hungarian',
    'vi': 'Vietnamese',
    'is': 'Icelandic',
    'cy': 'Welsh',
    'id': 'Indonesian',
    'yi': 'Yiddish',
    'nso': 'Northen Sotho'
}

export const loadLanguages = () => {
    let html = '';

    for (const key in langs) {
        html += `<option value="${key}">${langs[key]}</option>`
    }

    document.getElementById('dest-lang').innerHTML = html;
}

export const getTranslation = async () => {
    const response = await fetch('/translator/translate', {
        body: {
            text: document.getElementById('text-to-translate').value,
            dest: document.getElementById('dest-lang').value
        }
    })

    if (response.successful)
        document.getElementById('translated-text')
            .innerText = response.text;
}