import { writable } from "svelte/store";

function UniqueKeyRouteStore() {
    const { subscribe, set, update } = writable({});

    return {
        subscribe,

        /**
         * This is an overrided set, such that it would keep track of on route for each key
         * the current route is still available as it was before: `$store.url`
         *
         * previous state can be obtained by using value key as shown below
         * `$store[key].url`
         */
        set: (route) =>
            update((routes) => ({
                ...routes,
                [route.key]: route,
                ...route,
            })),
    };
}

export const activeRoute = UniqueKeyRouteStore();
