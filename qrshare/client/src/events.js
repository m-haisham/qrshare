/*
    Events and reactions
*/
import { updateStore } from './store'

/**
 * Responds to history changes
 * this in combination with history.pushState, handles document url 
 */
window.onpopstate = function(e) {
    if (e.state) {
        updateStore(e.state.path);
    }
}