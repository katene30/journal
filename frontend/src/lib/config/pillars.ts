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
			{ id: 'overall-calm', leftLabel: 'Calm', rightLabel: 'Overwhelmed' },
			{ id: 'overall-energy', leftLabel: 'Low energy', rightLabel: 'Energised' },
			{ id: 'overall-grounded', leftLabel: 'Disconnected', rightLabel: 'Grounded' }
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
			{ id: 'anxiety', leftLabel: 'Calm', rightLabel: 'Anxious' },
			{ id: 'stress', leftLabel: 'Relaxed', rightLabel: 'Stressed' },
			{ id: 'focus', leftLabel: 'Focused', rightLabel: 'Distracted' }
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
			{ id: 'energy', leftLabel: 'Exhausted', rightLabel: 'Energetic' },
			{ id: 'sleep', leftLabel: 'Poor sleep', rightLabel: 'Well rested' },
			{ id: 'movement', leftLabel: 'Sedentary', rightLabel: 'Active' },
			{ id: 'nourishment', leftLabel: 'Poorly nourished', rightLabel: 'Well nourished' }
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
			{ id: 'connection', leftLabel: 'Isolated', rightLabel: 'Connected' },
			{ id: 'interactions', leftLabel: 'Draining interactions', rightLabel: 'Nourishing interactions' },
			{ id: 'belonging', leftLabel: 'Disconnected', rightLabel: 'Belonging' }
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
			{ id: 'meaning', leftLabel: 'Lacking purpose', rightLabel: 'Purposeful' },
			{ id: 'grounded', leftLabel: 'Ungrounded', rightLabel: 'Grounded' },
			{ id: 'peace', leftLabel: 'Unsettled', rightLabel: 'At peace' }
		]
	}
];

export const getPillarById = (id: string): PillarConfig | undefined => {
	return PILLARS.find((p) => p.id === id);
};

export const getPillarColor = (id: string): string => {
	return getPillarById(id)?.color ?? '#607D8B';
};
