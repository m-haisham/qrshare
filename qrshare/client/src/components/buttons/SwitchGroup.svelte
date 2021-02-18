<script>
    export let options;
    export let selected = [];
    export let initial = false;

    // create selection values array
    $: values = Array.from({ length: options.length }, (v, i) =>
        values === undefined ? initial : values[i]
    );

    // update selected
    $: selected = options.filter((v, i) => values[i]);

    /**
     * Toggles the given button via the text
     * @param e element instance
     */
    function toggle(e) {
        const index = e.target.dataset.index;
        values[index] = !values[index];
    }
</script>

<div>
    {#each options as option, index}
        <button
            type="button"
            class:button-primary={values[index]}
            data-index={index}
            on:click={toggle}>{option}</button
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
