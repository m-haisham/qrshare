import Content from './Content.svelte'
import SearchResult from './SearchResult.svelte'
import { qrUrl, updateStore, search } from './store'
import { toDataURL } from '../request'

function updateSharedRoutes(params, state) {
    updateStore(state.path)
}

function updateSearch(params, state) {
    search('py', 2)
}

const routes = [
    {
        // id: 0,
        // key: 0,
        // name: '/',
        // component: Content,
        // on: updateSharedRoutes,
        id: 0,
        key: 1,
        name: '/',
        component: SearchResult,
        on: updateSearch,
    },
    {
        id: 1,
        key: 0,
        name: '/:path',
        component: Content,
        on: updateSharedRoutes,
    },
    {
        id: 2,
        key: 1,
        name: '/search/:query',
        component: SearchResult,
        on: updateSearch,
    }
]

const options = {
    initial: {
        id: 0,
        state: {
            path: '/root',
            href: '/'
        }
    },
    onMount: async () => {
        qrUrl.set(await toDataURL("/svg"));
    }
}

export { routes, options }