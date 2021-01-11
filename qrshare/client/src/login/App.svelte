<script>
    import Global from "../components/Global.svelte";
    import Footer from "../components/Footer.svelte";
    import Desktop from "./Desktop.svelte";
    import Mobile from './Mobile.svelte'
    import { MediaQuery } from "../utilities";

    let msg = "";
    async function auth(e) {
        const { value } = e.detail;

        try {
            let response = await fetch(`./login?key=${value}`, {
                method: "POST",
                redirect: "follow",
            });

            // redirect or
            if (response.redirected) {
                window.location.assign(response.url);
            } else {
                let data = await response.json();

                // hack: setting same thing twice removes it so...
                msg = "";
                msg = !data ? "The key does not match, try again." : data.msg;
            }
        } catch (e) {
            alert(e);
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
