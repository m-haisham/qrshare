<script>
    export let disabled = true;
</script>

<button class="normalized" on:click {disabled}>
    <slot />
    <slot name="trailing" />
</button>

<style>
    button {
        height: 4rem;
        width: 100%;

        display: flex;
        justify-content: space-between;

        font-size: 1.5rem;
    }

    button:disabled {
        border-color: transparent;
    }

    button > :global(*[name="trailing"]) {
        color: var(--color-subtitle);
        font-size: 1.3rem;
        font-weight: normal;
    }

    button :global(.icon) {
        display: flex;
        align-items: center;
        height: 100%;
    }
</style>
