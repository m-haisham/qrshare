<script>
    // components
    import { SwitchGroup } from "../../components/buttons";
    import Collapsible from "../../components/Collapsible.svelte";
    import Divider from "../../components/Divider.svelte";

    // state values
    import {
        currentRoute as current,
        isSearching,
        searchQuery,
    } from "../store";

    // functions
    import { createSearchUrl } from "../../helper";
    import { navigateTo } from "../../module/router";

    let types = [];
    let extensions = "";

    function submit(e) {
        // query
        const query = $searchQuery ? $searchQuery : null;
        const exts = extensions.split(" ").filter((v) => v);

        navigateTo({
            id: $current.href === undefined ? 2 : 3,
            url: createSearchUrl({
                path: $current.href,
                query,
                exts,
                types,
            }),
            name: "Search",
        });
    }
</script>

<div class="stick">
    <div class="container">
        <Collapsible textH="OPTIONS" secondary={true}>
            <form on:submit|preventDefault={submit}>
                <fieldset disabled={$isSearching}>
                    <input
                        type="text"
                        placeholder="Search"
                        bind:value={$searchQuery}
                    />
                    <div class="more">
                        <input
                            type="text"
                            placeholder="Extensions"
                            bind:value={extensions}
                        />
                        <SwitchGroup
                            options={["is_file", "is_dir"]}
                            initial={true}
                            bind:selected={types}
                        />
                    </div>
                    <button>SEARCH</button>
                </fieldset>
            </form>
        </Collapsible>
    </div>
    <Divider />
</div>

<style>
    .container {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    form,
    fieldset {
        margin: 0;
    }

    input {
        width: 100%;
        margin-bottom: 1rem;
        text-align: center;
    }

    button {
        width: 100%;
    }

    @media (min-width: 550px) {
        input {
            text-align: start;
        }

        button {
            width: auto;
            padding-left: 2rem;
            padding-right: 2rem;
            margin-bottom: 0;
        }
    }

    /* STYLE MORE OPTIONS */
    .more {
        display: flex;
        flex-direction: column;
    }

    @media (min-width: 550px) {
        .more {
            flex-direction: row;
            gap: 1rem;
        }

        .more > *:first-child {
            flex-grow: 8;
        }

        .more > *:last-child {
            flex-grow: 4;
        }
    }
</style>
