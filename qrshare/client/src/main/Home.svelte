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

    $: inSearch = $activeRoute.id === 2;
    $: title = inSearch ? "Search" : $current.name;
    $: subtitle =
        !inSearch && $current.parent ? "~" + $current.parent.href : null;

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
    }
</script>

<svelte:head>
    <title>{title}</title>
</svelte:head>

<Header {title} {subtitle}>
    <HeaderExtension>
        <Search on:submit={search} disabled={$isSearching} {value} />
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
<Divider />
<div class="container">
    <Router {routes} {options} />
</div>

<style>
    .container {
        margin-top: 1rem;
    }

    @media (min-width: 550px) {
        .container {
            margin-top: 2rem;
        }
    }
</style>
