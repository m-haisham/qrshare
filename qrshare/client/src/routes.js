import Home from './views/Home.svelte'

function updatePaths(params, state) {
    console.log({params, state})
}

const routes = [
    {
        id: 0,
        name: '/',
        component: Home,
        on: updatePaths
    },
    {
        id: 1,
        name: '/:path',
        component: Home,
        on: updatePaths
    }
]

export { routes }