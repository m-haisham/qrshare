<script>
    import { AppBar, BottomNavigationBar } from "./navigation";

    export let title;
    export let subtitle = null;
    export let navs = [];
    export let active = null;
    export let sticky = false;
</script>

<main>
    <AppBar {title} {subtitle} {navs} {active} {sticky} />
    <slot />
    <BottomNavigationBar {navs} {active} />
</main>

<style>
    main {
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
</style>
