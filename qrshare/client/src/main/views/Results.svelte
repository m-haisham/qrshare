<script>
    import {
        isSearching,
        currentRoute,
        searchResults,
        processedResults,
    } from "../store";
    import { SearchListItem } from "../components";
    import { Collapsible } from "../../components";
    import { Funnel } from "../../module/icons";
    import { navigateTo } from "../../module/router";
    import { createLink } from "../../helper";
    import SearchBar from "../components/Searchbar.svelte";

    let title = "No matches found";
    $: {
        if ($isSearching) title = `Searching... (${$searchResults.length})`;
        else if ($searchResults.length == 0) title = "No matches found";
        else title = `Found ${$searchResults.length} matches`;
    }

    let collapsed = false;
    const collapse = () => (collapsed = !collapsed);

    function load(e) {
        const route = e.detail;
        navigateTo({ id: 1, url: route.href, state: route, name: route.name });
    }

    function file(e) {
        createLink(e.detail.path).click();
    }

    function zip(e) {
        createLink(e.detail.zip).click();
    }
</script>

<svelte:head>
    <title>Search in ~{$currentRoute.href || "/"} - qrshare</title>
</svelte:head>

<!-- main body -->
<div class="container">
    <Collapsible {title} icon={Funnel} hide={collapsed} on:click={collapse} />

    <div class="content" class:collapsed>
        <!-- Searchbar -->
        <SearchBar />

        <!-- Results -->
        <li class="grid">
            {#each $processedResults as route, i}
                <SearchListItem
                    id={i}
                    {route}
                    on:folder={load}
                    on:file={file}
                    on:zip={zip}
                />
            {/each}
        </li>
    </div>
</div>

<!-- main body -->
<style>
    .container {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .content {
        display: grid;
        grid-template-columns: repeat(2, calc(50% - 0.5rem));
        grid-template-rows: auto auto;
        grid-template-areas:
            "search search"
            "results results";
        column-gap: 1rem;
    }

    .content :global(form) {
        grid-area: search;
    }

    .grid {
        grid-area: results;

        display: grid;
        grid-template-columns: 100%;
        column-gap: 1rem;

        margin-top: 1rem;
    }
    @media (min-width: 750px) {
        .content :global(form) {
            border-bottom: none;

            /* hack to give form an fixed height */
            height: calc(100vh - 16rem);
            position: sticky;
            top: 12rem;
        }
        .grid {
            grid-area: auto;
            padding-top: 0.9rem;
        }
        .content {
            grid-template-columns:
                calc(100% - 240px - 0.5rem)
                calc(240px - 0.5rem);
            grid-template-rows: auto auto;
            grid-template-areas:
                "results search"
                "results search";
        }
    }

    @media (min-width: 1000px) {
        .grid {
            grid-template-columns: repeat(2, calc(50% - 1rem / 2));
            margin-top: 2rem;
        }
    }

    /* collapsing */
    .collapsed :global(form) {
        display: none;
    }

    @media (min-width: 750px) {
        .collapsed {
            grid-template-columns: 100%;
        }

        .collapsed .grid {
            grid-template-columns: repeat(2, calc(50% - 1rem / 2));
            margin-top: 2rem;
        }
    }
</style>
