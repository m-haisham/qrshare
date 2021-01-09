<script>
    import RouteListItem from "./RouteListItem.svelte";
    import { currentRoute as current, routes, updateStore } from "../../store";

    function load({ path }) {
        updateStore(path);
    }

    function goto() {}
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
                isFile={true}
                on:file={load} />
        {:else if !$current.isRoot}
            <RouteListItem
                name="..."
                path="/root"
                isFile={true}
                on:file={load} />
        {/if}

        <!-- item list -->
        {#each $routes as { name, path, isFile, href }}
            <RouteListItem
                {...{ name, path, isFile }}
                on:folder={(e) => load({ path: e.detail.path })}
                on:file={(e) => console.log(e)}
                on:zip={(e) => console.log(e)} />
        {/each}
    </ul>
{:else}
    <p>Empty</p>
{/if}
