import { writable, derived, get } from 'svelte/store';
import type { PillarId } from '$lib/types';
import { entriesApi, type Entry } from '$lib/api';

// Entry data matching Django model exactly
export interface EntryData {
	id?: number;
	date: string; // YYYY-MM-DD format
	// Hinengaro
	mood: number | null;
	anxiety_level: number | null;
	stress_level: number | null;
	// Tinana
	sleep_hours: number | null;
	sleep_quality: number | null;
	exercise_level: number | null;
	diet_quality: number | null;
	energy_level: number | null;
	alcohol_caffeine_consumption: string;
	// Whanau
	social_connection: number | null;
	social_interactions_quality: number | null;
	// Wairua
	sense_of_meaning: number | null;
	// Mauriora
	felt_like_myself: number | null;
	// Waiora
	environment_quality: number | null;
	// Reflection
	overall_day_rating: number | null;
	best_thing_today: string;
	hardest_thing_today: string;
	significant_events: string;
	log: string;
}

function todayString(): string {
	return new Date().toISOString().split('T')[0];
}

function createEmptyEntry(): EntryData {
	return {
		date: todayString(),
		mood: null,
		anxiety_level: null,
		stress_level: null,
		sleep_hours: null,
		sleep_quality: null,
		exercise_level: null,
		diet_quality: null,
		energy_level: null,
		alcohol_caffeine_consumption: '',
		social_connection: null,
		social_interactions_quality: null,
		sense_of_meaning: null,
		felt_like_myself: null,
		environment_quality: null,
		overall_day_rating: null,
		best_thing_today: '',
		hardest_thing_today: '',
		significant_events: '',
		log: ''
	};
}

// Main entry store
export const currentEntry = writable<EntryData>(createEmptyEntry());

// Active pillar store
export const activePillar = writable<PillarId>('reflection');

// Pillar order for navigation
const PILLAR_ORDER: PillarId[] = [
	'reflection',
	'hinengaro',
	'tinana',
	'whanau',
	'wairua',
	'mauriora',
	'waiora'
];

// Actions
export const entryActions = {
	reset: () => {
		currentEntry.set(createEmptyEntry());
		activePillar.set('reflection');
	},

	setDate: (date: string) => {
		currentEntry.update((e) => ({ ...e, date }));
	},

	setField: <K extends keyof EntryData>(field: K, value: EntryData[K]) => {
		currentEntry.update((e) => ({ ...e, [field]: value }));
	},

	navigateToPillar: (pillarId: PillarId) => {
		activePillar.set(pillarId);
	},

	navigateNext: () => {
		activePillar.update((current) => {
			const idx = PILLAR_ORDER.indexOf(current);
			return PILLAR_ORDER[Math.min(idx + 1, PILLAR_ORDER.length - 1)];
		});
	},

	navigatePrev: () => {
		activePillar.update((current) => {
			const idx = PILLAR_ORDER.indexOf(current);
			return PILLAR_ORDER[Math.max(idx - 1, 0)];
		});
	}
};

// Helper to map API response to store
function mapApiToStore(apiEntry: Entry): EntryData {
	return {
		id: apiEntry.id,
		date: apiEntry.date,
		mood: apiEntry.mood,
		anxiety_level: apiEntry.anxiety_level,
		stress_level: apiEntry.stress_level,
		sleep_hours: apiEntry.sleep_hours,
		sleep_quality: apiEntry.sleep_quality,
		exercise_level: apiEntry.exercise_level,
		diet_quality: apiEntry.diet_quality,
		energy_level: apiEntry.energy_level,
		alcohol_caffeine_consumption: apiEntry.alcohol_caffeine_consumption || '',
		social_connection: apiEntry.social_connection,
		social_interactions_quality: apiEntry.social_interactions_quality,
		sense_of_meaning: apiEntry.sense_of_meaning,
		felt_like_myself: apiEntry.felt_like_myself,
		environment_quality: apiEntry.environment_quality,
		overall_day_rating: apiEntry.overall_day_rating,
		best_thing_today: apiEntry.best_thing_today || '',
		hardest_thing_today: apiEntry.hardest_thing_today || '',
		significant_events: apiEntry.significant_events || '',
		log: apiEntry.log || ''
	};
}

// API actions
export const entryApiActions = {
	loadToday: async () => {
		const apiEntry = await entriesApi.today();
		currentEntry.set(mapApiToStore(apiEntry));
		return apiEntry;
	},

	loadByDate: async (date: string) => {
		const apiEntry = await entriesApi.byDate(date);
		currentEntry.set(mapApiToStore(apiEntry));
		return apiEntry;
	},

	loadEntry: async (id: number) => {
		const apiEntry = await entriesApi.get(id);
		currentEntry.set(mapApiToStore(apiEntry));
		return apiEntry;
	},

	saveEntry: async () => {
		const entry = get(currentEntry);
		const { id, ...data } = entry;

		let saved: Entry;
		if (id) {
			saved = await entriesApi.update(id, data);
		} else {
			saved = await entriesApi.create(data as Entry);
		}

		currentEntry.update((e) => ({ ...e, id: saved.id }));
		return saved;
	}
};

// LocalStorage draft persistence
const DRAFT_KEY = 'journal_draft';

export const saveDraft = () => {
	const entry = get(currentEntry);
	localStorage.setItem(DRAFT_KEY, JSON.stringify(entry));
};

export const loadDraft = (): EntryData | null => {
	const saved = localStorage.getItem(DRAFT_KEY);
	if (saved) {
		try {
			return JSON.parse(saved);
		} catch {
			return null;
		}
	}
	return null;
};

export const clearDraft = () => {
	localStorage.removeItem(DRAFT_KEY);
};
