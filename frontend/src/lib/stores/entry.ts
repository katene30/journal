import { writable, derived } from 'svelte/store';
import type { EntryState, PillarState, MauriState, PillarId } from '$lib/types';

// Helper to create empty pillar state
const createEmptyPillarState = (): PillarState => ({
	mauri: 'untouched',
	scales: [],
	reflection: ''
});

// Initial entry state
const createEmptyEntry = (): EntryState => ({
	date: new Date(),
	overallScales: [],
	journalText: '',
	hinengaro: createEmptyPillarState(),
	tinana: createEmptyPillarState(),
	whanau: createEmptyPillarState(),
	wairua: createEmptyPillarState(),
	isDraft: true
});

// Main entry store
export const currentEntry = writable<EntryState>(createEmptyEntry());

// Active pillar store
export const activePillar = writable<PillarId>('reflection');

// Derived store for pillar mauri states (for nav display)
export const pillarMauriStates = derived(currentEntry, ($entry) => ({
	reflection: calculateMauri($entry.overallScales.length, $entry.journalText),
	hinengaro: $entry.hinengaro.mauri,
	tinana: $entry.tinana.mauri,
	whanau: $entry.whanau.mauri,
	wairua: $entry.wairua.mauri
}));

// Calculate mauri state based on engagement
function calculateMauri(scalesAnswered: number, reflectionText: string): MauriState {
	const hasReflection = reflectionText.trim().length > 0;
	const hasScales = scalesAnswered > 0;

	if (hasReflection && scalesAnswered >= 2) return 'deep';
	if (hasReflection || scalesAnswered >= 2) return 'meaningful';
	if (hasScales) return 'light';
	return 'untouched';
}

// Actions
export const entryActions = {
	reset: () => {
		currentEntry.set(createEmptyEntry());
		activePillar.set('reflection');
	},

	setDate: (date: Date) => {
		currentEntry.update((e) => ({ ...e, date }));
	},

	setJournalText: (text: string) => {
		currentEntry.update((e) => ({ ...e, journalText: text }));
	},

	updatePillar: (pillarId: PillarId, updates: Partial<PillarState>) => {
		if (pillarId === 'reflection') return; // Reflection is handled separately

		currentEntry.update((e) => ({
			...e,
			[pillarId]: { ...e[pillarId as keyof Pick<EntryState, 'hinengaro' | 'tinana' | 'whanau' | 'wairua'>], ...updates }
		}));
	},

	navigateToPillar: (pillarId: PillarId) => {
		activePillar.set(pillarId);
	},

	navigateNext: () => {
		const order: PillarId[] = ['reflection', 'hinengaro', 'tinana', 'whanau', 'wairua'];
		activePillar.update((current) => {
			const currentIndex = order.indexOf(current);
			const nextIndex = Math.min(currentIndex + 1, order.length - 1);
			return order[nextIndex];
		});
	},

	navigatePrev: () => {
		const order: PillarId[] = ['reflection', 'hinengaro', 'tinana', 'whanau', 'wairua'];
		activePillar.update((current) => {
			const currentIndex = order.indexOf(current);
			const prevIndex = Math.max(currentIndex - 1, 0);
			return order[prevIndex];
		});
	}
};

// LocalStorage draft persistence
const DRAFT_KEY = 'journal_draft';

export const saveDraft = () => {
	currentEntry.subscribe((entry) => {
		if (entry.isDraft) {
			localStorage.setItem(DRAFT_KEY, JSON.stringify(entry));
		}
	});
};

export const loadDraft = (): EntryState | null => {
	const saved = localStorage.getItem(DRAFT_KEY);
	if (saved) {
		try {
			const parsed = JSON.parse(saved);
			parsed.date = new Date(parsed.date);
			return parsed;
		} catch {
			return null;
		}
	}
	return null;
};

export const clearDraft = () => {
	localStorage.removeItem(DRAFT_KEY);
};
