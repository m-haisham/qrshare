<script>
    export let title;
</script>

<div>
    <h5>{title}</h5>
    <slot />
</div>

<style>
    div {
        margin-bottom: 1rem;
    }

    h5 {
        padding: 0 20px;

        font-size: 1.5rem;
        font-weight: bolder;

        margin: 2rem 0;
        border-left: 1px solid var(--color-button-border);
    }
</style>
