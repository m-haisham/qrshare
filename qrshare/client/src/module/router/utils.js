export function getRouteById(routes, id) {
    for (let route of routes) if (route.id == id) return route;
}

export function getRouteByName(routes, name) {
    for (let route of routes) if (route.name == name) return route;
}

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

    // if namedUrl is undefined, dont continue to parse named url
    if (
        namedUrl === null ||
        namedUrl === undefined ||
        // cant parse from non existent information
        path === "/"
    ) {
        // params require no further changes
        Object.freeze(params);

        return params;
    }

    // extract all the values from named Url
    const namedKeys = namedUrl.split("/").filter((v) => v);

    // build regular expression using named keys
    let rx_builder = "\\/";
    for (let [index, key] of namedKeys.entries()) {
        if (key.startsWith(":")) {
            // start group, match everything (greedy)
            rx_builder += "(.+";

            // switch to (lazy) matching
            if (!key.endsWith(":") && index < namedKeys.length) {
                rx_builder += "?";
            }

            // end group
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
            params[key.replace(/^:+|:+$/g, "")] = result[index];
            index++;
        }
    }

    // params require no further changes
    Object.freeze(params);

    return params;
}
