<script>
    export let buttons;
</script>

<div class="button-group">
    {#each buttons as btn}
        <button
            type="button"
            class:button-primary={btn.primary ?? false}
            class:expand={btn.expand ?? true}
            on:click={btn.click}>{btn.text}</button
        >
    {/each}
</div>

<style>
    div {
        display: flex;
        flex-direction: row;
        margin-bottom: 1rem;
    }

    button {
        margin-bottom: 0;
    }

    .expand {
        flex-grow: 1;
    }

    button:first-child {
        border-radius: 4px 0 0 4px;
    }

    button:last-child {
        border-radius: 0 4px 4px 0;
    }

    button:not(:first-child):not(:last-child) {
        border-radius: 0;
    }
</style>
