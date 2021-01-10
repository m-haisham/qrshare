<script>
    export let href;
    export let name;
    export let path;
    export let isFile;
    export let matches;

    import { SizedBox } from "../../utilities";
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

    let title;
    $: {
        const _title = name;

        for (let match of matches) {
            console.log(match);
            console.log(_title.slice(...match));
        }
    }
</script>

<style>
    .ct-button {
        display: block;
        width: 100%;
        font-weight: bold;
        text-align: start;
    }

    div {
        display: flex;
        flex-direction: row;
    }
</style>

{#if isFile}
    <button class="ct-button line-clamp" on:click={file}> {name} </button>
{:else}
    <div>
        <button class="ct-button line-clamp" on:click={folder}>{name}</button>
        <SizedBox width="1rem" />
        <button on:click={zip}>ZIP</button>
    </div>
{/if}
