import { activeRoute } from './store'
import { getById, getByName } from './utils'
import { UrlParser } from 'url-params-parser'

let definedRoutes = []

export function init({routes}) {
    definedRoutes = routes

    // register to history.state
    window.onpopstate = function(e) {
        console.log(e)
        if (e.state) {
            const { id, state } = e.state
            const { location, name } = e.target

            navigateTo(id, location.pathname, state, name)
        }
    }

    // initial active route
    activeRoute.set({
        ...getByName(definedRoutes, '/'),
        params: {},
        state: {},
    })

}

export async function navigateTo(id, url, [state = {}, name = '']) {
    let route = getById(definedRoutes, id)
    let params = UrlParser(url, route.url).namedParams
    
    route.on(params, state)
    
    // change active route
    activeRoute.set({...route, params, state})
    window.history.pushState({id: route.id, state}, name, url)
}