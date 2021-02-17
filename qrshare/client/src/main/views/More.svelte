<script>
    import { Github } from "../../module/icons";
    import { fetchOrRedirect } from "../../request";
    import { ListGroup, ListTile } from "../../components/list";
    import { createLink } from "../../helper";
    import { meta } from "../store";

    const goTo = (href) => window.open(href);
    const source = () => goTo("https://github.com/mHaisham/qrshare");
    const issue = () =>
        goTo("https://github.com/mHaisham/qrshare/issues/new/choose");

    /** logout the client from current session and redirect to auth screen */
    function logout() {
        fetchOrRedirect("/logout", "POST");
    }
</script>

<svelte:head>
    <title>More - qrshare</title>
</svelte:head>

<div class="container">
    {#if $meta.login}
        <ListGroup title="Client">
            <ListTile on:click={logout} disabled={false}>Logout</ListTile>
        </ListGroup>
    {/if}
    <ListGroup title="Server">
        <ListTile>
            IP Address
            <div name="trailing">{$meta.ip}</div>
        </ListTile>
    </ListGroup>
    <ListGroup title="About">
        <ListTile on:click={source} disabled={false}>
            Source
            <div name="trailing" class="icon"><Github /></div>
        </ListTile>
        <ListTile on:click={issue} disabled={false}>
            Issue
            <div name="trailing" class="icon"><Github /></div>
        </ListTile>
        <ListTile>
            Version
            <div name="trailing">v{$meta.version}</div>
        </ListTile>
    </ListGroup>
</div>

<style>
    .container {
        margin-bottom: 1rem;
    }
</style>
