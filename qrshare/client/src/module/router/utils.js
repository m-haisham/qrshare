export function getRouteById(routes, id) {
    for (let route of routes)
        if (route.id == id)
            return route;
}

export function getRouteByName(routes, name) {
    for (let route of routes)
        if (route.name == name)
            return route
}

/**
 * Extracts valid information from url to object 
 * 
 * @param {String} url url to be parsed
 * @param {String} namedUrl url pattern of how to organise information
 */
export function parseNamedParams(url, namedUrl) {

    const [path, queries] = url.split('?')

    const allPathNames = path.split("/").filter((v) => v);
    const allNamedParamKeys = namedUrl.split("/").filter((v) => v);
  
    let lastkey
    const params = {};
    for (let [index, key] of allPathNames.entries()) {
        if (index < allNamedParamKeys.length) {
            let paramkey = allNamedParamKeys[index];
            if (paramkey.startsWith(":")) {
                lastkey = paramkey.slice(1);
                params[lastkey] = key;
            }
        } else {
            params[lastkey] += `/${key}`;
        }
    }

    // queries
    if (queries)
        for (let query of queries.split('&')) {
            const [key, value] = query.split('=')
            params[key] = value
        }
    
    return params;
}