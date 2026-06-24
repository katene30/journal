<script lang="ts">
	import '$lib/scss/main.scss';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { authActions, authLoading, isAuthenticated } from '$lib/stores/auth';
	import Header from '$lib/components/Header.svelte';

	let { children } = $props();

	const publicRoutes = ['/app/login', '/app/register'];

	const isPublicRoute = $derived(publicRoutes.some(route => $page.url.pathname.startsWith(route)));

	onMount(() => {
		authActions.checkAuth();
	});

	$effect(() => {
		const path = $page.url.pathname;
		const isPublicRoute = publicRoutes.some(route => path.startsWith(route));

		if (!$authLoading) {
			if (!$isAuthenticated && !isPublicRoute) {
				goto('/app/login');
			} else if ($isAuthenticated && isPublicRoute) {
				goto('/app');
			}
		}
	});
</script>

<svelte:head>
	<title>Hauora Journal</title>
	<meta name="description" content="Track your wellbeing across Te Whare Tapa Whā" />
</svelte:head>

{#if $authLoading}
	<div class="loading-screen">Loading...</div>
{:else}
	<a href="#main-content" class="skip-link">Skip to main content</a>

	<div class="page">
		{#if !isPublicRoute && $isAuthenticated}
			<Header />
		{/if}
		<main id="main-content" class="main">
			{@render children()}
		</main>
	</div>
{/if}

<style>
	.loading-screen {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		color: var(--color-text-muted);
	}
</style>
