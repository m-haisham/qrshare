import { writable } from "svelte/store";

function UniqueKeyRouteStore() {
    const { subscribe, set, update } = writable({});

    return {
        subscribe,
        set: (route) =>
            update((routes) => {
                return {
                    ...routes,
                    [route.key]: route,
                    ...route,
                };
            }),
    };
}

export const activeRoute = UniqueKeyRouteStore();
