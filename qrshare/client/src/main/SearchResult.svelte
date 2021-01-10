<script>
    import { isSearching, searchResults } from "./store";
    import { SearchListItem } from "./display";
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

<h4>{$searchResults.length} Results</h4>
<li class="grid">
    {#each $searchResults as route}
        <ul>
            <SearchListItem {route} />
        </ul>
    {/each}
</li>
