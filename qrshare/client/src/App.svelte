<script>
	import Home from "./pages/Home.svelte";
	import Footer from "./components/Footer.svelte";
</script>

<style>
	:global(:root) {
		--color-light: #f1f1f1;
		--color-light-dark: #ccc;
		--color-dark: #222222;
		--color-warning: #cc3300;
	}

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
		<Home />
	</div>
	<footer>
		<Footer />
	</footer>
</main>
