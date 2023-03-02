export default async (uri, { method = 'POST', headers = { 'Content-Type': 'application/json;charset=utf-8' }, body } = {}) => {
    const response = await fetch(uri, { method, headers, body: JSON.stringify(body) });

    return JSON.parse(await response.text());
};  