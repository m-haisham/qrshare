import { Home, Results, Qrcode, More } from "../views";
import { meta, qrMarkup, updateStore, search, title } from "../store";
import { requestJson, requestText } from "../../request";
import { navigateTo } from "../../module/router";

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
    {
        id: 5,
        key: 3,
        name: "/more",
        component: More,
    },
];

const options = {
    initial: {
        id: initialId,
        execute: false,
    },
    init: async (route) => {
        /* setting default titles */
        title._set({ key: route.key });
        title.update(0, "Loading...");

        navigateTo({
            id: 0,
            state: {
                path: "/root",
                href: "/",
            },
            push: false,
        });

        qrMarkup.set(await requestText("/svg"));
        meta.set(await requestJson("/meta"));
    },
};

Object.freeze(routes);
Object.freeze(options);

export { routes, options };
