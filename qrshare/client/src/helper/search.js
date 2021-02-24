export function createSearchUrl({
    path = "/",
    query,
    exts,
    types,
    limit = 100,
}) {
    // get base url depending on path
    const base = path == "/" ? "/results?" : `${path}/results?`;

    // url parameters
    const params = [];

    // add query
    if (query != null) {
        params.push("query=" + query);
    }

    // add extensions
    if (exts != null) {
        // if the array has no values, return
        if (!exts) return;

        params.push("exts=" + exts.join(","));
    }

    // add types filtering
    if (types != null) {
        params.push("types=" + types.join(","));
    }

    // add limit
    params.push("limit=" + limit);

    // join base url and params to get full url
    return base + params.join("&");
}
