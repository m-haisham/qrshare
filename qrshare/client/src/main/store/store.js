import { writable } from "svelte/store";

function createListStore() {
    const { subscribe, set, update } = writable([])

    return {
        subscribe,
        set,
        push: (item) => update(l => [...l, item]),
        clear: () => set([]),
    }
}

// shared routes
export const routes = writable([])
export const qrUrl = writable('')
export const currentRoute = writable({})

// search
export const isSearching = writable(false)
export const searchResults = createListStore()