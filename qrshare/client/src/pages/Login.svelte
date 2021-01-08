<script>
    import Global from "../components/Global.svelte";
    import Footer from "../components/Footer.svelte";
    import { Mobile, Desktop } from "../components/login";
    import { MediaQuery } from "../components/utilities";

    let msg = "";
    async function auth(e) {
        const { value } = e.detail;

        try {
            let response = await fetch(`./login?passcode=${value}`, {
                method: "POST",
                redirect: "follow",
            });

            msg = (await response.json()).msg;
        } catch (e) {
            msg = response.text();
        }
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
                    <Desktop {msg} on:submit={auth} />
                {:else}
                    <!-- mobile -->
                    <Mobile {msg} on:submit={auth} />
                {/if}
            </MediaQuery>
        </div>
        <footer>
            <Footer />
        </footer>
    </main>
</Global>
