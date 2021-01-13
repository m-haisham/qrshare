import { activeRoute } from './store'
import { getRouteById, parseNamedParams } from './utils'

let definedRoutes = []

export function init({routes, initial}) {
    definedRoutes = routes

    registerPopStateListener()
    setInitialRoute(initial)
}

export async function navigateTo({id, url, state = {}, name = '', push=true}) {
    const route = getRouteById(definedRoutes, id)
    let params = {}
    if (url) {
        params = parseNamedParams(url, route.name)
    }
    
    // change active route
    activeRoute.set({...route, params, state})
    route.on(params, state)
    
    if (push)
        window.history.pushState({id: route.id, state}, name, url || route.name)
}

function registerPopStateListener() {
    window.onpopstate = function(e) {
        if (e.state) {
            navigateTo({url: e.target.location.pathname, ...e.state, push: false})
        }
    }
}

function setInitialRoute({ id, params={}, state={} }) {
    let route = getRouteById(definedRoutes, id);
    
    activeRoute.set({
        ...route,
        params,
        state
    })

    route.on(params, state)

    window.history.pushState({id, state, name: route.name}, 'Home', route.name)
}