<script lang="ts">
	import { isAuthenticated } from '$lib/stores/auth';

	const LAST_UPDATED = '23 November 2026';
	const CONTACT = 'hauorajournal@gmail.com';
</script>

<svelte:head>
	<title>Privacy policy · Hauora Journal</title>
</svelte:head>

<article class="privacy">
	<p class="privacy__back">
		{#if $isAuthenticated}
			<a href="/app/account">← Back to your account</a>
		{:else}
			<a href="/app/login">← Back to sign in</a>
		{/if}
	</p>

	<h1>Privacy policy</h1>
	<p class="privacy__updated">Last updated {LAST_UPDATED}</p>

	<p class="privacy__lead">
		Your journal is personal. This page explains, in plain language, what Hauora Journal stores,
		where it's kept, who can see it, and how you stay in control of it.
	</p>

	<section>
		<h2>Who we are</h2>
		<p>
			Hauora Journal is a small, independent project run from Aotearoa New Zealand. It isn't a
			company and doesn't make money from your data. We follow the New Zealand Privacy Act 2020.
		</p>
		<p>Questions or requests: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
	</section>

	<section>
		<h2>What we store</h2>
		<ul>
			<li><strong>Your email address</strong>, to sign you in and send password reset links.</li>
			<li>
				<strong>Your password</strong>, stored only as a one-way hash. Nobody, including us, can
				read it.
			</li>
			<li>
				<strong>Your journal entries</strong>: the ratings, notes and reflections you write, and
				when you wrote them.
			</li>
			<li>
				<strong>When you joined and last signed in</strong>.
			</li>
		</ul>
		<p>
			That's all. We don't ask for your name, location, or anything else, and the app has no
			advertising or analytics trackers.
		</p>
	</section>

	<section>
		<h2>Cookies</h2>
		<p>The app uses two cookies, both needed for it to work:</p>
		<ul>
			<li><strong>sessionid</strong> keeps you signed in.</li>
			<li><strong>csrftoken</strong> protects your account from forged requests by other websites.</li>
		</ul>
		<p>There are no tracking, advertising, or third-party cookies.</p>
	</section>

	<section>
		<h2>Where your data is kept</h2>
		<p>
			Your data is stored in a database run by <strong>Neon</strong>, and the app runs on
			<strong>Google Cloud</strong>. Both are in Sydney, Australia. Data is encrypted while it
			travels between your device and the app (HTTPS), and while it's stored.
		</p>
		<p>
			Password reset emails are sent through <strong>Gmail</strong>. Only your email address
			and the reset link pass through it, never your journal.
		</p>
		<p>
			Like most websites, the server keeps short-term technical logs of requests (such as IP
			address, browser type, and which page was requested) to keep the service running and
			secure. Your journal writing is never included in these logs, and they're deleted
			automatically after about 30 days.
		</p>
	</section>

	<section>
		<h2>Who can see your journal</h2>
		<p>
			Only you, through your account. Your entries are never sold, shared, or shown to other
			users, and aren't used for advertising.
		</p>
		<p>
			To be open with you: entries aren't end-to-end encrypted, so the person who runs Hauora
			Journal can technically access the database. We only do so when needed to fix a problem
			or when you ask us to, and never to read entries out of curiosity. We'll only hand data
			to anyone else if New Zealand law requires it.
		</p>
		<p>
			Your entries aren't sent to AI services or used to train AI. If AI features are ever
			added, they'll be optional and this policy will be updated before they launch.
		</p>
	</section>

	<section>
		<h2>Your rights and choices</h2>
		<ul>
			<li>
				<strong>See and download everything.</strong> On your
				<a href="/app/account">Account</a> page you can download all your data as a
				spreadsheet or a full export.
			</li>
			<li><strong>Correct it.</strong> You can edit or update any entry at any time.</li>
			<li>
				<strong>Delete it.</strong> You can permanently delete your account and every entry from
				your Account page. It's removed straight away. Copies may remain in the database
				provider's short-term backups for up to 7 days before they're gone for good.
			</li>
		</ul>
		<p>
			If you have a concern we haven't resolved, you can contact the
			<a href="https://www.privacy.org.nz" rel="noopener" target="_blank">Office of the Privacy Commissioner</a>.
		</p>
	</section>

	<section>
		<h2>Changes to this policy</h2>
		<p>
			If this policy changes, we'll update the date at the top. If a change affects how your
			journal is used, we'll email you before it takes effect.
		</p>
	</section>

	<aside class="privacy__support" aria-label="Support">
		<p>
			Hauora Journal is a self-reflection tool, not a health service. If you're struggling and
			need to talk to someone, free call or text <strong>1737</strong> any time to reach a
			trained counsellor. In an emergency, call <strong>111</strong>.
		</p>
	</aside>
</article>

<style lang="scss">
	.privacy {
		max-width: 680px;
		margin: 0 auto;
		padding: var(--space-lg) var(--space-md);
		line-height: 1.6;

		h1 {
			font-size: var(--font-size-xxl);
			margin: 0;
		}

		h2 {
			font-size: var(--font-size-lg);
			margin: var(--space-lg) 0 var(--space-xs);
		}

		p,
		ul {
			margin: 0 0 var(--space-sm);
		}

		ul {
			padding-left: var(--space-md);
		}

		li + li {
			margin-top: var(--space-xs);
		}

		a {
			color: var(--color-link);
		}
	}

	.privacy__back {
		font-size: var(--font-size-sm);
	}

	.privacy__updated {
		font-size: var(--font-size-sm);
		color: var(--color-text-muted);
	}

	.privacy__lead {
		font-size: var(--font-size-lg);
	}

	.privacy__support {
		margin-top: var(--space-xl);
		padding: var(--space-sm) var(--space-md);
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-left: 4px solid var(--color-success);
		border-radius: var(--radius-md);

		p {
			margin: 0;
		}
	}
</style>
