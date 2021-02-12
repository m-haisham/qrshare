import Content from "./Content.svelte";
import SearchResult from "./SearchResult.svelte";
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
        component: Content,
        on: updateSharedRoutes,
        // component: SearchResult,
        // on: updateSearch,
    },
    {
        id: 1,
        key: 0,
        name: "/:path",
        component: Content,
        on: updateSharedRoutes,
    },
    {
        id: 2,
        key: 1,
        name: "/results",
        component: SearchResult,
        on: updateSearch,
    },
    {
        id: 3,
        key: 1,
        name: "/:path:/results",
        component: SearchResult,
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
