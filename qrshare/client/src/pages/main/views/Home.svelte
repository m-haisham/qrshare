<script>
    import { IndefiniteLoader } from "../../../components/progressbars";
    import { RouteList } from "../components";
    import { title, currentRoute } from "../store";
</script>

<svelte:head>
    <title>{$title.current} - qrshare</title>
</svelte:head>

<div class="container">
    {#if !$currentRoute.name}
        <!-- this is displayed when the routes are loading -->
        <IndefiniteLoader />
    {:else}
        <RouteList />
    {/if}
</div>

<style>
    .container {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
