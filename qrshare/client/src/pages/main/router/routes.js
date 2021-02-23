import { navigateTo } from "../../../module/router";
import { requestJson, requestText } from "../../../request";
import { Home, Results, Qrcode, More } from "../views";
import { meta, qrMarkup, updateStore, search, title, subtitle } from "../store";

async function updateRoutes(params, state) {
    updateStore(state.href);
}

async function updateSearch(params, state) {
    search(params);
}

const routes = [
    {
        id: 0,
        key: 0,
        name: "/",
        component: Home,
        on: updateRoutes,
    },
    {
        id: 1,
        key: 0,
        name: "/path/:path",
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
    /* initial route data is obtained from jinja2 template
       this includes initialId and initialRoute */
    initial: {
        id: initialId,
        url: initialRoute.href,
        state: initialRoute,
        execute: initialId === 1,
        push: true,
    },
    init: async (route) => {
        /* setting default titles */
        title._set({ key: route.key });
        subtitle._set({ key: route.key });
        title.update(0, "Loading...");

        /* this does not actually change view 0 (home),
           it essentially serves to load initial route data
           
           initial route data is loaded during processing initial route data when id is 1 */
        if (route.id !== 1)
            navigateTo({
                id: 0,
                state: {
                    path: "/",
                    href: "/",
                },
                push: false,
            });

        /* these data need to be loaded only once since they are static */
        qrMarkup.set(await requestText("/markup/qr"));
        meta.set(await requestJson("/meta"));
    },
};

Object.freeze(routes);
Object.freeze(options);

export { routes, options };
