<script>
    // components
    import { ButtonGroup, SwitchGroup } from "../../components/list";
    import OrderSelector from "./OrderSelector.svelte";

    // state values
    import {
        currentRoute,
        searchCollapsed,
        isSearching,
        searchInfo,
    } from "../store";

    // functions
    import { createSearchUrl } from "../../helper";
    import { navigateTo } from "../../module/router";

    let errors = { query: false, exts: false, limit: "" };
    const hasErrors = () => Object.values(errors).some((v) => v);

    const options = ["is_file", "is_dir"];

    /** always ensure there is always one type selected */
    function toggle(e) {
        const { index } = e.detail;

        let types = $searchInfo.types;

        /* count number of true values in group */
        const truthfull = types.reduce((a, v) => a + (v ? 1 : 0), 0);

        if (truthfull === 1 && types[index]) {
            /* gets the next index */
            const other = (index + 1) % options.length;

            /* unselect current and select next */
            types[index] = false;
            types[other] = true;
        } else {
            /* just a simple flip */
            types[index] = !types[index];
        }

        searchInfo.update((info) => ({ ...info, types }));
    }

    function submit(e) {
        const query = $searchInfo.query ? $searchInfo.query : null;
        const exts = $searchInfo.extensions.split(" ").filter((v) => v);
        const types = options.filter((v, i) => $searchInfo.types[i]);
        const limit = $searchInfo.limit;

        /* query and extensions validation, atleast one of the fields must be filled */
        if ((query == null || query.trim() === "") && exts.length === 0) {
            errors = { ...errors, query: true, exts: true };
        } else {
            errors = { ...errors, query: false, exts: false };
        }

        /* limit must be greator than 0 */
        if (!limit) {
            errors = { ...errors, limit: "[Required]" };
        } else if (limit <= 0) {
            errors = { ...errors, limit: "[Must be greator than 0]" };
        } else {
            errors = { ...errors, limit: "" };
        }

        /* gate keeping, no errors shall here forth */
        if (hasErrors()) {
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
                limit,
            }),
            name: "Search",
        });
    }

    const buttons = [
        {
            text: "Search",
            click: submit,
            primary: true,
        },
        {
            text: "+hide",
            click: (e) => {
                /* we manually call submit so we may check for errors afterwards */
                e.preventDefault();
                submit(e);

                /* this checks if there are any erros
                   and hides search bar only if there are none */
                if (!hasErrors()) {
                    searchCollapsed.set(true);
                }
            },
        },
    ];
</script>

<form on:submit|preventDefault={submit}>
    <fieldset disabled={$isSearching}>
        <!-- query -->
        <label for="search-query">Query</label>
        <input
            type="text"
            id="search-query"
            bind:value={$searchInfo.query}
            class:error={errors.query}
        />

        <!-- extensions -->
        <label for="search-extensions">
            Extensions <span>[separated by space]</span>
        </label>
        <input
            type="text"
            bind:value={$searchInfo.extensions}
            class:error={errors.exts}
        />

        <!-- route types -->
        <label for="filter-types">Types <span>[Multiple]</span></label>
        <SwitchGroup
            id="filter-types"
            {options}
            selected={$searchInfo.types}
            on:toggle={toggle}
        />

        <!-- limit -->
        <label for="result-limit">
            Limit <span class="error">{errors.limit}</span>
        </label>
        <input
            type="number"
            id="result-limit"
            bind:value={$searchInfo.limit}
            class:error={$searchInfo.limit <= 0}
        />

        <!-- order by -->
        <OrderSelector />

        <!-- action buttons [search] -->
        <ButtonGroup {buttons} />
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

    input.error {
        border-color: var(--color-warning);
    }

    form :global(.button-group) {
        margin-top: 2rem;
    }

    @media (min-width: 550px) {
        input {
            text-align: start;
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

    label span.error {
        color: var(--color-warning);
    }
</style>
