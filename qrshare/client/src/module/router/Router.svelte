<script>
    export let routes;

    import { onMount } from "svelte";
    import { activeRoute } from "./store";
    import { init } from "./actions";

    onMount(() => {
        init({ routes });
    });
</script>

<svelte:component this={$activeRoute.component} />
