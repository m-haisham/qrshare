<script>
    import { BaseApp } from "../../components";
    import { HorizontalProgress } from "../../components/progressbars";
    import { ExclamationSquare, Github } from "../../module/icons";
    import { delay, openSource } from "../../helper";
    import { onMount } from "svelte";

    /* global values are retrieved
       these are values provided to html file in flask via jinja2 */
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
        /* this is set to stop the countdown */
        redirectCancelled = true;

        value = 0;
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
        /* set initial values */
        value = 1;
        redirectMessage = `Redirecting in ${timeout} seconds`;

        /* this begins the actual countdown */
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

        /* countdown has ended, initiate redirect */
        redirectNow();
    }

    onMount(async () => {
        countdown();
    });

    const navs = [
        {
            click: () => {},
            component: ExclamationSquare,
        },
        {
            click: openSource,
            component: Github,
        },
    ];
    const active = 0;
</script>

<svelte:head>
    <title>{code}: {name}</title>
</svelte:head>

<BaseApp title={code} subtitle={name} {navs} {active}>
    <div class="container">
        <p>{message}</p>
    </div>
    <div class="redirect">
        <div class="container">
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
    </div>
</BaseApp>

<style>
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

    .redirect {
        position: fixed;
        width: 100%;
        bottom: 5rem;
    }

    .redirect .container {
        display: flex;
        flex-direction: row;
    }

    @media (min-width: 550px) {
        .redirect {
            bottom: 0;
        }
    }

    .stop {
        border-radius: 0 4px 4px 0;
    }
</style>
