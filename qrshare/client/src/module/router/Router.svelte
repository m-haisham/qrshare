<script>
    export let routes;
    export let options;

    import { onMount } from "svelte";
    import { activeRoute } from "./store";
    import { init } from "./actions";

    onMount(async () => {
        init({ routes, ...options });
        options.onMount();
    });
</script>

{#key $activeRoute.key}
    <svelte:component this={$activeRoute.component} />
{/key}
