<script>
    import { AppBar, BottomNavigationBar } from "../../components/navigation";
    import { openSource } from "../../helper";
    import { DoorClosed, Key, Github } from "../../module/icons";
    import { request } from "../../request";

    let msg = "";
    let value;
    async function auth(e) {
        if (!value) {
            msg = "This field is required";
            return;
        }

        const response = await request(`/login?key=${value}`, "POST");

        /* when request redirects it wont return any response
           this prevents from throwing an error when trying converting to json */
        if (response) {
            const data = await response.json();
            msg = data ? data.msg : "The key does not match, try again.";
        }
    }

    /** when input changes, clear the error */
    const change = (e) => (msg = "");

    /** give focus to element */
    const focus = (e) => e.focus();

    const navs = [
        {
            click: () => {},
            component: Key,
        },
        {
            click: openSource,
            component: Github,
        },
    ];

    /* active navigation value does not change */
    const active = 0;
</script>

<main>
    <AppBar title="Locked" {navs} {active} sticky={true} />
    <div class="content">
        <div class="container">
            <DoorClosed />
            <h4>Knock Knock ...</h4>
            <form action="Submit" on:submit|preventDefault={auth}>
                <input
                    type="password"
                    name="code"
                    class:warn={msg}
                    bind:value
                    on:change={change}
                    use:focus
                />
                <div class="error-message">
                    {msg}
                </div>
                <button class="button-primary">Submit</button>
            </form>
        </div>
    </div>
    <BottomNavigationBar {navs} {active} />
</main>

<style>
    main {
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .content {
        width: 100%;

        /* center the elements */
        position: absolute;
        top: 50%;
        left: 50%;
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
    }

    @media (min-width: 550px) {
        .content {
            width: 400px;
        }
    }

    h4 {
        margin: 1rem 0;
    }

    input {
        display: block;
        width: 100%;
        margin: 0;
    }

    button {
        margin: 1.5rem 0;
    }

    .container :global(svg) {
        height: 5rem;
        width: 5rem;
    }

    .error-message {
        color: var(--color-warning);
    }

    .warn,
    .warn:focus {
        border-color: var(--color-warning);
    }
</style>
