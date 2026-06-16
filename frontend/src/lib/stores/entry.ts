import { writable, derived, get } from 'svelte/store';
import type { EntryState, PillarState, MauriState, PillarId } from '$lib/types';
import { entriesApi, type Entry, type EntryUpdate } from '$lib/api';

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

// Map frontend state to Django API format
function toApiFormat(entry: EntryState): EntryUpdate {
	const scaleValue = (scales: { id: string; value: number | null }[], id: string) =>
		scales.find((s) => s.id === id)?.value ?? null;

	return {
		date: entry.date.toISOString().split('T')[0],
		// Reflection
		log: entry.journalText,
		overall_day_rating: scaleValue(entry.overallScales, 'overall'),
		// Hinengaro
		mood: scaleValue(entry.hinengaro.scales, 'mood'),
		anxiety_level: scaleValue(entry.hinengaro.scales, 'anxiety'),
		stress_level: scaleValue(entry.hinengaro.scales, 'stress'),
		// Tinana
		sleep_quality: scaleValue(entry.tinana.scales, 'sleep'),
		exercise_level: scaleValue(entry.tinana.scales, 'exercise'),
		energy_level: scaleValue(entry.tinana.scales, 'energy'),
		// Whanau
		social_connection: scaleValue(entry.whanau.scales, 'connection'),
		social_interactions_quality: scaleValue(entry.whanau.scales, 'support'),
		// Wairua
		sense_of_meaning: scaleValue(entry.wairua.scales, 'meaning')
	};
}

// Map Django API response to frontend state
function fromApiFormat(apiEntry: Entry): EntryState {
	const makeScale = (id: string, value: number | null) => ({
		id,
		leftLabel: '',
		rightLabel: '',
		value
	});

	return {
		id: apiEntry.id,
		date: new Date(apiEntry.date),
		overallScales: [makeScale('overall', apiEntry.overall_day_rating)],
		journalText: apiEntry.log || '',
		hinengaro: {
			mauri: 'untouched',
			scales: [
				makeScale('mood', apiEntry.mood),
				makeScale('anxiety', apiEntry.anxiety_level),
				makeScale('stress', apiEntry.stress_level)
			]
		},
		tinana: {
			mauri: 'untouched',
			scales: [
				makeScale('sleep', apiEntry.sleep_quality),
				makeScale('exercise', apiEntry.exercise_level),
				makeScale('energy', apiEntry.energy_level)
			]
		},
		whanau: {
			mauri: 'untouched',
			scales: [
				makeScale('connection', apiEntry.social_connection),
				makeScale('support', apiEntry.social_interactions_quality)
			]
		},
		wairua: {
			mauri: 'untouched',
			scales: [makeScale('meaning', apiEntry.sense_of_meaning)]
		},
		savedAt: new Date(apiEntry.updated_at),
		isDraft: false
	};
}

// API actions
export const entryApiActions = {
	loadToday: async () => {
		const apiEntry = await entriesApi.today();
		const entry = fromApiFormat(apiEntry);
		currentEntry.set(entry);
		return entry;
	},

	loadEntry: async (id: number) => {
		const apiEntry = await entriesApi.get(id);
		const entry = fromApiFormat(apiEntry);
		currentEntry.set(entry);
		return entry;
	},

	saveEntry: async () => {
		const entry = get(currentEntry);
		const data = toApiFormat(entry);

		let saved: Entry;
		if (entry.id) {
			saved = await entriesApi.update(entry.id, data);
		} else {
			saved = await entriesApi.create(data as Entry);
		}

		currentEntry.update((e) => ({
			...e,
			id: saved.id,
			savedAt: new Date(saved.updated_at),
			isDraft: false
		}));

		clearDraft();
		return saved;
	}
};
