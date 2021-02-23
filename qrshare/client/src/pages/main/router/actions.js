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
            const { id, key, title, subtitle } = e.state;

            /* this block checks for the presence of titles
               in state and applies them */
            if (key) {
                if (!title) titleStore.apply(key);
                else titleStore.cached(key, title);

                if (!subtitle) subtitleStore.apply(key);
                else subtitleStore.cached(key, subtitle);
            }

            switch (id) {
                /* essentially forces all search popstate events to not execute
                   provided on state change code */
                case 3:
                case 4:
                    e.state.execute = false;
                    break;

                default:
                    break;
            }

            /* call default */
            onpopstate(e);
        }
    };
}

export { extendPopStateListener };
