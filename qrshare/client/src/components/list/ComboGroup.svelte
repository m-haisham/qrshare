<script>
    import { createEventDispatcher } from "svelte";
    import SwitchListTile from "./SwitchListTIle.svelte";

    export let options;
    export let selected;
    export let id = null;

    const dispatch = createEventDispatcher();
</script>

<div {id}>
    {#each options as option}
        <SwitchListTile
            checked={option === selected}
            on:click={() => dispatch("toggle", { option })}
        >
            {option}
        </SwitchListTile>
    {/each}
</div>
