import { writable } from "svelte/store";

// shared routes
export const routes = writable([])
export const qrUrl = writable('')
export const currentRoute = writable({})

// search
export const isSearching = writable(false)
export const searchResults = writable([])