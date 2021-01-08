<style>
    .grid {
        display: grid;
        grid-template-columns: calc(50% - 0.5rem) calc(50% - 0.5rem);
        grid-template-rows: auto auto;
        grid-template-areas:
            "top top"
            "bottom bottom";

        column-gap: 1rem;
    }

    .top {
        grid-area: top;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--color-light-dark);
    }

    .bottom {
        grid-area: bottom;
    }

    @media (min-width: 550px) {
        .grid {
            grid-template-areas:
                "top bottom"
                "top bottom";
        }

        .top {
            margin-bottom: none;
            border-bottom: none;
        }
    }
</style>

<div class="grid">
    <div class="top">
        <slot name="top" />
    </div>
    <div class="bottom">
        <slot name="bottom" />
    </div>
</div>
