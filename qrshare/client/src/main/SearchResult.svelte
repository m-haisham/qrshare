<script>
    import { isSearching, searchResults } from "./store";
    import { SearchListItem } from "./display";
    import { navigateTo } from "../module/router";

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

<style>
    .grid {
        display: grid;
        grid-template-columns: 100%;
        column-gap: 1rem;
    }

    @media (min-width: 550px) {
        .grid {
            grid-template-columns: 50% 50%;
        }
    }
</style>

<!-- Heading -->
{#if $isSearching}
    <h4>Searching... ({$searchResults.length})</h4>
{:else if $searchResults.length == 0}
    <h4>No matches found</h4>
{:else}
    <h4>Found {$searchResults.length} matches</h4>
{/if}

<!-- Results -->
<li class="grid">
    {#each $searchResults as route}
        <SearchListItem {route} on:folder={load} on:file={file} on:zip={zip} />
    {/each}
</li>
