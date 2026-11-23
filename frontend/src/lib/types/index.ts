// Semantic differential scale (bipolar)
export interface SemanticScale {
	id: string;
	title: string;
	leftLabel: string;
	rightLabel: string;
	helpText?: string;
	/** Higher means less well (e.g. anxiety), so pillar scores count it as 6 - value */
	reversed?: boolean;
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
	/** Short English description, e.g. "Mind & emotions" */
	theme: string;
	color: string;
	/** Darker variant for chart lines when `color` is under 3:1 contrast on the surface */
	chartColor?: string;
	question: {
		maori: string;
		english: string;
	};
	scales: Omit<SemanticScale, 'value'>[];
	textFields?: TextFieldConfig[];
	extraFields?: ExtraFieldConfig[];
}
