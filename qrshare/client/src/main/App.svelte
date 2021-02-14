<script>
    import BaseApp from "../components/BaseApp.svelte";
    import { List, Search, App, ThreeDots } from "../module/icons";

    import { Router, activeRoute, navigateTo } from "../module/router";
    import { routes, options } from "./routes";

    import { title, subtitle, currentRoute, updateStore } from "./store";

    const navs = [
        {
            /* its not checked for prior visit in home
               since the routes options calls updateStore onMount which is a visit to home */
            click: () => {
                title.apply(0);
                subtitle.apply(0);

                updateStore($currentRoute.last);

                const { id, url } = $activeRoute[0];
                navigateTo({ id, url, execute: false });
            },
            component: List,
        },
        {
            click: () => {
                if ($activeRoute.key === 1) return;

                // if there were no prior visit to search
                if ($activeRoute[1] === undefined) {
                    title.cache(1, "Search");
                    subtitle.cache(1, null);

                    navigateTo({ id: 2, execute: false });

                    // apply from prior visit
                } else {
                    title.apply(1);
                    subtitle.cache(1, $currentRoute.href);

                    const { id, url } = $activeRoute[1];
                    navigateTo({ id, url, execute: false });
                }
            },
            component: Search,
        },
        {
            click: () => {
                viewIndex.set(2);
            },
            component: App,
        },
        {
            click: () => {
                viewIndex.set(3);
            },
            component: ThreeDots,
        },
    ];
</script>

<BaseApp
    title={$title.current}
    subtitle={$subtitle.current}
    {navs}
    active={$activeRoute.key}
    sticky={true}
>
    <Router {routes} {options} />
</BaseApp>
