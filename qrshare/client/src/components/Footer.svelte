<script>
    // the variable is not used currently
    // just added to satisfy linter
    let dark = false;
</script>

<div class:dark>
    <a href="https://github.com/mHaisham/qrshare">
        <img src="assets/github.svg" alt="Github Source" />
    </a>
</div>

<style>
    div {
        /* structure */
        display: flex;
        align-items: center;
        justify-items: center;

        /* look */
        padding: 2rem 0;
        border-top: 1px solid var(--color-light-dark);
    }

    a {
        width: 4rem;
        height: 4rem;
        margin: 0 auto;
        z-index: 1;
        transition: ease 200ms;
        filter: invert(2%) sepia(9%) saturate(228%) hue-rotate(314deg)
            brightness(92%) contrast(76%);
    }

    a:hover {
        filter: none;
    }

    /* DARK MODE */
    div.dark {
        color: var(--color-dark);
        background-color: var(--color-dark);
    }

    div.dark > a {
        /* look */
        filter: invert(100%) sepia(3%) saturate(845%) hue-rotate(217deg)
            brightness(118%) contrast(89%);
    }

    div.dark > a:hover {
        filter: invert(100%) sepia(3%) saturate(845%) hue-rotate(217deg)
            brightness(90%) contrast(89%);
    }
</style>
