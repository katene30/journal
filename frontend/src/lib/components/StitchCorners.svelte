<!--
	Decorative stitched corners behind the entry form.
	Artwork: upper-left-stitch.svg and lower-right-stitch.svg, inlined so the
	stroke can follow the active pillar's colour (currentColor).
-->
<script lang="ts">
	let { color = 'var(--color-text)' }: { color?: string } = $props();
</script>

<div class="stitches" style="color: {color}" aria-hidden="true">
	<svg class="stitches__tl" viewBox="0 0 288 507" fill="none" xmlns="http://www.w3.org/2000/svg">
		<line x1="7.07107" y1="448" x2="59" y2="499.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="59" y1="448.071" x2="7.07107" y2="500" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="7.07107" y1="376" x2="59" y2="427.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="59" y1="376.071" x2="7.07107" y2="428" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="86.0711" y1="376" x2="138" y2="427.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="138" y1="376.071" x2="86.0711" y2="428" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="79.0711" y1="304" x2="131" y2="355.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="131" y1="304.071" x2="79.0711" y2="356" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="80.0711" y1="217" x2="132" y2="268.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="132" y1="217.071" x2="80.0711" y2="269" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="156.071" y1="80" x2="208" y2="131.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="208" y1="80.0711" x2="156.071" y2="132" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="231.071" y1="73" x2="283" y2="124.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="283" y1="73.0711" x2="231.071" y2="125" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="231.071" y1="7" x2="283" y2="58.9289" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="283" y1="7.07107" x2="231.071" y2="59" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="157.071" y1="220" x2="209" y2="271.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="209" y1="220.071" x2="157.071" y2="272" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="157.071" y1="151" x2="209" y2="202.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="209" y1="151.071" x2="157.071" y2="203" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
	</svg>
	<svg class="stitches__br" viewBox="0 0 376 358" fill="none" xmlns="http://www.w3.org/2000/svg">
		<line x1="234.071" y1="299" x2="286" y2="350.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="286" y1="299.071" x2="234.071" y2="351" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="90.0711" y1="299" x2="142" y2="350.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="142" y1="299.071" x2="90.0711" y2="351" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="246.071" y1="81" x2="298" y2="132.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="298" y1="81.0711" x2="246.071" y2="133" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="314.071" y1="77" x2="366" y2="128.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="366" y1="77.0711" x2="314.071" y2="129" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="319.071" y1="7" x2="371" y2="58.9289" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="371" y1="7.07107" x2="319.071" y2="59" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="90.0711" y1="221" x2="142" y2="272.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="142" y1="221.071" x2="90.0711" y2="273" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="7.07107" y1="299" x2="59" y2="350.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="59" y1="299.071" x2="7.07107" y2="351" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="162.071" y1="152" x2="214" y2="203.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="214" y1="152.071" x2="162.071" y2="204" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="174.071" y1="77" x2="226" y2="128.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="226" y1="77.0711" x2="174.071" y2="129" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="314.071" y1="299" x2="366" y2="350.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="366" y1="299.071" x2="314.071" y2="351" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="315.071" y1="221" x2="367" y2="272.929" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
		<line x1="367" y1="221.071" x2="315.071" y2="273" stroke-width="10" stroke-linecap="round" stroke="currentColor"/>
	</svg>
</div>

<style>
	.stitches {
		/* Phones have no free margins, so the stitches would sit behind the
		   heading, tabs and buttons. Only show them from tablet width up. */
		display: none;
		position: absolute;
		inset: 0;
		z-index: 0;
		overflow: hidden;
		pointer-events: none;
		opacity: 0.14;
		transition: color 400ms ease;
	}

	svg {
		position: absolute;
		display: block;
		height: auto;
	}

	/* Natural sizes 288x507 and 376x358; scaled so both read as one set */
	.stitches__tl {
		top: var(--space-sm);
		left: var(--space-sm);
		width: clamp(110px, 18vw, 260px);
	}

	.stitches__br {
		right: var(--space-sm);
		bottom: var(--space-sm);
		width: clamp(143px, 23.5vw, 340px);
	}

	@media (min-width: 768px) {
		.stitches {
			display: block;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.stitches {
			transition: none;
		}
	}
</style>
