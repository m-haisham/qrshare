<script>
    import { Title } from "../typography";
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
    form {
        margin-bottom: 1rem;
    }

    input {
        width: 100%;
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
        <input type="password" bind:value use:init />
        <button
            type="button"
            class="button-primary"
            on:click={submit}>Submit</button>
    </form>
</div>
