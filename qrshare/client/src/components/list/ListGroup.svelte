<script>
    export let title;
</script>

<div>
    <h5>{title}</h5>
    <slot />
</div>

<style>
    h5 {
        padding: 0 20px;

        font-size: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1rem;
        font-weight: bold;

        margin: 2rem 0;
        border-left: 1px solid var(--color-button-border);
    }
</style>
