/**
 * @param {str} href attribute
 */
export function createLink(href) {
    let link = document.createElement("a");
    link.setAttribute("href", href);
    return link
}