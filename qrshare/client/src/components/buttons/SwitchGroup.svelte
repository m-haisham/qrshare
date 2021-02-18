<script>
    import { createEventDispatcher } from "svelte";

    export let options;
    export let selected;

    const dispatch = createEventDispatcher();

    /** this dispatchs custom event with contains index of button clicked */
    const click = (e) => dispatch("toggle", { index: e.target.dataset.index });
</script>

<div>
    {#each options as option, index}
        <button
            type="button"
            class:button-primary={selected[index]}
            data-index={index}
            on:click={click}>{option}</button
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
        width: 100%;
        margin-bottom: 0;
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
