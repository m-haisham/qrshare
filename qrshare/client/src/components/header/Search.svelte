<script>
    export let onClick;

    import { SizedBox } from "../../utilities";

    let value = "";
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

    @media (min-width: 550px) {
        form {
            flex-direction: row;
        }

        input {
            width: auto;
            text-align: start;
            margin-bottom: auto;
        }
    }
</style>

<form>
    <input type="text" bind:value placeholder="Query" />
    <SizedBox width="2rem" />
    <button
        class="header-button"
        type="button"
        on:click={onClick(value)}>Search</button>
</form>
