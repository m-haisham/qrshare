<script>
    export let actions;
</script>

{#each actions as action}
    {#if action.raw}
        <svelte:component this={action.component} />
    {:else}
        <button on:click={action.click}>
            <svelte:component this={action.component} />
        </button>
    {/if}
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
</style>
