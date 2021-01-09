export async function fetchOrRedirect(url) {
    let response = await fetch(url, { redirect:'follow' });
    if (response.redirect) {
        window.location.assign(response.url)
        return
    }

    return response
}

export async function jsonOrRedirect(url) {
    return fetchOrRedirect(url).then((r) => r.json())
}

export async function toDataURL(url) {
    let response = await fetch(url)
    let blob = await response.blob()
    return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsDataURL(blob)
    })
}