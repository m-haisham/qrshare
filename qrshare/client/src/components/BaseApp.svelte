<script>
    import { AppBar, BottomNavigationBar } from "./navigation";

    export let title;
    export let subtitle = null;
    export let navs = [];
    export let active = null;
    export let actionStates = [];
    export let sticky = false;

    /* NavigationElements takes an array of booleans representing icons that are active */
    $: navStates = Array.from({ length: navs.length }, (v, i) => i === active);
</script>

<main>
    <AppBar
        {title}
        {subtitle}
        {navs}
        {navStates}
        {active}
        {actionStates}
        {sticky}
    />
    <slot />
    <BottomNavigationBar {navs} {navStates} />
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
    }
</style>
