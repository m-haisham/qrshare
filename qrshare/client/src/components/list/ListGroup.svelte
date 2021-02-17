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
        font-size: 1.5rem;
        font-weight: bolder;

        margin: 2rem 0;
    }
</style>
