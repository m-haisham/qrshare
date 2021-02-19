<script>
    export let title;
    export let icon;
    export let hide = true;
</script>

<div class="prompt">
    <h4>{title}</h4>
    <button class:active={!hide} on:click>
        <div class="icon">
            <svelte:component this={icon} />
        </div>
    </button>
</div>

<div class="content" class:hide>
    <slot />
</div>

<style>
    .prompt {
        display: flex;
        flex-direction: row;
        align-items: center;

        margin-bottom: 1rem;
    }

    h4,
    button {
        margin: 0;
    }

    button {
        padding: 0 12px;

        margin-left: auto;
    }

    button .icon {
        display: flex;
        align-items: center;
        height: 100%;
    }

    .icon :global(svg) {
        height: 2rem;
        width: 2rem;
    }

    .active {
        border-color: var(--color-primary);
    }

    .active :global(svg) {
        fill: var(--color-primary);
    }

    .content {
        max-height: auto;
        overflow: hidden;
    }

    .hide {
        max-height: 0;
    }
</style>
