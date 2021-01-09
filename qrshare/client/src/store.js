import { writable } from "svelte/store";


export const routes = writable([])
export const qrUrl = writable('')
export const currentRoute = writable({})