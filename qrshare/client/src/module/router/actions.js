import { activeRoute } from './store'
import { getRouteById, parseNamedParams } from './utils'

let definedRoutes = []

export function init({routes, initial}) {
    definedRoutes = routes

    registerPopStateListener()
    setInitialRoute(initial)
}

export async function navigateTo({id, url, state = {}, name = ''}) {
    const route = getRouteById(definedRoutes, id)
    const params = parseNamedParams(url, route.name)
    
    // change active route
    activeRoute.set({...route, params, state})
    route.on(params, state)
    
    window.history.pushState({id: route.id, state}, name, url || route.name)
}

function registerPopStateListener() {
    window.onpopstate = function(e) {
        console.log(e)
        if (e.state) {
            const { id, state } = e.state
            const { location, name } = e.target

            navigateTo(id, location.pathname, state, name)
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

    window.history.pushState({id, state}, 'Home', route.name)
}