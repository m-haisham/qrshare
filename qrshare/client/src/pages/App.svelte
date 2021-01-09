<script>
	import { onMount } from "svelte";

	import Footer from "../components/Footer.svelte";
	import { currentRoute, routes, qrUrl } from "../store.js";
	import { jsonOrRedirect, toDataURL } from "../request.js";

	onMount(async () => {
		// get current routes
		let data = await jsonOrRedirect("/root");
		routes.set(data.routes);

		// set initial route
		let root = (({ routes, ...others }) => ({ ...others }))(data);
		currentRoute.set(root);

		// qrcode
		let url = await toDataURL("/svg");
		qrUrl.set(url);
	});
</script>

<style>
	main {
		height: 100vh;
		display: flex;
		flex-direction: column;
	}

	footer {
		margin-top: auto;
	}
</style>

<main>
	<div>
		<h1>Main1</h1>
	</div>
	<footer>
		<Footer />
	</footer>
</main>
