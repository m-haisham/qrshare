<script>
	import Home from "./pages/Home.svelte";
	import Footer from "./components/Footer.svelte";
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
		<Home />
	</div>
	<footer>
		<Footer />
	</footer>
</main>
