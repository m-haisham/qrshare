<script>
    import { createEventDispatcher } from "svelte";
    import SwitchListTile from "./SwitchListTIle.svelte";

    export let options;
    export let selected;
    export let id = null;

    const dispatch = createEventDispatcher();
</script>

<div {id}>
    {#each options as option, index}
        <SwitchListTile
            checked={selected[index]}
            on:click={() => dispatch("toggle", { index })}
        >
            {option}
        </SwitchListTile>
    {/each}
</div>
