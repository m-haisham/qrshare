<script>
    import { Check } from "../../module/icons";
    import { createEventDispatcher } from "svelte";

    /** describes whether the tile is checked */
    export let checked = true;

    const dispatch = createEventDispatcher();

    function onClick() {
        dispatch("click", !checked);
    }
</script>

<button on:click={onClick} class="normalized">
    <div class="content line-clamp"><slot /></div>
    <div class="check">
        {#if checked}
            <Check />
        {/if}
    </div>
</button>

<style>
    button {
        display: flex;

        width: 100%;

        padding: 0;
    }

    .content {
        padding: 0 20px;
    }

    .check {
        display: flex;
        align-items: center;

        position: relative;

        height: 100%;

        margin: 0;
        margin-left: auto;

        padding: auto;
        padding-left: 3rem;
        padding-right: 3rem;

        border-left: 1px solid var(--color-button-border);
    }

    button:hover .check,
    button:focus .check {
        border-left-color: var(--color-button-hover-border);
    }

    .check :global(svg) {
        width: 2rem;
        height: 2rem;

        position: absolute;
        top: 50%;
        left: 50%;

        transform: translate(-50%, -50%);
    }
</style>
