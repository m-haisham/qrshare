/* 
    Functions used to request and process data from access points
*/

/**
 * fetches url but prioritizing redirect
 * @param {string} url
 */
async function fetchOrRedirect(url, method = "GET") {
    let response = await fetch(url, { method, redirect: "follow" });
    if (response.redirected) {
        window.location.assign(response.url);
        return;
    }

    return response;
}

/**
 * fetches url but prioritizing redirect
 * and converts to js object
 * @param {string} url
 */
async function jsonOrRedirect(url, method = "GET") {
    return fetchOrRedirect(url, method).then((r) => r.json());
}

/**
 * Downloads the url and converts to data url
 * used for images
 * @param {string} url
 */
async function toDataURL(url) {
    let response = await fetch(url);
    let blob = await response.blob();
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

/**
 * makes a request to the provided url and converts (or tries to)
 * the response to text
 *
 * the method is primarily used for fetching html
 *
 * @param {string} url
 * @param {string} method request method GET, POST, PUT
 */
async function request_text(url, method = "GET") {
    return fetchOrRedirect(url, method).then((r) => r.text());
}

export { fetchOrRedirect, jsonOrRedirect, toDataURL, request_text };
