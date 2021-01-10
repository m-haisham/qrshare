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
        border: 1px solid #bbb;
    }

    li :global(span) {
        background-color: var(--color-primary-light);
    }

    .button-multiline {
        height: auto;
        max-width: 100%;
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
    }

    .title {
        font-weight: bold;
    }

    .button-extension {
        margin: 0;
        width: 100%;
        border-radius: 0;
        border: none;
        border-top: 1px solid #bbb;
        text-align: start;
    }

    .title-row {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
    }

    .title-id {
        color: var(--color-light-dark);
    }
</style>

<li>
    <button class="button-multiline" on:click={main}>
        <div class="title">
            <div class="title-row">
                <div>
                    {@html title}
                </div>
                <div class="title-id">#{id}</div>
            </div>
        </div>
        <div class="subtitle">~{route.parent.href}</div>
    </button>
    {#if !route.isFile}
        <button class="button-extension" on:click={zip}>Download ZIP</button>
    {/if}
</li>
