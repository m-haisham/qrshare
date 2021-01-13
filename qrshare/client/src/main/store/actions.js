import { fetchOrRedirect, jsonOrRedirect } from '../../request'
import { currentRoute, isSearching, routes, searchResults } from './store'

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

export async function search(query, limit=200) {

    // reset previous results
    isSearching.set(true)
    searchResults.clear()

    const source = new EventSource(`/search?query=${query}&limit=${limit}`)
    // console.log({msg: 'start', source})
    
    source.onmessage = (e) => {
        searchResults.push(JSON.parse(e.data))
    }

    source.onerror = (e) => {
        if (e.eventPhase === EventSource.CLOSED) {
            source.close()
            isSearching.set(false)
        }
    }
}