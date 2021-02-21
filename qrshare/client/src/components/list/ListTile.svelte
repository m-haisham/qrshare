<script>
    export let disabled = true;
    export let id = null;
</script>

<button {id} class="normalized" on:click {disabled}>
    <slot />
    <slot name="trailing" />
</button>

<style>
    button {
        height: 4rem;
        width: 100%;

        display: flex;
        justify-content: space-between;
    }

    button:disabled {
        border-color: transparent;
    }

    button > :global(*[name="trailing"]) {
        color: var(--color-subtitle);
        font-weight: normal;
    }

    button :global(.icon) {
        display: flex;
        align-items: center;
        height: 100%;
    }
</style>
