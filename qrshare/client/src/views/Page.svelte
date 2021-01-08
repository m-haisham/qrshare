<script>
    import Footer from "../components/Footer.svelte";
</script>

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

<main>
    <div>
        <slot />
    </div>
    <footer>
        <Footer />
    </footer>
</main>
