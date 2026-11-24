import { writable } from 'svelte/store';
import { browser } from '$app/environment';

/**
 * What entry tiles show. Saved on this device only: someone might want
 * previews on their own laptop but not on a phone they hand around.
 *
 * Defaults: journal previews off (reflections are opened on purpose),
 * hauora indicators on.
 */
export interface PrivacyPrefs {
	showPreviews: boolean;
	showIndicators: boolean;
}

const KEY = 'hauora.privacy';
const DEFAULTS: PrivacyPrefs = { showPreviews: false, showIndicators: true };

function load(): PrivacyPrefs {
	if (!browser) return DEFAULTS;
	try {
		const saved = JSON.parse(localStorage.getItem(KEY) ?? '{}');
		return {
			showPreviews: typeof saved.showPreviews === 'boolean' ? saved.showPreviews : DEFAULTS.showPreviews,
			showIndicators: typeof saved.showIndicators === 'boolean' ? saved.showIndicators : DEFAULTS.showIndicators
		};
	} catch {
		return DEFAULTS;
	}
}

export const privacyPrefs = writable<PrivacyPrefs>(load());

privacyPrefs.subscribe((prefs) => {
	if (!browser) return;
	try {
		localStorage.setItem(KEY, JSON.stringify(prefs));
	} catch {
		// Private browsing or storage blocked: the setting lasts for this visit only
	}
});
