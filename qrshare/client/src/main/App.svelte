<script>
    import { onMount } from "svelte";
    import BaseApp from "../components/BaseApp.svelte";
    import { List, Search, App, ThreeDots } from "../module/icons";
    import { Router, init, navigateTo, activeRoute } from "../module/router";

    import { routes, options, extendPopStateListener } from "./router";

    import { title, subtitle, currentRoute, updateStore } from "./store";

    /* router is initialized manually to control function call flow
       this ensures that extend is called after router initialization */
    onMount(async () => {
        await init({ routes, options });
        extendPopStateListener();
    });

    /** convenience function to build navigation route based on key */
    function buildNavigation({ id, key, url }) {
        return {
            id,
            url,
            execute: false,
            state: {
                key,
                title: $title.current,
                subtitle: $subtitle.current,
            },
        };
    }

    /**
     * build navigation variant
     * gets id and url from cached route
     */
    const buildNavigationDefined = (key) =>
        buildNavigation({ key, ...$activeRoute[key] });

    const navs = [
        {
            /* its not checked for prior visit in home
           since the routes options calls updateStore onMount which is a visit to home */
            click: () => {
                /* clicking on routes while being there serves as a reload */
                updateStore($currentRoute.last);
                if ($activeRoute.key === 0) return;

                title.apply(0);
                subtitle.apply(0);

                navigateTo(buildNavigationDefined(0));
            },
            component: List,
        },
        {
            click: () => {
                if ($activeRoute.key === 1) return;

                subtitle.cache(
                    1,
                    $currentRoute.href ? "~" + $currentRoute.href : null
                );

                // if there were no prior visit to search
                if ($activeRoute[1] === undefined) {
                    title.cache(1, "Search");

                    navigateTo(buildNavigation({ id: 2, key: 1 }));

                    // apply from prior visit
                } else {
                    title.apply(1);

                    navigateTo(buildNavigationDefined(1));
                }
            },
            component: Search,
        },
        {
            click: () => {
                if ($activeRoute.key === 2) return;

                title.cache(2, "QR");
                subtitle.cache(2, "scan to share");

                navigateTo(buildNavigation({ id: 4, key: 2 }));
            },
            component: App,
        },
        {
            click: () => {
                if ($activeRoute.key === 3) return;

                title.cache(3, "More");
                subtitle.cache(3, null);

                navigateTo(buildNavigation({ id: 5, key: 3 }));
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
    <Router {routes} {options} init={false} />
</BaseApp>
