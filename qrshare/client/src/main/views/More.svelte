<script>
    import { Github } from "../../module/icons";
    import { ListGroup, ListTile } from "../../components/list";
    import { createLink } from "../../helper";
    import { meta } from "../store";

    const goTo = (href) => createLink(href).click();
    const source = () => goTo("https://github.com/mHaisham/qrshare");
    const issue = () =>
        goTo("https://github.com/mHaisham/qrshare/issues/new/choose");
</script>

<svelte:head>
    <title>More - qrshare</title>
</svelte:head>

<div class="container">
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
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
