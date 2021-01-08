<script>
    import { Header } from "../header";
    import Divider from "../Divider.svelte";
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    let value;
    function submit() {
        if (value) dispatch("submit", { value });
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
        width: 100%;
        text-align: center;
    }

    button {
        width: 100%;
    }
</style>

<Header title="Auth" />
<Divider />
<div class="container">
    <form>
        <input type="password" bind:value use:init />
        <button
            type="button"
            class="button-primary"
            on:click={submit}>Submit</button>
    </form>
</div>
