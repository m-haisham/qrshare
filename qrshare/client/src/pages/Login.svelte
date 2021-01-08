<script>
    import Global from "../components/Global.svelte";
    import Footer from "../components/Footer.svelte";
    import { Mobile, Desktop } from "../components/login";
    import { MediaQuery } from "../components/utilities";

    function auth(e) {
        console.log(e.detail.value);
    }
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
            <MediaQuery query="(min-width: 550px)" let:matches>
                {#if matches}
                    <!-- other -->
                    <Desktop on:submit={auth} />
                {:else}
                    <!-- mobile -->
                    <Mobile on:submit={auth} />
                {/if}
            </MediaQuery>
        </div>
        <footer>
            <Footer />
        </footer>
    </main>
</Global>
