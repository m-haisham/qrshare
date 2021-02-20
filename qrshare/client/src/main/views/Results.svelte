<script>
    import { onMount } from "svelte";
    import {
        title,
        subtitle,
        searchCollapsed,
        isSearching,
        currentRoute,
        searchResults,
        processedResults,
    } from "../store";
    import { SearchListItem } from "../components";
    import { createLink } from "../../helper";
    import SearchBar from "../components/Searchbar.svelte";

    $: {
        /* set title based on search state */
        if ($isSearching) {
            title.update(1, `Searching... (${$searchResults.length})`);
        } else if ($searchResults.length == 0) {
            title.update(1, "No matches found");
        } else {
            title.update(1, `Found ${$searchResults.length} matches`);
        }
    }

    onMount(() => {
        subtitle.set(1, $currentRoute.href ? "~" + $currentRoute.href : "~/");
    });

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
    <div class="content" class:collapsed={$searchCollapsed}>
        <!-- Searchbar -->
        <div class="search-bar">
            <SearchBar />
        </div>

        <!-- Results -->
        <ul class="grid">
            {#each $processedResults as route, i}
                <SearchListItem
                    id={i}
                    {route}
                    on:folder={load}
                    on:file={file}
                    on:zip={zip}
                />
            {/each}
        </ul>
    </div>
</div>

<!-- main body -->
<style>
    .container {
        margin-top: 1rem;
        margin-bottom: 1rem;
        height: 100%;
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

    .search-bar {
        grid-area: search;
    }

    .grid {
        grid-area: results;

        display: grid;
        grid-template-columns: 100%;
        column-gap: 1rem;

        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    @media (min-width: 750px) {
        .content :global(form) {
            border-bottom: none;

            /* hack to give form an fixed height */
            position: sticky;
            position: -webkit-sticky;
            top: 10.3rem;
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
    .collapsed .search-bar {
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
