// Semantic differential scale (bipolar)
export interface SemanticScale {
	id: string;
	title: string;
	leftLabel: string;
	rightLabel: string;
	helpText?: string;
	value: number | null;
}

// Pillar identifiers - matches Django model groupings
export type PillarId =
	| 'reflection'
	| 'hinengaro'
	| 'tinana'
	| 'whanau'
	| 'wairua'
	| 'mauriora'
	| 'waiora';

// Text field config for reflection pillar
export interface TextFieldConfig {
	id: string;
	label: string;
	placeholder: string;
}

// Extra field config (number inputs, text inputs)
export interface ExtraFieldConfig {
	id: string;
	type: 'number' | 'text';
	label: string;
	placeholder: string;
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
	textFields?: TextFieldConfig[];
	extraFields?: ExtraFieldConfig[];
}
