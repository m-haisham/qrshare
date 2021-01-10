<script>
    export let route;

    import { SizedBox } from "../../utilities";
    import { createEventDispatcher } from "svelte";

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

    let title;
    $: {
        const { name, matches } = route;

        title = "";
        let start = 0;
        for (let match of matches) {
            title +=
                name.slice(start, match[0]) +
                `<span>${name.slice(...match)}</span>`;
            start = match[1];
        }

        // piece after all the matches
        title += name.slice(start);
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

    button :global(span) {
        background-color: var(--color-primary);
    }
</style>

{#if route.isFile}
    <button class="ct-button line-clamp" on:click={file}>
        {@html title}
    </button>
{:else}
    <div>
        <button
            class="ct-button line-clamp"
            on:click={folder}>{@html title}</button>
        <SizedBox width="1rem" />
        <button on:click={zip} data-tooltip="This is a tooltip">ZIP</button>
    </div>
{/if}
