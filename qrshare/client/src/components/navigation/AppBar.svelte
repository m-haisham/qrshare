<script>
    import { afterUpdate } from "svelte";
    import NavigationElements from "./NavigationElements.svelte";
    import ActionBar from "./ActionBar.svelte";

    export let title;
    export let subtitle = null;
    export let navs;
    export let active = null;
    export let sticky = false;

    /* extract actions of the currently active view */
    $: actions = navs[active]?.actions;

    let pre;

    afterUpdate(() => {
        /* auto scroll subtitle to the furthest, subtitle is most commonly used to display path
           where the last added paths are the most important */
        if (pre) pre.scrollLeft = pre.scrollWidth;
    });
</script>

<header class:sticky>
    <div class="container content">
        <div class="title-wrapper">
            <h4 class="title line-clamp">{title}</h4>
        </div>
        <nav class="actions">
            {#if actions}
                <ActionBar {actions} />
                <div class="divider" />
            {/if}
            <div class="static">
                <NavigationElements {navs} {active} />
            </div>
        </nav>
    </div>
    <div class="subtitle">
        <div class="container">
            <pre
                bind:this={pre}>
                    <!-- non-breaking whitespace -->
                    {subtitle ?? ' '}
            </pre>
        </div>
    </div>
</header>

<style>
    header {
        background-color: var(--color-background);
        opacity: 1;
        z-index: 10;

        /* header and content divider */
        border-bottom: 1px solid var(--color-divider);
        padding-bottom: none;
    }

    h4 {
        padding: 0;
    }

    .sticky {
        position: sticky;
        position: -webkit-sticky;
        top: 0;
        left: 0;
    }

    .content {
        display: flex;
        align-items: center;
        justify-content: space-between;

        height: 100%;

        /* this is a hack applied to make sure that height
           remains same with or without actions */
        min-height: calc(59px - 1rem);
    }

    /* this is applied to all buttons under appbar */
    header :global(button) {
        margin: 0;
    }

    .title {
        font-weight: bold;
        padding: 1rem 0;
        margin-bottom: 0rem;
        word-break: none;
    }

    .subtitle {
        background-color: var(--color-secondary-background);
    }

    pre {
        margin: 0;
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;

        font-size: 1.4rem;

        overflow-y: hidden;
    }

    pre::-webkit-scrollbar {
        height: 1px;
        display: absolute;
    }

    pre::-webkit-scrollbar-track {
        background: var(--color-light);
    }

    /* Handle */
    pre::-webkit-scrollbar-thumb {
        background: var(--color-light-dark);
    }

    .actions {
        display: flex;
        gap: 1rem;

        margin-left: auto;
    }

    .static,
    .divider {
        /* hide in mobile view */
        display: none;
    }
    .divider {
        height: 3rem;
        border-left: 1px solid var(--color-divider);

        margin: auto 0;
    }

    @media (min-width: 750px) {
        .static {
            display: flex;
        }

        .divider {
            display: block;
        }
    }
</style>
