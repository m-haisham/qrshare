/**
 * @param {str} href attribute
 */
export function createLink(href) {
    let link = document.createElement("a");
    link.setAttribute("href", href);
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
