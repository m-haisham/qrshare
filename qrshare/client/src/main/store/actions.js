import { jsonOrRedirect } from '../../request'
import { currentRoute, routes } from './store'

/**
 * gets the route information and updates state
 * @param {string} path url path pointing towards a particular
 */
export async function updateStore(path) {

    // get data
    let data = await jsonOrRedirect(path)

    // overwrite on the current store
    let current = ((({ routes, ...others }) => ({ ...others })))(data)
    currentRoute.set(
        current
    )

    // set sub routes
    routes.set(data.routes)

    return { current, routes }
}