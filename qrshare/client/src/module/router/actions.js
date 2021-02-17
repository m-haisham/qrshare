import { activeRoute } from "./store";
import { parseNamedParams } from "./utils";

let definedRoutes = {};

export async function init({ routes, options }) {
    definedRoutes = {};
    for (let route of routes) {
        definedRoutes[route.id] = route;
    }

    // initialize options
    options.init();

    registerPopStateListener();
    setInitialRoute(options.initial);
}

export async function navigateTo({
    id,
    url,
    state = {},
    name = "",
    execute = true,
    push = true,
}) {
    const route = definedRoutes[id];

    // extract information from url
    let params = {};
    if (url) {
        params = parseNamedParams(url, route.name);
    } else {
        url = route.name;
    }

    /* this allows execute to be accessed during pop state */
    if (state.execute === undefined) state.execute = execute;

    // prevent further modification to params and state
    Object.freeze(params);
    Object.freeze(state);

    // change active route
    activeRoute.set({ ...route, url, params, state });
    if (state.execute) route.on && route.on(params, state);

    // change browser url
    if (push)
        window.history.pushState(
            { id: route.id, state },
            name,
            url || route.name
        );
}

function registerPopStateListener() {
    window.onpopstate = function (e) {
        if (e.state) {
            navigateTo({
                url: e.target.location.pathname,
                ...e.state,
                push: false,
            });
        }
    };
}

function setInitialRoute({ id, params = {}, state = {} }) {
    let route = definedRoutes[id];

    activeRoute.set({
        ...route,
        url: route.name,
        params,
        state,
    });

    route.on(params, state);

    window.history.pushState(
        { id, state, name: route.name },
        "Home",
        route.name
    );
}
