import Home from './Home.svelte'
import { qrUrl, updateStore } from './store'
import { toDataURL } from '../request'

function updateSharedRoutes(params, state) {
    updateStore(state.path)
}

const routes = [
    {
        id: 0,
        key: 0,
        name: '/',
        component: Home,
        on: updateSharedRoutes,
    },
    {
        id: 1,
        key: 0,
        name: '/:path',
        component: Home,
        on: updateSharedRoutes,
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