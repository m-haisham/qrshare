<script>
    export let textH;
    export let textS = "Hide";
    export let secondary = false;
    export let show = false;

    import Divider from "./Divider.svelte";
    import { MediaQuery } from "../utilities";

    $: toggleText = show ? textS : textH;

    function toggleShow() {
        show = !show;
    }
</script>

<MediaQuery query="(min-width: 550px)" let:matches>
    <!-- other -->
    {#if matches}
        <slot />

        <!-- mobile -->
    {:else}
        <div class="block">
            <!-- content -->
            <div class={show ? "box" : "box box-hide"}>
                <slot />
                <Divider percent="50" />
            </div>
            <!-- toggle button -->
            <button
                class={secondary ? "" : "button-primary"}
                on:click={toggleShow}>{toggleText}</button
            >
        </div>
    {/if}
</MediaQuery>

<style>
    .block {
        display: flex;
        flex-direction: column;
    }

    .box {
        max-height: auto;
        overflow: hidden;
    }

    .box-hide {
        max-height: 0;
    }

    button {
        margin-bottom: 0;
    }
</style>
