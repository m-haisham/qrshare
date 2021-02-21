/**
 * makes a request to the provided url and returns the response,
 *
 * redirects are followed
 *
 * @param {string} url
 * @param {string} method request method GET, POST, PUT
 */
async function request(url, method = "GET") {
    let response = await fetch(url, { method, redirect: "follow" });
    if (response.redirected) {
        window.location.assign(response.url);
        return;
    }

    return response;
}

/**
 * makes a request to the provided url and converts (or tries to)
 * the response to text
 *
 * @param {string} url
 * @param {string} method request method GET, POST, PUT
 */
async function requestJson(url, method = "GET") {
    return request(url, method).then((r) => r.json());
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
async function requestText(url, method = "GET") {
    return request(url, method).then((r) => r.text());
}

export { request, requestJson, requestText };
