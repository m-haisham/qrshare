<script>
    import Footer from "../components/Footer.svelte";
    import Home from "./Home.svelte";
    import { IndefiniteLoader } from "../components/progressbars";
    import { currentRoute, qrUrl } from "./store";

    /* since router object is only created after route is loaded
       we manually call the initialize on router */
    import { onMount } from "svelte";
    import { init } from "../module/router/actions";
    import { routes, options } from "./routes";

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
    <footer>
        <Footer />
    </footer>
</main>

<style>
    main {
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    footer {
        margin-top: auto;
    }
</style>
