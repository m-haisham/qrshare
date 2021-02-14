import Home from "./views/Home.svelte";
import Results from "./views/Results.svelte";
import { qrUrl, updateStore, search } from "./store";
import { toDataURL } from "../request";

function updateSharedRoutes(params, state) {
    updateStore(state.path);
}

function updateSearch(params, state) {
    // search({ path: "/", exts: ["py", "pyc"] });
    search(params);
    // console.log({ params });
}

const routes = [
    {
        id: 0,
        key: 0,
        name: "/",
        component: Home,
        on: updateSharedRoutes,
        // component: Results,
        // on: updateSearch,
    },
    {
        id: 1,
        key: 0,
        name: "/:path",
        component: Home,
        on: updateSharedRoutes,
    },
    {
        id: 2,
        key: 1,
        name: "/results",
        component: Results,
        on: updateSearch,
    },
    {
        id: 3,
        key: 1,
        name: "/:path:/results",
        component: Results,
        on: updateSearch,
    },
];

const options = {
    initial: {
        id: 0,
        state: {
            path: "/root",
            href: "/",
        },
    },
    init: async () => {
        qrUrl.set(await toDataURL("/svg"));
    },
};

Object.freeze(routes);
Object.freeze(options);

export { routes, options };
