<script>
    import {
        isSearching,
        currentRoute,
        searchResults,
        isSorted,
        processedResults,
    } from "../store";
    import { SearchListItem } from "../components";
    import { navigateTo } from "../../module/router";
    import { createLink } from "../../helper";
    import SearchBar from "../components/Searchbar.svelte";

    let title = "No matches found";
    $: {
        if ($isSearching) title = `Searching... (${$searchResults.length})`;
        else if ($searchResults.length == 0) title = "No matches found";
        else title = `Found ${$searchResults.length} matches`;
    }

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

<!-- Searchbar -->
<SearchBar {title} />

<!-- main body -->
<div class="container">
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

<!-- main body -->
<style>
    .grid {
        display: grid;
        grid-template-columns: 100%;
        column-gap: 1rem;
    }
    @media (min-width: 550px) {
        .grid {
            grid-template-columns: repeat(2, calc(50% - 1rem / 2));
        }
    }
</style>
