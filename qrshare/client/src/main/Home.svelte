<script>
    import { Router } from "../module/router";
    import { routes, options } from "./routes";
    import { Header, HeaderExtension, Search } from "../components/header";
    import { SizedBox } from "../utilities";
    import { currentRoute as current, isSearching } from "./store";
    import Divider from "../components/Divider.svelte";
    import { createLink, createSearchUrl } from "../helper";
    import { navigateTo, activeRoute } from "../module/router";

    let value = "";

    $: inSearch = $activeRoute.key === 1;

    let title;
    let subtitle;

    // determines whether menu is open
    let expanded = false;

    // reset variables depending on state
    $: {
        // reset title
        title = inSearch ? "Search" : $current.name;

        // reset subtitle
        if (inSearch && $current.href) {
            subtitle = "~" + $current.href;
        } else if ($current.parent) {
            subtitle = "~" + $current.parent.href;
        } else {
            subtitle = null;
        }
    }

    function currentZip() {
        createLink($current.zip).click();
    }

    function home() {
        navigateTo({ id: 0, state: { path: "/root" } });
    }

    function search(e) {
        navigateTo({
            id: $current.href === undefined ? 2 : 3,
            url: createSearchUrl({
                path: $current.href,
                query: e.detail.query,
            }),
            name: "Search",
        });

        // close the menu when navigating to search menu
        expanded = false;
    }
</script>

<svelte:head>
    <title>{title}</title>
</svelte:head>

<Header {title} {subtitle}>
    <HeaderExtension bind:show={expanded}>
        <!-- There is a more advanced searchbar available in search -->
        {#if !inSearch}
            <Search on:submit={search} disabled={$isSearching} {value} />
        {/if}

        <SizedBox width="4rem" />

        {#if inSearch}
            <button class="u-full-width header-button" on:click={home}
                >Home</button
            >
        {:else}
            <button class="u-full-width header-button" on:click={currentZip}
                >Zip</button
            >
        {/if}
    </HeaderExtension>
</Header>
<Router {routes} {options} />
