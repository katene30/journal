<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { isAuthenticated, currentUser, authActions } from '$lib/stores/auth';

	let menuOpen = $state(false);

	function toggleMenu() {
		menuOpen = !menuOpen;
	}

	function closeMenu() {
		menuOpen = false;
	}

	async function handleLogout() {
		await authActions.logout();
		closeMenu();
		goto('/app/login');
	}

	function isActive(path: string): boolean {
		const currentPath: string = $page.url.pathname;
		if (path === '/app') {
			return currentPath === '/app' || currentPath === '/app/';
		}
		return currentPath.startsWith(path);
	}
</script>

<header class="header">
	<div class="header__container">
		<a href="/app" class="header__brand" onclick={closeMenu}>
			Hauora Journal
		</a>

		{#if $isAuthenticated}
			<button
				class="header__toggle"
				type="button"
				aria-expanded={menuOpen}
				aria-controls="nav-menu"
				aria-label="Toggle navigation"
				onclick={toggleMenu}
			>
				<span class="header__toggle-bar"></span>
				<span class="header__toggle-bar"></span>
				<span class="header__toggle-bar"></span>
			</button>

			<nav
				id="nav-menu"
				class="header__nav"
				class:header__nav--open={menuOpen}
			>
				<ul class="header__nav-list">
					<li>
						<a
							href="/app"
							class="header__nav-link"
							class:header__nav-link--active={isActive('/app') && !isActive('/app/entries') && !isActive('/app/new') && !isActive('/app/summary')}
							onclick={closeMenu}
						>
							Home
						</a>
					</li>
					<li>
						<a
							href="/app/entries"
							class="header__nav-link"
							class:header__nav-link--active={isActive('/app/entries')}
							onclick={closeMenu}
						>
							Entries
						</a>
					</li>
					<li>
						<a
							href="/app/new"
							class="header__nav-link"
							class:header__nav-link--active={isActive('/app/new')}
							onclick={closeMenu}
						>
							New Entry
						</a>
					</li>
					<li>
						<a
							href="/app/summary"
							class="header__nav-link"
							class:header__nav-link--active={isActive('/app/summary')}
							onclick={closeMenu}
						>
							Summary
						</a>
					</li>
				</ul>

				<div class="header__user">
					<span class="header__user-name">
						{$currentUser?.first_name || $currentUser?.email || 'User'}
					</span>
					<button
						type="button"
						class="header__logout"
						onclick={handleLogout}
					>
						Logout
					</button>
				</div>
			</nav>
		{:else}
			<a href="/app/login" class="header__login">Login</a>
		{/if}
	</div>
</header>

<style lang="scss">
	.header {
		background: var(--color-moana);
		color: white;
	}

	.header__container {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--space-sm) var(--space-md);
		max-width: 1200px;
		margin: 0 auto;
	}

	.header__brand {
		font-size: var(--font-size-lg);
		font-weight: 600;
		color: white;
		text-decoration: none;

		&:hover {
			color: var(--color-kowhai);
		}
	}

	.header__toggle {
		display: flex;
		flex-direction: column;
		gap: 4px;
		padding: var(--space-xs);
		background: none;
		border: none;
		cursor: pointer;

		@media (min-width: 768px) {
			display: none;
		}
	}

	.header__toggle-bar {
		display: block;
		width: 24px;
		height: 2px;
		background: white;
		border-radius: 1px;
		transition: transform var(--transition-fast), opacity var(--transition-fast);
	}

	.header__toggle[aria-expanded='true'] {
		.header__toggle-bar:nth-child(1) {
			transform: translateY(6px) rotate(45deg);
		}
		.header__toggle-bar:nth-child(2) {
			opacity: 0;
		}
		.header__toggle-bar:nth-child(3) {
			transform: translateY(-6px) rotate(-45deg);
		}
	}

	.header__nav {
		display: none;
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background: var(--color-moana);
		padding: var(--space-md);
		box-shadow: var(--shadow-lg);

		@media (min-width: 768px) {
			display: flex;
			align-items: center;
			gap: var(--space-lg);
			position: static;
			padding: 0;
			box-shadow: none;
		}
	}

	.header__nav--open {
		display: block;

		@media (min-width: 768px) {
			display: flex;
		}
	}

	.header__nav-list {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);

		@media (min-width: 768px) {
			flex-direction: row;
			gap: var(--space-sm);
		}
	}

	.header__nav-link {
		display: block;
		padding: var(--space-sm) var(--space-md);
		color: rgba(255, 255, 255, 0.85);
		text-decoration: none;
		border-radius: var(--radius-sm);
		transition: background var(--transition-fast), color var(--transition-fast);

		&:hover {
			background: rgba(255, 255, 255, 0.1);
			color: white;
		}

		@media (min-width: 768px) {
			padding: var(--space-xs) var(--space-sm);
		}
	}

	.header__nav-link--active {
		background: rgba(255, 255, 255, 0.15);
		color: white;
	}

	.header__user {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		margin-top: var(--space-md);
		padding-top: var(--space-md);
		border-top: 1px solid rgba(255, 255, 255, 0.2);

		@media (min-width: 768px) {
			margin-top: 0;
			padding-top: 0;
			border-top: none;
			margin-left: auto;
		}
	}

	.header__user-name {
		font-size: var(--font-size-sm);
		color: rgba(255, 255, 255, 0.85);
	}

	.header__logout {
		padding: var(--space-xs) var(--space-sm);
		background: transparent;
		border: 1px solid rgba(255, 255, 255, 0.5);
		border-radius: var(--radius-sm);
		color: white;
		font-size: var(--font-size-sm);
		cursor: pointer;
		transition: background var(--transition-fast), border-color var(--transition-fast);

		&:hover {
			background: rgba(255, 255, 255, 0.1);
			border-color: white;
		}
	}

	.header__login {
		padding: var(--space-xs) var(--space-md);
		background: var(--color-kowhai);
		border-radius: var(--radius-sm);
		color: var(--color-whenua);
		text-decoration: none;
		font-weight: 500;
		transition: background var(--transition-fast);

		&:hover {
			background: var(--color-kowhai-light, #e0b54d);
		}
	}
</style>
