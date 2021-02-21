import { title as titleStore, subtitle as subtitleStore } from "../store";

/**
 * extends functionality of onpopstate by adding mutations to store
 *
 * mutations include
 * - checking for presence of title and subtitle and applying them to appbar
 */
function extendPopStateListener() {
    const onpopstate = window.onpopstate;
    window.onpopstate = (e) => {
        if (e.state) {
            const { key, title, subtitle } = e.state;

            /* this block checks for the presence of titles
               in state and applies them */
            if (key !== undefined) {
                if (title !== undefined) {
                    titleStore.cached(key, title);
                }

                if (subtitle !== undefined) {
                    subtitleStore.cached(key, subtitle);
                }
            }

            /* call default */
            onpopstate(e);
        }
    };
}

export { extendPopStateListener };
