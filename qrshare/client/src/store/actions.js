import { jsonOrRedirect } from '../request'
import { currentRoute, routes } from './store'

export async function updateStore(path) {
    // get data
    let data = await jsonOrRedirect(path)

    // overwrite on the current store
    currentRoute.set(
        ((({ routes, ...others }) => ({ ...others })))(data)
    )

    routes.set(data.routes)
}