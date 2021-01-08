<script>
    export let parent;
    export let routes = [];

    import RouteListItem from "./RouteListItem.svelte";
</script>

{#if routes}
    <ul>
        <!-- back item -->
        {#if parent}
            <RouteListItem
                name="..."
                path={parent.path}
                href={parent.href}
                isFile={true} />
        {/if}

        <!-- item list -->
        {#each routes as route}
            <RouteListItem {...route} on:go={(e) => console.log(e)} />
        {/each}
    </ul>
{:else}
    <p>Empty</p>
{/if}
