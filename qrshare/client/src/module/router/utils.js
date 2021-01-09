export function getById(routes, id) {
    for (let route of routes)
        if (route.id == id)
            return route;
}

export function getByName(routes, name) {
    for (let route of routes)
        if (route.name == name)
            return route
}