<style>
    div {
        /* structure */
        display: flex;
        align-items: center;
        justify-items: center;

        /* look */
        padding: 2rem 0;
        color: var(--color-dark);
        background-color: var(--color-dark);
    }

    a {
        width: 4rem;
        height: 4rem;
        margin: 0 auto;
        z-index: 1;

        /* look */
        filter: invert(100%) sepia(3%) saturate(845%) hue-rotate(217deg)
            brightness(118%) contrast(89%);
    }

    a:hover {
        filter: invert(100%) sepia(3%) saturate(845%) hue-rotate(217deg)
            brightness(90%) contrast(89%);
        transition: ease 200ms;
    }
</style>

<div>
    <a href="/about"> <img src="assets/github.svg" alt="Github Source" /> </a>
</div>
