function escape(string) {
    return string.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&");
}

/**
 * Extracts valid information from url to object
 *
 * @param {String} url url to be parsed
 * @param {String} namedUrl url pattern of how to organise information
 */
export function parseNamedParams(url, namedUrl) {
    // split queries from the url string
    const [path, queries] = url.split("?");

    // initialize params object
    let params = {};

    // parse queries
    if (queries) {
        for (let query of queries.split("&")) {
            const [key, value] = query.split("=");

            // if there is no value, skip the query field
            if (value == null || value === "") continue;

            // split between commas to get values list
            const values = value.split(",");

            // set as array if there is more than one value
            if (values.length == 1) {
                params[key] = value;
            } else {
                params[key] = values;
            }
        }
    }

    if (
        namedUrl == null ||
        /* '/' does not have any further information that can be extracted */
        path === "/"
    ) {
        return params;
    }

    /* extract all the values from named Url
       filter is applied to remove any empty elements such as whitespace */
    const namedKeys = namedUrl.split("/").filter((v) => v);

    /* build regular expression using named keys */
    let rx_builder = "\\/";
    for (let [index, key] of namedKeys.entries()) {
        if (key.startsWith(":")) {
            /* start group, start by matching everything after (greedy) */
            rx_builder += "(.+";

            /* switch to (lazy) matching, stop at next slash */
            if (!key.endsWith(":") && index < namedKeys.length) {
                rx_builder += "?";
            }

            rx_builder += ")";
        } else {
            rx_builder += escape(key);
        }

        // add inbetween slashes
        if (index < namedKeys.length - 1) {
            rx_builder += "\\/";
        }
    }

    // ^[]$ added so that the rx would be a full match
    const result = path.match(RegExp(`^${rx_builder}$`));

    // parse the result into named keys
    let index = 1;
    for (let key of namedKeys) {
        if (key.startsWith(":")) {
            /* the following regex removes leading and trailing colons (:) */
            params[key.replace(/^:+|:+$/g, "")] = result[index];
            index++;
        }
    }

    return params;
}
