<script>
	import PageTest from "../pages/PageTest.svelte";
	import { example as data } from "../ex.js";

	console.log(data);
</script>

<PageTest {data} />
