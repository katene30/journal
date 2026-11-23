<script lang="ts">
	import { onMount } from 'svelte';
	import { isAuthenticated } from '$lib/stores/auth';
	import { entriesApi, type EntryListItem } from '$lib/api/entries';
	import EntryCard from '$lib/components/EntryCard.svelte';
	import NihoTaniwha from '$lib/components/NihoTaniwha.svelte';
	import ArrowRightIcon from '$lib/icons/ArrowRightIcon.svelte';

	let recentEntries = $state<EntryListItem[]>([]);
	let loadingEntries = $state(true);

	onMount(async () => {
		if ($isAuthenticated) {
			try {
				recentEntries = await entriesApi.recent();
			} catch (e) {
				console.error('Failed to load recent entries:', e);
			} finally {
				loadingEntries = false;
			}
		}
	});
</script>

<div class="home">
	<!-- Hero Section -->
	<section class="hero reading-column">
		<!-- Title, summary and buttons read as one block; the motif spans its height -->
		<div class="hero__content">
			<h1>Hauora Journal</h1>
			<p class="hero__subtitle">Holistic wellbeing tracking, rooted in te ao Māori</p>

			<div class="hero__actions">
				{#if $isAuthenticated}
					<a href="/app/new" class="btn btn--primary">
						New Entry <ArrowRightIcon />
					</a>
					<a href="/app/summary" class="btn btn--secondary">
						View Summary
					</a>
				{:else}
					<a href="/app/login" class="btn btn--primary">
						Login <ArrowRightIcon />
					</a>
					<a href="/app/register" class="btn btn--secondary">
						Sign Up
					</a>
				{/if}
			</div>
		</div>
		<div class="hero__motif">
			<div class="hero__motif-art">
				<NihoTaniwha />
			</div>
		</div>
	</section>

	<!-- Recent Entries (logged in only) -->
	{#if $isAuthenticated}
		<section class="section reading-column">
			<h2>Recent Entries</h2>
			{#if loadingEntries}
				<p class="loading">Loading...</p>
			{:else if recentEntries.length === 0}
				<p class="empty">No entries yet. Start journaling!</p>
			{:else}
				<div class="entries-grid">
					{#each recentEntries.slice(0, 3) as entry}
						<EntryCard {entry} />
					{/each}
				</div>
				<a href="/app/entries" class="view-all">View all entries →</a>
			{/if}
		</section>
	{/if}

	<!-- Features Section -->
	<section class="section reading-column">
		<h2>Features</h2>
		<div class="features-grid">
			<div class="feature-card">
				<h3>Track Your Hauora</h3>
				<p>Monitor your wellbeing across all dimensions — mind, body, family, spirit, identity, and environment.</p>
			</div>
			<div class="feature-card">
				<h3>Māori Health Framework</h3>
				<p>Built on Te Whare Tapa Whā and Te Pae Mahutonga — holistic models developed by Sir Mason Durie.</p>
			</div>
			<div class="feature-card">
				<h3>Journal with Metrics</h3>
				<p>Combine freeform journaling with structured data. Reflect on your day while tracking patterns over time.</p>
			</div>
			<div class="feature-card">
				<h3>Private & Secure</h3>
				<p>Your journal is yours. All data is stored securely and only accessible by you.</p>
			</div>
		</div>
	</section>

	<!-- About Section -->
	<section class="section reading-column">
		<h2>About</h2>

		<div class="about-content">
			<div class="about-block">
				<h3>Te Whare Tapa Whā</h3>
				<p>A Māori health model representing wellbeing as a wharenui (meeting house) with four walls. All walls must be strong for the house to stand:</p>
				<ul>
					<li><strong>Hinengaro</strong> — Mind, thoughts, emotions</li>
					<li><strong>Tinana</strong> — Body, physical health</li>
					<li><strong>Whānau</strong> — Family, social connections</li>
					<li><strong>Wairua</strong> — Spirit, meaning, purpose</li>
				</ul>
			</div>

			<div class="about-block">
				<h3>Te Pae Mahutonga</h3>
				<p>Uses the Southern Cross constellation as a framework for health promotion:</p>
				<ul>
					<li><strong>Mauriora</strong> — Cultural identity, access to te ao Māori</li>
					<li><strong>Waiora</strong> — Physical environment, connection to land</li>
				</ul>
			</div>

			<div class="about-block">
				<h3>How It Works</h3>
				<p>Each day, reflect on different aspects of your wellbeing using simple scales and journal prompts. Over time, see patterns and insights about what affects your hauora.</p>
			</div>
		</div>
	</section>

	<!-- Footer -->
	<footer class="footer reading-column">
		<p>Built with aroha in Aotearoa</p>
	</footer>
</div>

<style lang="scss">
	.home {
		min-height: 100vh;
	}

	.hero {
		--reading-max: 1000px;
		display: flex;
		align-items: stretch;
		gap: var(--space-xl);
		padding-block: var(--space-xxl) var(--space-lg);
		color: var(--color-text);
	}

	/* Home handles its own spacing. Scoped with :has so it doesn't leak to other pages */
	:global(.main:has(> .home)) {
		padding: 0;
	}

	.hero__content {
		flex: 0 1 auto;
		min-width: 0;
	}

	.hero h1 {
		font-size: clamp(2.25rem, 5vw, 3rem);
		margin: 0 0 var(--space-sm);
	}

	/* Takes the remaining width and stretches to the text block's height */
	.hero__motif {
		position: relative;
		flex: 1 1 0;
		min-width: 0;
		opacity: 0.6;

		/* No room beside the text on phones */
		@media (max-width: 767px) {
			display: none;
		}
	}

	/* Pinned to the block's top and bottom, less padding, and centred in the
	   space beside the text so it neither crowds nor drifts; width follows the artwork */
	.hero__motif-art {
		position: absolute;
		top: var(--space-sm);
		bottom: var(--space-sm);
		left: 50%;
		transform: translateX(-50%);
		aspect-ratio: 1825 / 944;
		max-width: 100%;
	}

	.hero__subtitle {
		font-size: var(--font-size-lg);
		color: var(--color-text-muted);
		margin-bottom: var(--space-xl);
	}

	.hero__actions {
		display: flex;
		justify-content: flex-start;
		gap: var(--space-sm);
		flex-wrap: wrap;
	}

	.section {
		--reading-max: 900px;
		padding-block: var(--space-xl);

		h2 {
			font-size: var(--font-size-heading);
			color: var(--color-text);
			margin-bottom: var(--space-lg);
		}
	}

	.entries-grid {
		display: grid;
		gap: var(--space-md);
		grid-template-columns: 1fr;

		@media (min-width: 600px) {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	.loading,
	.empty {
		text-align: center;
		color: var(--color-text-muted);
		padding: var(--space-lg);
	}

	.view-all {
		display: inline-block;
		margin-top: var(--space-md);
		color: var(--color-link);
	}

	.features-grid {
		display: grid;
		gap: var(--space-md);
		grid-template-columns: 1fr;

		@media (min-width: 500px) {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	.feature-card {
		background: var(--color-surface);
		padding: var(--space-lg);
		border-radius: var(--radius-lg);
		box-shadow: var(--shadow-sm);

		h3 {
			font-size: var(--font-size-base);
			color: var(--color-text);
			margin-bottom: var(--space-sm);
		}

		p {
			font-size: var(--font-size-sm);
			color: var(--color-text-muted);
			line-height: 1.6;
		}
	}

	.about-content {
		display: grid;
		gap: var(--space-lg);
	}

	.about-block {
		h3 {
			font-size: var(--font-size-lg);
			color: var(--color-text);
			margin-bottom: var(--space-sm);
		}

		p {
			color: var(--color-text-muted);
			line-height: 1.6;
			margin-bottom: var(--space-sm);
		}

		ul {
			list-style: none;
			padding: 0;
			margin: 0;
		}

		li {
			padding: var(--space-xs) 0;
			color: var(--color-text);

			strong {
				color: var(--color-text);
			}
		}
	}

	.footer {
		--reading-max: 900px;
		padding-block: var(--space-xl);
		color: var(--color-text-muted);
		font-size: var(--font-size-sm);
	}
</style>
