<script>
    import Footer from "../components/Footer.svelte";
    import Home from "./Home.svelte";
    import { IndefiniteLoader } from "../components/progressbars";
    import { List, Search, App, ThreeDots } from "../module/icons";
    import { currentRoute, qrUrl } from "./store";

    /* since router object is only created after route is loaded
       we manually call the initialize on router */
    import { onMount } from "svelte";
    import { init } from "../module/router/actions";
    import { routes, options } from "./routes";
    import BottomNavigationBar from "../components/navigation/BottomNavigationBar.svelte";

    onMount(async () => {
        init({ routes, options });
    });
</script>

<main>
    <div>
        {#if !$currentRoute.name || !$qrUrl}
            <!-- this is displayed when the routes are loading -->
            <IndefiniteLoader />
        {:else}
            <Home />
        {/if}
    </div>
    <BottomNavigationBar
        navs={[
            {
                click: () => {},
                component: List,
            },
            {
                click: () => {},
                component: Search,
            },
            {
                click: () => {},
                component: App,
            },
            {
                click: () => {},
                component: ThreeDots,
            },
        ]}
    />
</main>

<style>
    main {
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
</style>
