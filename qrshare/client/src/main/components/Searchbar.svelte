<script>
    // components
    import { SwitchGroup } from "../../components/list";
    import OrderSelector from "./OrderSelector.svelte";

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
        const types = options.filter((v, i) => $searchInfo.types[i]);

        /* this checks if there are any search values */
        if ((query == null || query.trim() === "") && exts.length === 0) {
            return;
        }

        navigateTo({
            /* checks whether current route is root
               root search url is different from rest */
            id:
                $currentRoute.href == null || $currentRoute.href === "/"
                    ? 2
                    : 3,
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

<form on:submit|preventDefault={submit}>
    <fieldset disabled={$isSearching}>
        <label for="search-query">Query</label>
        <input type="text" id="search-query" bind:value={$searchInfo.query} />
        <label for="search-extensions">
            Extensions <span>[separated by space]</span>
        </label>
        <input type="text" bind:value={$searchInfo.extensions} />
        <label for="filter-types">Types <span>[Multiple]</span></label>
        <SwitchGroup
            id="filter-types"
            {options}
            selected={$searchInfo.types}
            on:toggle={toggle}
        />
        <OrderSelector />
        <button class="button-primary">SEARCH</button>
    </fieldset>
</form>

<style>
    form {
        grid-area: search;
        border-bottom: 1px solid var(--color-divider);
    }

    form,
    fieldset {
        margin: 0;
    }

    input {
        width: 100%;
        margin-bottom: 1rem;
        /* text-align: center; */
    }

    button {
        width: 100%;
    }

    .button-primary {
        margin-top: 1rem;
    }

    @media (min-width: 550px) {
        input {
            text-align: start;
        }

        button {
            width: auto;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }
    @media (min-width: 750px) {
        form {
            border-bottom: none;
        }
    }

    label span {
        font-size: 1.2rem;
        color: var(--color-subtitle);
    }
</style>
