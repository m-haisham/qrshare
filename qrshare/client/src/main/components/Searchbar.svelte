<script>
    // components
    import { SwitchGroup } from "../../components/buttons";
    import Collapsible from "../../components/Collapsible.svelte";
    import Divider from "../../components/Divider.svelte";

    // state values
    import { currentRoute, isSearching, searchInfo } from "../store";

    // functions
    import { createSearchUrl } from "../../helper";
    import { navigateTo } from "../../module/router";

    const options = ["is_file", "is_dir"];
    function toggle(e) {
        const { index } = e.detail;
        searchInfo.update((info) => ({
            ...info,
            types: info.types.map((v, i) => (index == i ? !v : v)),
        }));
    }

    function submit(e) {
        // query
        const query = $searchInfo.query ? $searchInfo.query : null;
        const exts = $searchInfo.extensions.split(" ").filter((v) => v);
        const types = $searchInfo.types;

        /* this checks if there are any search values */
        if ((query == null || query.trim() === "") && exts.length === 0) {
            return;
        }

        navigateTo({
            id: $currentRoute.href === "/" ? 2 : 3,
            url: createSearchUrl({
                path: $currentRoute.href,
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
                        bind:value={$searchInfo.query}
                    />
                    <div class="more">
                        <input
                            type="text"
                            placeholder="Extensions"
                            bind:value={$searchInfo.extensions}
                        />
                        <SwitchGroup
                            {options}
                            selected={$searchInfo.types}
                            on:toggle={toggle}
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
