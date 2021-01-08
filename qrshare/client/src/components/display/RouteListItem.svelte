<script>
    export let href;
    export let name;
    export let path;
    export let isFile;

    import { SizedBox } from "../../utilities";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    function body() {
        dispatch("go", { path, href });
    }

    function zip() {
        dispatch("zip", { path, href });
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
    <button class="ct-button line-clamp" on:click={body}> {name} </button>
{:else}
    <div>
        <button class="ct-button line-clamp" on:click={body}>{name}</button>
        <SizedBox width="1rem" />
        <button on:click={zip}>ZIP</button>
    </div>
{/if}
