/* 
    Functions used to request and process data from access points
*/

/**
 * fetches url but prioritizing redirect
 * @param {string} url
 */
export async function fetchOrRedirect(url) {
    let response = await fetch(url, { redirect:'follow' });
    if (response.redirect) {
        window.location.assign(response.url)
        return
    }

    return response
}

/**
 * fetches url but prioritizing redirect
 * and converts to js object
 * @param {string} url 
 */
export async function jsonOrRedirect(url) {
    return fetchOrRedirect(url).then((r) => r.json())
}

/**
 * Downloads the url and converts to data url
 * used for images
 * @param {string} url 
 */
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