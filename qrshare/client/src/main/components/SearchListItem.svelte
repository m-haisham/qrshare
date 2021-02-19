<script>
    export let id;
    export let route;

    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    function main() {
        dispatch(route.isFile ? "file" : "folder", route);
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

<li>
    <button class="button-multiline" on:click={main}>
        <div class="title-row">
            <div class="title-text">
                {@html title}
            </div>
            <div class="title-id">#{id + 1}</div>
        </div>
        <div class="subtitle">~{route.parent.href}</div>
    </button>
    {#if !route.isFile}
        <button class="button-extension" on:click={zip}>Download ZIP</button>
    {/if}
</li>

<style>
    li {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 0;
        list-style: none;
        font-size: 14px;
        line-height: 2.5rem;
        letter-spacing: 0.1rem;
        border-radius: 4px;
        border: 1px solid var(--color-divider);
    }

    li :global(span) {
        background-color: var(--color-primary-light);
    }

    .button-multiline {
        height: 100%;
        margin: 0;
        padding: 1rem 20px 1rem 20px;
        color: #555;
        text-align: start;
        font-size: inherit;
        font-weight: inherit;
        line-height: 2.3rem;
        letter-spacing: inherit;
        text-transform: none;
        text-decoration: none;
        white-space: inherit;
        overflow-wrap: break-word;
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        border: none;
        cursor: pointer;

        display: flex;
        flex-direction: column;
    }

    .title-row {
        display: flex;
        width: 100%;
        overflow-wrap: break-word;
        font-weight: bold;
    }

    .subtitle {
        width: 100%;
    }

    .button-extension {
        margin: 0;
        width: 100%;
        border-radius: 0;
        border: none;
        border-top: 1px solid var(--color-divider);
        text-align: start;
    }

    .button-multiline:hover,
    .button-extension:hover {
        color: #111;
    }

    .title-text {
        overflow: hidden;
    }

    .title-id {
        margin-left: auto;
        color: var(--color-light-dark);
    }
</style>
