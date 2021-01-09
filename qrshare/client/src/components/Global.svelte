<script>
    import { currentRoute } from "../store";
</script>

<style>
    :global(:root) {
        --color-light: #f1f1f1;
        --color-light-dark: #ccc;
        --color-dark: #222222;
        --color-warning: #cc3300;
    }
</style>

<svelte:head>
    <title>{$currentRoute.name}</title>
</svelte:head>
<slot />
