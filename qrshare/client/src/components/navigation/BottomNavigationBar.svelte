<script>
    /**
     * navs specify the navigation routes
     *
     * navs is a list of objects with each object containing
     * - click: function to be called on nav clicked
     * - component: component to render inside button
     * - props: props to be passed to component (optional)
     */
    export let navs;
</script>

<div class="bottom-nav-wrapper">
    <div class="bottom-nav">
        {#each navs as nav}
            <button on:click={nav.click}>
                <svelte:component this={nav.component} {...nav.props || {}} />
            </button>
        {/each}
    </div>
</div>

<style>
    .bottom-nav-wrapper {
        --nav-height: 5rem;
        padding-top: var(--nav-height);
    }

    @media (min-width: 550px) {
        .bottom-nav-wrapper {
            display: none;
        }
    }

    .bottom-nav {
        --content-height: 4rem;

        /* set bottom bar posiition */
        position: fixed;
        bottom: 0;

        height: var(--nav-height);
        width: 100%;

        background-color: var(--color-background);
        border-top: 1px solid var(--color-light-dark);

        display: flex;
        align-items: center;
        justify-content: space-around;
        padding: 0;
    }

    button {
        border: none;

        /* center svgs vertically */
        display: flex;
        align-items: center;

        margin: 0;
        padding: auto 1rem;
    }

    button :global(svg) {
        width: 2rem;
        height: 2rem;
    }
</style>
