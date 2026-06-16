import type { PillarConfig } from '$lib/types';

export const PILLARS: PillarConfig[] = [
	{
		id: 'reflection',
		icon: '📝',
		name: 'Reflection',
		teReo: 'Whakaaro',
		color: '#607D8B',
		question: {
			maori: 'He pēhea tō rā i tēnei rā?',
			english: 'How was your day today?'
		},
		scales: [
			{
				id: 'overall_day_rating',
				leftLabel: 'Difficult day',
				rightLabel: 'Great day'
			}
		],
		textFields: [
			{ id: 'best_thing_today', label: 'Best thing today', placeholder: 'What went well?' },
			{ id: 'hardest_thing_today', label: 'Hardest thing today', placeholder: 'What was challenging?' },
			{ id: 'significant_events', label: 'Significant events', placeholder: 'Anything notable happen?' },
			{ id: 'log', label: 'Journal', placeholder: "What's on your mind?" }
		]
	},
	{
		id: 'hinengaro',
		icon: '🧠',
		name: 'Hinengaro',
		teReo: 'Mind',
		color: '#2196F3',
		question: {
			maori: 'E pēhea ana tō hinengaro i tēnei rā?',
			english: 'How is your mind today?'
		},
		scales: [
			{ id: 'mood', leftLabel: 'Low mood', rightLabel: 'Positive mood' },
			{ id: 'anxiety_level', leftLabel: 'Calm', rightLabel: 'Anxious' },
			{ id: 'stress_level', leftLabel: 'Relaxed', rightLabel: 'Stressed' }
		]
	},
	{
		id: 'tinana',
		icon: '💪',
		name: 'Tinana',
		teReo: 'Body',
		color: '#4CAF50',
		question: {
			maori: 'E pēhea ana tō tinana i tēnei rā?',
			english: 'How is your body today?'
		},
		scales: [
			{ id: 'sleep_quality', leftLabel: 'Poor sleep', rightLabel: 'Well rested' },
			{ id: 'energy_level', leftLabel: 'Exhausted', rightLabel: 'Energetic' },
			{ id: 'exercise_level', leftLabel: 'Sedentary', rightLabel: 'Active' },
			{ id: 'diet_quality', leftLabel: 'Poorly nourished', rightLabel: 'Well nourished' }
		],
		extraFields: [
			{ id: 'sleep_hours', type: 'number', label: 'Hours of sleep', placeholder: '8' },
			{ id: 'alcohol_caffeine_consumption', type: 'text', label: 'Alcohol/caffeine', placeholder: 'e.g., 2 coffees, 1 beer' }
		]
	},
	{
		id: 'whanau',
		icon: '💛',
		name: 'Whānau',
		teReo: 'Relationships',
		color: '#FF9800',
		question: {
			maori: 'E pēhea ana ō hononga i tēnei rā?',
			english: 'How are your connections today?'
		},
		scales: [
			{ id: 'social_connection', leftLabel: 'Isolated', rightLabel: 'Connected' },
			{ id: 'social_interactions_quality', leftLabel: 'Draining', rightLabel: 'Nourishing' }
		]
	},
	{
		id: 'wairua',
		icon: '🌿',
		name: 'Wairua',
		teReo: 'Spirit',
		color: '#9C27B0',
		question: {
			maori: 'E pēhea ana tō wairua i tēnei rā?',
			english: 'How is your spirit today?'
		},
		scales: [
			{ id: 'sense_of_meaning', leftLabel: 'Lacking purpose', rightLabel: 'Purposeful' }
		]
	},
	{
		id: 'mauriora',
		icon: '🪞',
		name: 'Mauriora',
		teReo: 'Identity',
		color: '#00BCD4',
		question: {
			maori: 'I rongo koe i a koe anō i tēnei rā?',
			english: 'Did you feel like yourself today?'
		},
		scales: [
			{ id: 'felt_like_myself', leftLabel: 'Not myself', rightLabel: 'Fully myself' }
		]
	},
	{
		id: 'waiora',
		icon: '🏡',
		name: 'Waiora',
		teReo: 'Environment',
		color: '#795548',
		question: {
			maori: 'E pēhea ana tō taiao i tēnei rā?',
			english: 'How is your environment today?'
		},
		scales: [
			{ id: 'environment_quality', leftLabel: 'Unsupportive', rightLabel: 'Supportive' }
		]
	}
];

export const getPillarById = (id: string): PillarConfig | undefined => {
	return PILLARS.find((p) => p.id === id);
};

export const getPillarColor = (id: string): string => {
	return getPillarById(id)?.color ?? '#607D8B';
};
