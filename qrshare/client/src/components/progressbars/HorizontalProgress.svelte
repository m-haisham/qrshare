<script>
    export let value = 0.2;
    export let trails = false;
</script>

<button
    role="progressbar"
    aria-valuenow={value}
    aria-valuemin={0}
    aria-valuemax={1}
    class:trails
    on:click
>
    <div class="bar" style={`width: ${value * 100}%`} />
    <div class="text"><slot /></div>
</button>

<style>
    button {
        position: relative;
        width: 100%;
        padding: 0;
    }

    .trails {
        border-radius: 4px 0 0 4px;
        border-right: none;
    }

    .bar {
        position: absolute;
        top: 0;
        height: 100%;
        background-color: var(--color-primary);
        border-radius: 4px;
        transition: width 250ms ease-out;
        opacity: 0.25;
    }

    .text {
        position: absolute;
        top: 0;
        height: 100%;
        width: calc(100% - 40px);
        padding: 0 20px;
        margin: 0 auto;
        text-align: start;
    }
</style>
