<script>
    export let msg;

    import { Title } from "../typography";
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    let value;
    function submit() {
        if (value) dispatch("submit", { value });
    }

    // error indicators
    $: warn = Boolean.valueOf(msg) && msg !== "";
    function change() {
        if (value) {
            msg = "";
        } else {
            msg = "Required";
        }
    }

    function init(e) {
        e.focus();
    }
</script>

<style>
    form {
        margin-bottom: 1rem;
        min-width: 300px;
    }

    input {
        width: 100%;
        margin-bottom: 0.2rem;
    }

    .warn {
        border-color: var(--color-warning);
    }

    h6 {
        color: var(--color-warning);
    }

    @media (min-width: 550px) {
        .content {
            padding: 2rem;
            border: 2px solid var(--color-light-dark);
            border-radius: 1rem;

            margin: 0;
            position: absolute;
            top: calc(50% - 6rem);
            left: 50%;
            -ms-transform: translate(-50%, -50%);
            transform: translate(-50%, -50%);
        }
    }
</style>

<div class="content">
    <Title>Auth</Title>
    <form>
        <input
            type="password"
            class:warn
            on:change={change}
            bind:value
            use:init />
        <h6>{msg}</h6>
        <button
            type="button"
            class="button-primary"
            on:click={submit}>Submit</button>
    </form>
</div>
