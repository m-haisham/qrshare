<script>
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";
    import { Github } from "../../../module/icons";
    import { request } from "../../../request";
    import { ListGroup, ListTile } from "../../../components/list";
    import { openSource } from "../../../helper";
    import { title, subtitle, meta } from "../store";

    onMount(() => {
        title.set(3, "More");
        subtitle.set(3, null);
    });

    function issue() {
        window.open("https://github.com/mHaisham/qrshare/issues/new/choose");
    }

    /** logout the client from current session and redirect to auth screen */
    function logout() {
        request("/logout", "POST");
    }
</script>

<svelte:head>
    <title>More - qrshare</title>
</svelte:head>

<div class="container" in:fade={{ duration: 100 }}>
    {#if $meta.login}
        <ListGroup title="Client">
            <ListTile on:click={logout} disabled={false}>Logout</ListTile>
        </ListGroup>
    {/if}
    <ListGroup title="Server">
        <ListTile>
            IP Address
            <div name="trailing">{$meta.ip ?? ""}</div>
        </ListTile>
    </ListGroup>
    <ListGroup title="About">
        <ListTile on:click={openSource} disabled={false}>
            Source
            <div name="trailing" class="icon"><Github /></div>
        </ListTile>
        <ListTile on:click={issue} disabled={false}>
            Issue
            <div name="trailing" class="icon"><Github /></div>
        </ListTile>
        <ListTile>
            Version
            <div name="trailing">v{$meta.version ?? "?"}</div>
        </ListTile>
    </ListGroup>
</div>

<style>
    .container {
        margin-bottom: 1rem;
    }
</style>
