// Mauri (presence) states for each pillar
export type MauriState = 'untouched' | 'light' | 'meaningful' | 'deep';

// Semantic differential scale (bipolar)
export interface SemanticScale {
	id: string;
	leftLabel: string; // e.g., "Calm"
	rightLabel: string; // e.g., "Overwhelmed"
	value: number | null; // 1-7, null if not set
}

// State for each pillar
export interface PillarState {
	mauri: MauriState;
	scales: SemanticScale[];
	reflection?: string;
}

// Pillar identifiers
export type PillarId = 'reflection' | 'hinengaro' | 'tinana' | 'whanau' | 'wairua';

// Full entry state
export interface EntryState {
	id?: number;
	date: Date;

	// Core reflection (always available)
	overallScales: SemanticScale[];
	journalText: string;

	// Pillar states
	hinengaro: PillarState;
	tinana: PillarState;
	whanau: PillarState;
	wairua: PillarState;

	// Metadata
	savedAt?: Date;
	isDraft: boolean;
}

// Derived pillar scores (calculated, not input)
export interface DerivedScores {
	hinengaro: number | null;
	tinana: number | null;
	whanau: number | null;
	wairua: number | null;
}

// Pillar configuration (for rendering)
export interface PillarConfig {
	id: PillarId;
	icon: string;
	name: string;
	teReo: string;
	color: string;
	question: {
		maori: string;
		english: string;
	};
	scales: Omit<SemanticScale, 'value'>[];
}

// API response types
export interface EntryResponse {
	id: number;
	date: string;
	mood: number | null;
	anxiety_level: number | null;
	stress_level: number | null;
	sleep_quality: number | null;
	exercise_level: number | null;
	diet_quality: number | null;
	energy_level: number | null;
	social_connection: number | null;
	social_interactions_quality: number | null;
	sense_of_meaning: number | null;
	felt_like_myself: number | null;
	environment_quality: number | null;
	overall_day_rating: number | null;
	best_thing_today: string;
	hardest_thing_today: string;
	significant_events: string;
	log: string;
	// Derived scores
	hinengaro_score: number | null;
	tinana_score: number | null;
	whanau_score: number | null;
	wairua_score: number | null;
}
