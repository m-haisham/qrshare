<script>
    export let href;
    export let name;
    export let path;
    export let isFile;

    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    function folder() {
        dispatch("folder", { name, path, href });
    }

    function file() {
        dispatch("file", { name, path, href });
    }

    function zip() {
        dispatch("zip", { name, path, href });
    }
</script>

{#if isFile}
    <button class="ct-button normalized line-clamp" on:click={file}>
        {name}
    </button>
{:else}
    <div>
        <button class="ct-button normalized line-clamp" on:click={folder}
            >{name}</button
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
