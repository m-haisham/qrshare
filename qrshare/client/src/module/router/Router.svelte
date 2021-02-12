<script>
    export let routes;
    export let options;
    export let init = true;

    import { onMount } from "svelte";
    import { activeRoute } from "./store";
    import { init as initActions } from "./actions";

    onMount(async () => {
        if (!init) {
            return;
        }

        initActions({ routes, options });
    });
</script>

{#key $activeRoute.key}
    <svelte:component this={$activeRoute.component} />
{/key}
