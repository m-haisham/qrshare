<script>
    import Footer from "../components/Footer.svelte";
    import Home from "./Home.svelte";
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
        <Home />
    </div>
    <footer>
        <Footer />
    </footer>
</main>
