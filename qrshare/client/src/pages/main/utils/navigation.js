import { navigateTo } from "../../../module/router";

function navigateHome(push = true) {
    navigateTo({
        id: 0,
        state: {
            path: "/",
            href: "/",
        },
        push,
    });
}

export { navigateHome };
