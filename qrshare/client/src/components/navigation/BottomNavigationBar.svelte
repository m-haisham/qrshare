<script>
    import NavigationElements from "./NavigationElements.svelte";

    export let navs;
    // export let active = null;
    export let navStates = null;
</script>

<div class="bottom-nav-wrapper">
    <nav class="bottom-nav">
        <NavigationElements {navs} active={navStates} />
    </nav>
</div>

<style>
    .bottom-nav-wrapper {
        --nav-height: 5rem;
        padding-top: var(--nav-height);
    }

    @media (min-width: 750px) {
        .bottom-nav-wrapper {
            display: none;
        }
    }

    .bottom-nav {
        /* set bottom bar posiition */
        position: fixed;
        bottom: 0;

        height: var(--nav-height);
        width: 100%;

        background-color: var(--color-background);
        border-top: 1px solid var(--color-divider);

        display: flex;
        align-items: center;
        justify-content: space-around;
        padding: 0;
    }

    @media (min-width: 550px) {
        .bottom-nav {
            justify-content: center;
            gap: 1rem;
        }
    }
</style>
