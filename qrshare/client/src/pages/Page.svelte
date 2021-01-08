<script>
    export let path;

    // UI components
    import Content from "./Content.svelte";
    import Footer from "../components/Footer.svelte";

    import { onMount } from "svelte";

    let response;
    onMount(async () => {
        response = fetch(`http://localhost:5000/${path}`).then((response) =>
            response.json()
        );
    });
</script>

<style>
    :global(:root) {
        --color-light: #f1f1f1;
        --color-light-dark: #ccc;
        --color-dark: #222222;
        --color-warning: #cc3300;
    }

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
    {#await response}
        Loading...
    {:then data}
        <div>
            <Content {data} />
        </div>
        <footer>
            <Footer />
        </footer>
    {:catch error}
        {error}
    {/await}
</main>
