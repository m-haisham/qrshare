<script>
    export let value;
    export let disabled;

    import { SizedBox } from "../../utilities";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    $: expanded = Boolean.valueOf(value) && value !== "";

    function submit(e) {
        e.preventDefault();

        if (value && !disabled) {
            dispatch("submit", { query: value });
        }
    }
</script>

<style>
    form {
        display: flex;
        flex-direction: column;
        margin-bottom: auto;
    }

    input {
        width: 100%;
        box-sizing: border-box;
        text-align: center;
        margin-bottom: 1rem;
    }

    button {
        width: 100%;
        box-sizing: border-box;
    }

    .disabled {
        opacity: 0.5;
    }

    @media (min-width: 550px) {
        form {
            flex-direction: row;
        }

        input {
            width: auto;
            text-align: start;
            margin-bottom: auto;
            border-top-right-radius: 0;
            border-bottom-right-radius: 0;
            transition: width 100ms ease;
        }
        button {
            width: auto;
            margin-left: -2rem;
            border-top-left-radius: 0;
            border-bottom-left-radius: 0;
        }
    }

    /* Larger than tablet */
    @media (min-width: 750px) {
        input {
            width: 20rem;
            transition: width 100ms ease;
        }

        input:focus,
        .expanded {
            width: 30rem;
        }
    }
</style>

<form on:submit={submit} class:disabled>
    <input type="text" bind:value {disabled} class:expanded />
    <SizedBox width="2rem" />
    <button class="header-button" type="submit" value="submit">Search</button>
</form>
