<script>
    export let msg;

    import { Header } from "../header";
    import Divider from "../Divider.svelte";
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
    .container {
        padding-top: 2rem;
    }

    input {
        margin-bottom: 0.2rem;
    }

    input,
    h6 {
        width: 100%;
        text-align: center;
    }

    .warn {
        border-color: var(--color-warning);
    }

    h6 {
        color: var(--color-warning);
    }

    button {
        width: 100%;
    }
</style>

<Header title="Auth" />
<Divider />
<div class="container">
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
