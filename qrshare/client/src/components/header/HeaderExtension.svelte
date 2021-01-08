<script>
    export let show = false;

    import Divider from "../Divider.svelte";
    import { MediaQuery, SizedBox } from "../../utilities";

    $: toggleText = show ? "Hide" : "Menu";

    function toggleShow() {
        show = !show;
    }
</script>

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

    @media (min-width: 550px) {
        .block {
            flex-direction: row;
            margin-left: auto;
        }
    }
</style>

<div class="block">
    <MediaQuery query="(min-width: 550px)" let:matches>
        <!-- other -->
        {#if matches}
            <slot />

            <!-- mobile -->
        {:else}
            <!-- content -->
            <div class={show ? 'box' : 'box box-hide'}>
                <slot />
                <Divider percent="50" />
            </div>
            <!-- toggle button -->
            <button
                class="button-primary"
                on:click={toggleShow}>{toggleText}</button>
        {/if}
    </MediaQuery>
</div>
