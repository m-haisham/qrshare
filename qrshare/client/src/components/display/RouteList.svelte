<script>
    import RouteListItem from "./RouteListItem.svelte";
    import { currentRoute as current, routes, updateStore } from "../../store";
    import { createLink } from "../../helper";

    function load(e) {
        const route = e.detail;

        // update state
        updateStore(route.path);

        // update url history
        window.history.pushState(route, route.name, route.href);
    }

    function file(e) {
        createLink(e.detail.zip).click();
    }

    function zip(e) {
        createLink(e.detail.zip).click();
    }
</script>

<style>
    ul {
        margin: 1rem auto 0 auto;
    }

    @media (min-width: 550px) {
        ul {
            margin: auto;
        }
    }
</style>

{#if routes}
    <ul>
        <!-- back item -->
        {#if $current.parent}
            <RouteListItem
                name="..."
                path={$current.parent.path}
                href={$current.parent.href}
                isFile={true}
                on:file={load} />
        {:else if !$current.isRoot}
            <RouteListItem
                name="..."
                path="/root"
                href="/"
                isFile={true}
                on:file={load} />
        {/if}

        <!-- item list -->
        {#each $routes as route}
            <RouteListItem
                {...route}
                on:folder={load}
                on:file={file}
                on:zip={zip} />
        {/each}
    </ul>
{:else}
    <p>Empty</p>
{/if}
