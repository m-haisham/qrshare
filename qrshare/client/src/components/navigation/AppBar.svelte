<script>
    import NavigationElements from "./NavigationElements.svelte";

    export let title;
    export let subtitle = null;
    export let navs = [];
    export let active = null;
    export let sticky = false;
</script>

<header class:sticky class:adjust-for-subtitle={true}>
    <div class="container">
        <div class="title-wrapper">
            <h4 class="title line-clamp">{title}</h4>
            {#if subtitle}
                <div class="subtitle line-clamp">{subtitle}</div>
            {/if}
        </div>
        <nav class="actions">
            <NavigationElements {navs} {active} />
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

        /* hide in mobile view */
        display: none;
    }

    @media (min-width: 550px) {
        .actions {
            display: flex;
        }
    }
</style>
