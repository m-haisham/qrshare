<script>
    import { AppBar, BottomNavigationBar } from "../components/navigation";
    import { HorizontalProgress } from "../components/progressbars";
    import { ExclamationSquareFill, Github } from "../module/icons";
    import { delay, openSource } from "../helper";
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

    const navs = [
        {
            click: () => {},
            component: ExclamationSquareFill,
        },
        {
            click: openSource,
            component: Github,
        },
    ];
    const active = 0;
</script>

<svelte:head>
    <title>Error {code}: {name}</title>
</svelte:head>

<main>
    <AppBar title={code} subtitle={name} {navs} {active} />
    <div class="container">
        <p>{message}</p>
    </div>
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
    <BottomNavigationBar {navs} {active} />
</main>

<style>
    main {
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    p {
        font-size: 1.9rem;
        margin-top: 1rem;
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

        margin-top: auto;
    }

    .stop {
        border-radius: 0 4px 4px 0;
    }
</style>
