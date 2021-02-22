/**
 * @param {str} href attribute
 */
export function createLink(href) {
    const link = document.createElement("a");
    link.setAttribute("href", href);
    return link;
}

export function downloadLink(href, name = "") {
    const link = document.createElement("a");
    link.setAttribute("href", href);
    link.setAttribute("download", name);
    return link;
}

/** redirect user to project github repository */
export function openSource(popup = true) {
    if (popup) {
        window.open("https://github.com/mHaisham/qrshare");
    } else {
        createLink("https://github.com/mHaisham/qrshare").click();
    }
}
