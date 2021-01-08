<script>
	import createRouter from "@spaceavocado/svelte-router";
	import RouterView from "@spaceavocado/svelte-router/component/view.svelte";

	// Views
	import Page from "./pages/Page.svelte";

	createRouter({
		routes: [
			{
				path: "/",
				name: "Home",
				component: Page,
				props: {
					path: "root",
				},
			},
			{
				path: "/:path",
				name: "File&Folder",
				component: Page,
				props: (route) => {
					return {
						path: route.params.path,
					};
				},
			},
			{
				path: "*",
				component: "Not Found",
			},
		],
	});
</script>

<RouterView />
