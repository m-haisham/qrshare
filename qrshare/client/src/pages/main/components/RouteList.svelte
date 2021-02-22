<script>
    import RouteListItem from "./RouteListItem.svelte";
    import { currentRoute as current, routes } from "../store";
    import { createLink } from "../../../helper";
    import { navigateTo } from "../../../module/router";

    function load(e) {
        const route = e.detail;
        navigateTo({ id: 1, url: route.href, state: route, name: route.name });
    }

    function file(e) {
        createLink(e.detail.path).click();
    }

    function zip(e) {
        window.open(e.detail.zip);
    }
</script>

{#if routes}
    <ul>
        <!-- back item -->
        {#if $current.parent}
            <RouteListItem
                route={{ ...$current.parent, name: "...", isFile: true }}
                on:file={load}
            />
        {/if}

        <!-- item list -->
        {#each $routes as route}
            <RouteListItem
                {route}
                on:folder={load}
                on:file={file}
                on:zip={zip}
            />
        {/each}
    </ul>
{:else}
    <p>Empty</p>
{/if}

<style>
    ul {
        margin-bottom: 0;
    }
</style>
