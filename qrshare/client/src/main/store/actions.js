import { jsonOrRedirect } from "../../request";
import {
    title,
    subtitle,
    currentRoute,
    isSearching,
    routes,
    searchResults,
} from "./store";

/**
 * gets the route information and updates state
 * @param {string} path url path pointing towards a particular
 */
export async function updateStore(path) {
    // get data
    let data = await jsonOrRedirect(path);

    // overwrite on the current store
    let current = (({ routes, ...others }) => others)(data);
    currentRoute.set({ ...current, last: path });

    // set sub routes
    routes.set(data.routes);

    // set titles
    title.cache(0, current.name);
    if (current.parent) {
        subtitle.cache(0, "~" + current.parent.href);
    } else {
        subtitle.cache(0, null);
    }

    return { current, routes };
}

/**
 * Initiates a search on the given parameters
 *
 * Note: Previous search results are deleted
 *
 * @param {string} path path to search
 * @param {string} query query string that is applied on path name
 * @param {Array[string]} exts file extensions
 * @param {Array[string]} types types of paths to include in search (is_file, is_dir)
 * @param {number} limit number of search results to return
 */
export async function search({ path = "/", query, exts, types, limit = 100 }) {
    // reset previous results
    isSearching.set(true);
    searchResults.clear();

    // Build search query url
    // The parameters are added as needed
    const base = "/search?";

    // url parameters
    const params = [];

    // add search path
    params.push("path=" + path);

    // add search limit
    params.push("limit=" + limit);

    // add query
    if (query != null) {
        params.push("query=" + query);
    }

    // add extensions
    if (exts != null) {
        // exts is expected to be an array
        // this constructs a url with multiple values for exts
        if (Array.isArray(exts)) {
            for (let ext of exts) {
                params.push("exts=" + ext);
            }
        } else if (typeof exts === "string") {
            params.push("exts=" + exts);
        } else {
            console.error(
                `Received unexpected type exts[${typeof exts}]=${exts}; Expected type Array`
            );
        }
    }

    // add types
    if (types != null) {
        // types is expected to be an array
        // this constructs a url with multiple values for types
        if (Array.isArray(types)) {
            for (let type of types) {
                params.push("types=" + type);
            }
        } else if (typeof types === "string") {
            params.push("types=" + types);
        } else {
            console.error(
                `Received unexpected type types[${typeof types}]=${types}; Expected type Array`
            );
        }
    }

    const source = new EventSource(base + params.join("&"));
    // console.log({msg: 'start', source})

    source.onmessage = (e) => {
        searchResults.push(JSON.parse(e.data));
    };

    source.onerror = (e) => {
        if (e.eventPhase === EventSource.CLOSED) {
            isSearching.set(false);
        } else {
            console.error(e.target.message);
        }
        source.close();
    };
}
