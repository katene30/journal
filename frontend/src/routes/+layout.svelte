<script lang="ts">
	import '$lib/scss/main.scss';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { authActions, authLoading, isAuthenticated } from '$lib/stores/auth';
	import Header from '$lib/components/Header.svelte';

	let { children } = $props();

	// Signed-in users are sent home from these
	const authRoutes = ['/app/login', '/app/register', '/app/forgot-password', '/app/reset-password'];
	// Anyone can view these, signed in or not
	const openRoutes = ['/app/privacy'];

	const matches = (routes: string[], path: string) => routes.some((route) => path.startsWith(route));

	const isAuthRoute = $derived(matches(authRoutes, $page.url.pathname));

	onMount(() => {
		authActions.checkAuth();
	});

	$effect(() => {
		const path = $page.url.pathname;
		if ($authLoading || matches(openRoutes, path)) return;

		const isAuthRoute = matches(authRoutes, path);
		if (!$isAuthenticated && !isAuthRoute) {
			goto('/app/login');
		} else if ($isAuthenticated && isAuthRoute) {
			goto('/app');
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
		{#if !isAuthRoute && $isAuthenticated}
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
