import { Home, Results, Qrcode } from "../views";
import { meta, qrUrl, updateStore, search } from "../store";
import { jsonOrRedirect, toDataURL } from "../../request";

function updateRoutes(params, state) {
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
        on: updateRoutes,
        // component: Results,
        // on: updateSearch,
    },
    {
        id: 1,
        key: 0,
        name: "/:path",
        component: Home,
        on: updateRoutes,
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
    {
        id: 4,
        key: 2,
        name: "/qrcode",
        component: Qrcode,
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
        meta.set(await jsonOrRedirect("/meta"));
    },
};

Object.freeze(routes);
Object.freeze(options);

export { routes, options };
