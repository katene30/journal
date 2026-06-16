<script lang="ts">
	import '$lib/scss/main.scss';

	let { children } = $props();
</script>

<svelte:head>
	<title>Hauora Journal</title>
	<meta name="description" content="Track your wellbeing across Te Whare Tapa Whā" />
</svelte:head>

<a href="#main-content" class="skip-link">Skip to main content</a>

<div class="page">
	<main id="main-content" class="main">
		{@render children()}
	</main>
</div>
