<script>
    import HourglassSplit from "../../../module/icons/HourglassSplit.svelte";
    import { fade } from "svelte/transition";
    import { RouteList } from "../components";
    import { title, currentRoute } from "../store";
</script>

<svelte:head>
    <title>{$title.current} - qrshare</title>
</svelte:head>

<div class="container">
    {#if !$currentRoute.name}
        <!-- this is displayed when the routes are loading -->
        <div class="loading" out:fade={{ duration: 100 }}>
            <HourglassSplit />
        </div>
    {:else}
        <RouteList />
    {/if}
</div>

<style>
    .container {
        margin-top: 1rem;
        margin-bottom: 1rem;

        position: relative;
    }

    .loading {
        --size: 10rem;

        position: fixed;
        top: 50%;
        left: 50%;
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
    }

    .loading :global(svg) {
        height: var(--size);
        width: var(--size);

        color: var(--color-subtitle);
    }
</style>
