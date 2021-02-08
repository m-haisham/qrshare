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

// shared routes
export const routes = writable([]);
export const qrUrl = writable("");
export const currentRoute = writable({});

// search
export const searchInfo = writable({});
export const isSearching = writable(false);
export const searchResults = createListStore();

// sort
export const isSorted = createBooleanStore(true);
export const processedResults = derived(
    [searchResults, isSorted],
    ([$searchResults, $isSorted]) =>
        $isSorted ? [...$searchResults].sort(compare) : $searchResults
);
