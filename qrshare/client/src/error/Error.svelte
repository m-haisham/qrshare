<script>
    import Footer from "../components/Footer.svelte";
    import Header from "../components/header/Header.svelte";
    import { HorizontalProgress } from "../components/progressbars";
    import { onMount } from "svelte";

    /* global values are retrieved */
    const code = errorCode;
    const name = errorName;
    const message = errorMessage;
    const redirect = errorRedirect;
    const timeout = errorTimeout;

    /* timeout controls */
    let value = 0;
    const maximumTime = timeout;
    const timeoutIncrement = maximumTime / 1000;

    /* redirect controls */
    let redirectMessage = `Redirecting in ${timeout} seconds`;
    let redirectCancelled = false;

    /**
     * Redirects the user to root
     */
    function redirectNow() {
        // so that the new message isnt overwritten
        value = 0;
        redirectCancelled = true;

        redirectMessage = "Redirecting now";
        window.location.assign(redirect);
    }

    /**
     * Cancels redirect countdown
     */
    function cancelRedirect() {
        if (!redirectCancelled) {
            redirectMessage = `Click to redirect (Auto redirect cancelled)`;
            value = 1;
            redirectCancelled = true;
        }
    }

    /* delay for the given time */
    const delay = (ms) => new Promise((res) => setTimeout(res, ms));

    /**
     * redirect countdown
     */
    async function countdown() {
        // set initial values
        value = 1;
        redirectMessage = `Redirecting in ${timeout} seconds`;

        // actual countdown
        for (
            let timeLeft = maximumTime;
            timeLeft >= 0;
            timeLeft -= timeoutIncrement
        ) {
            await delay(timeoutIncrement * 1000);
            if (redirectCancelled) {
                return;
            }

            value = timeLeft / timeout;
            redirectMessage = `Redirecting in ${Math.ceil(timeLeft)} seconds`;
        }

        // initiate redirect
        redirectNow();
    }

    onMount(async () => {
        countdown();
    });
</script>

<svelte:head>
    <title>Error {code}: {name}</title>
</svelte:head>

<main>
    <div>
        <Header title={`${code}`} subtitle={name} />
        <div class="container">
            <p>{message}</p>
        </div>
    </div>
    <footer>
        <div class="container redirect">
            <HorizontalProgress
                trails={!redirectCancelled}
                bind:value
                on:click={redirectNow}
            >
                <div class="line-clamp">{redirectMessage}</div>
            </HorizontalProgress>
            <button
                class="stop"
                class:hide={redirectCancelled}
                on:click={cancelRedirect}>STOP</button
            >
        </div>
        <Footer />
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

    p {
        font-size: 1.9rem;
        margin-top: 1rem;
        text-align: center;
    }

    .hide {
        display: none;
    }

    @media (min-width: 550px) {
        p {
            font-size: 2.2rem;
            text-align: start;
        }
    }

    /* REDIRECT STYLES */
    .redirect {
        display: flex;
        flex-direction: row;
    }

    .stop {
        border-radius: 0 4px 4px 0;
    }
</style>
