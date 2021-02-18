import { writable, derived } from "svelte/store";

function createListStore() {
    const { subscribe, set, update } = writable([]);

    return {
        subscribe,
        set,
        update,
        push: (item) => update((l) => [...l, item]),
        clear: () => set([]),
    };
}

function createBooleanStore(initial) {
    const { subscribe, set, update } = writable(initial);

    return {
        subscribe,
        set,
        flip: () => update((b) => !b),
    };
}

function createCachedStore(initial) {
    const { subscribe, set, update } = writable({ current: initial });

    return {
        subscribe,
        set,

        /**
         * cache with key and apply given data to current
         *
         * @param {number} key cache identifier
         * @param {any} value data to store
         */
        cache: (key, value) =>
            update((store) => ({
                ...store,
                [key]: value,
                current: value,
            })),

        /**
         * apply cached data belonging to `key` to current
         */
        apply: (key) =>
            update((store) => ({
                ...store,
                current: store[key],
            })),
    };
}

/**
 * Compare via number of matches
 */
function compare(a, b) {
    let lenA = a.relevance;
    let lenB = b.relevance;

    if (lenA < lenB) return 1;
    else if (lenA > lenB) return -1;
    return 0;
}

export const meta = writable({});

// view
export const title = createCachedStore("Loading...");
export const subtitle = createCachedStore("");

// shared routes
export const routes = writable([]);
export const qrMarkup = writable("");
export const currentRoute = writable({});

// search
export const searchInfo = writable({ query: "", extensions: "" });
export const isSearching = writable(false);
export const searchResults = createListStore();

// sort
export const isSorted = createBooleanStore(true);
export const processedResults = derived(
    [searchResults, isSorted],
    ([$searchResults, $isSorted]) =>
        $isSorted ? [...$searchResults].sort(compare) : $searchResults
);
