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

    function sort(e) {
        isSorted.flip();
    }
</script>

<svelte:head>
    <title>Search in ~{$currentRoute.href || "/"} - qrshare</title>
</svelte:head>

<!-- Searchbar -->
<SearchBar />

<!-- main body -->
<div class="container">
    <!-- Heading -->
    <div class="header">
        <h4>
            {#if $isSearching}
                Searching... ({$searchResults.length})
            {:else if $searchResults.length == 0}
                No matches found
            {:else}Found {$searchResults.length} matches{/if}
        </h4>
        <button disabled={$isSearching} on:click={sort}>
            {$isSorted ? "Relevance" : "Unsorted"}
        </button>
    </div>

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

    .header {
        display: flex;
        justify-content: space-between;
    }

    .header h4 {
        text-align: start;
        margin-bottom: 0;
    }

    @media (min-width: 550px) {
        .grid {
            grid-template-columns: repeat(2, calc(50% - 1rem / 2));
        }
    }
    .container {
        margin-top: 1rem;
    }

    @media (min-width: 550px) {
        .container {
            margin-top: 2rem;
        }
    }
</style>
