<script>
    import { createEventDispatcher } from "svelte";

    export let route;

    const dispatch = createEventDispatcher();

    function folder() {
        dispatch("folder", route);
    }

    function file() {
        dispatch("file", route);
    }

    function zip() {
        dispatch("zip", route);
    }
</script>

{#if route.isFile}
    <button class="ct-button normalized line-clamp" on:click={file}>
        {route.name}
    </button>
{:else}
    <div>
        <button class="ct-button normalized line-clamp" on:click={folder}
            >{route.name}</button
        >
        <button on:click={zip}>ZIP</button>
    </div>
{/if}

<style>
    .ct-button {
        display: block;
        width: 100%;
        text-align: start;
    }

    div {
        display: flex;
        flex-direction: row;
    }

    div > *:nth-child(1) {
        border-radius: 4px 0 0 4px;
        border-right: none;
    }

    div > *:nth-child(2) {
        border-radius: 0 4px 4px 0;
    }
</style>
