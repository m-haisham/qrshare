<script>
	import { onMount } from "svelte";

	import Footer from "../components/Footer.svelte";
	import Content from "../views/Content.svelte";
	import Global from "../components/Global.svelte";
	import { updateStore, qrUrl } from "../store";
	import { jsonOrRedirect, toDataURL } from "../request.js";

	onMount(async () => {
		// get current routes
		updateStore("/root");

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

<Global>
	<main>
		<div>
			<Content />
		</div>
		<footer>
			<Footer />
		</footer>
	</main>
</Global>
