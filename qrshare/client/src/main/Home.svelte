<script>
    import Footer from "../components/Footer.svelte";
    import Content from "./Content.svelte";
    import Global from "../components/Global.svelte";
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

<Global>
    <main>
        <div>
            <Content />
        </div>
        <footer>
            <Footer />
        </footer>
    </main>
</Global>
