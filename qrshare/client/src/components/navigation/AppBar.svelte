<script>
    import NavigationElements from "./NavigationElements.svelte";

    export let title;
    export let subtitle = null;
    export let navs = [];
    export let navStates = [];
    export let active = null;
    export let actionStates = [];
    export let sticky = false;

    /* extract actions of the currently active view */
    $: actions = navs[active]?.actions;
</script>

<header class:sticky class:adjust-for-subtitle={true}>
    <div class="container">
        <div class="title-wrapper">
            <h4 class="title line-clamp">{title}</h4>
            <div class="subtitle line-clamp">{subtitle ?? ""}</div>
        </div>
        <nav class="actions">
            {#if actions}
                <NavigationElements navs={actions} active={actionStates} />
                <div class="divider" />
            {/if}
            <div class="static">
                <NavigationElements {navs} active={navStates} />
            </div>
        </nav>
    </div>
</header>

<style>
    header {
        background-color: var(--color-background);
        opacity: 1;
        z-index: 10;

        /* header and content divider */
        border-bottom: 1px solid var(--color-divider);
    }

    .sticky {
        position: sticky;
        position: -webkit-sticky;
        top: 0;
        left: 0;
    }

    .container {
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
    }

    .adjust-for-subtitle {
        padding-bottom: 1rem;
    }

    .adjust-for-subtitle .title {
        padding-bottom: 0rem;
    }

    .adjust-for-subtitle .actions {
        padding-top: 1rem;
    }

    .subtitle {
        color: var(--color-subtitle);
        margin-bottom: 0.5rem;
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
