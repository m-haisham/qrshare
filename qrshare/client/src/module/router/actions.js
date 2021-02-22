import { activeRoute } from "./store";
import { parseNamedParams } from "./utils";

let definedRoutes = {};

export async function init({ routes, options }) {
    definedRoutes = {};
    for (let route of routes) {
        definedRoutes[route.id] = route;
    }

    // initialize options
    options.init(definedRoutes[options.initial.id]);

    registerPopStateListener();
    navigateTo(options.initial);
}

/**
 * @param {number} id id of the route to travel to
 * @param {string} url url of the route, params are extracted from this according to id
 *
 * @param {object} state a custom object that would also be passed down to `route.on`,
 * this can be used to provided values to the on function that cannot be passed through params
 *
 * @param {string} name name is just an optional argument that is passed onto pushState
 * @param {boolean} execute determines whether to execute `route.on`
 * @param {boolean} push determines whether url is pushed onto url history
 */
export async function navigateTo({
    id,
    url,
    state = {},
    name = "",
    execute = true,
    push = true,
}) {
    const route = definedRoutes[id];

    let params = {};
    if (url) {
        params = parseNamedParams(url, route.name);
    } else {
        url = route.name;
    }

    /* no more mutations */
    Object.freeze(params);
    Object.freeze(state);

    /* change active route */
    activeRoute.set({ ...route, url, params, state });
    if (execute) route.on && route.on(params, state);

    /* change browser url */
    if (push) {
        window.history.pushState(
            { id: route.id, state },
            name,
            url || route.name
        );
    }
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
