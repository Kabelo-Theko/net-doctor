/**
 * net-doctor v2 "Calm Field Guide" — Tailwind consumption of tokens.css
 * Tokens are CSS custom properties (theme via html[data-theme]).
 */
module.exports = {
  content: ["./docs/**/*.html", "./src/**/*.{js,jsx,ts,tsx,vue}"],
  darkMode: ["selector", '[data-theme="field"]'],
  theme: {
    fontFamily: {
      display: ["Clash Display", "General Sans", "sans-serif"],
      sans: ["General Sans", "system-ui", "sans-serif"],
      mono: ["Red Hat Mono", "ui-monospace", "monospace"],
    },
    extend: {
      colors: {
        field: {
          DEFAULT: "var(--canvas-base)",
          surface: "var(--canvas-surface)",
          raised: "var(--canvas-raised)",
          inset: "var(--canvas-inset)",
          overlay: "var(--canvas-overlay)",
        },
        bone: {
          max: "var(--text-max)",
          DEFAULT: "var(--text-primary)",
          secondary: "var(--text-secondary)",
          tertiary: "var(--text-tertiary)",
          disabled: "var(--text-disabled)",
        },
        pulse: {
          DEFAULT: "var(--accent)",
          hover: "var(--accent-hover)",
          pressed: "var(--accent-pressed)",
          text: "var(--accent-text)",
          subtle: "var(--accent-subtle)",
          border: "var(--accent-border)",
          on: "var(--on-accent)",
          cmd: "var(--cmd-ink)",
        },
        pass: { DEFAULT: "var(--pass)", ink: "var(--pass-ink)", text: "var(--pass-text)", subtle: "var(--pass-subtle)" },
        fail: { DEFAULT: "var(--fail)", ink: "var(--fail-ink)", text: "var(--fail-text)", subtle: "var(--fail-subtle)" },
        amber: { DEFAULT: "var(--amber)", text: "var(--amber-text)", subtle: "var(--amber-subtle)" },
      },
      borderColor: { DEFAULT: "var(--border-default)", strong: "var(--border-strong)", pulse: "var(--accent-border)" },
      borderRadius: { item: "var(--radius-sm)", chip: "var(--radius-md)", card: "var(--radius-lg)", readout: "var(--radius-xl)", pill: "999px" },
      boxShadow: { 1: "var(--shadow-1)", 2: "var(--shadow-2)", ring: "var(--ring-accent)", focus: "var(--focus-ring)" },
      spacing: { rail: "216px" },
      maxWidth: { content: "880px" },
      fontSize: {
        hero: ["var(--text-hero)", { lineHeight: "1.04", letterSpacing: "-0.02em" }],
        h2: ["var(--text-h2)", { lineHeight: "1.15", letterSpacing: "-0.015em" }],
      },
      transitionTimingFunction: {
        standard: "cubic-bezier(.2, 0, 0, 1)",
        spring: "cubic-bezier(.34, 1.26, .5, 1)",
        emphasized: "cubic-bezier(.05, .7, .1, 1)",
      },
      transitionDuration: { micro: "130ms", small: "210ms", large: "300ms", page: "400ms" },
    },
  },
  plugins: [],
};
