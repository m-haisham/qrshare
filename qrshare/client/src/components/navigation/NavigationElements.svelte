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

    /**
     * index of active navigation
     */
    export let active = null;
</script>

{#each navs as nav, index}
    <button on:click={nav.click} class:active={index === active}>
        <svelte:component this={nav.component} {...nav.props ?? {}} />
    </button>
{/each}

<style>
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

    button.active :global(svg) {
        fill: var(--color-primary);
    }
</style>
