<main>
    <div>
        <slot name="header" />
        <slot />
    </div>
    <footer>
        <slot name="footer" />
    </footer>
</main>

<style>
    main {
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    footer {
        margin-top: auto;
    }
</style>
