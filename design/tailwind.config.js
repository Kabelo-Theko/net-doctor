/**
 * net-doctor "Bench Oscilloscope" — Tailwind consumption of tokens.css
 * Tokens are CSS custom properties (theme via html[data-theme]);
 * utilities reference the variables so classes switch themes for free.
 */
module.exports = {
  content: ["./docs/**/*.html", "./src/**/*.{js,jsx,ts,tsx,vue}"],
  darkMode: ["selector", '[data-theme="screen"]'],
  theme: {
    fontFamily: {
      scope: ["Azeret Mono", "ui-monospace", "monospace"],
      sans: ["Schibsted Grotesk", "system-ui", "sans-serif"],
    },
    extend: {
      colors: {
        bench: {
          DEFAULT: "var(--canvas-base)",
          screen: "var(--canvas-screen)",
          panel: "var(--canvas-panel)",
          inset: "var(--canvas-inset)",
          overlay: "var(--canvas-overlay)",
        },
        ink: {
          max: "var(--text-max)",
          DEFAULT: "var(--text-primary)",
          secondary: "var(--text-secondary)",
          tertiary: "var(--text-tertiary)",
          disabled: "var(--text-disabled)",
        },
        phos: {
          DEFAULT: "var(--phos)",
          dim: "var(--phos-dim)",
          ink: "var(--phos-ink)",
          subtle: "var(--phos-subtle)",
          border: "var(--phos-border)",
        },
        fail: { DEFAULT: "var(--fail)", ink: "var(--fail-ink)", subtle: "var(--fail-subtle)", border: "var(--fail-border)" },
        cursor: { DEFAULT: "var(--cursor)", subtle: "var(--cursor-subtle)" },
        graticule: { DEFAULT: "var(--graticule)", strong: "var(--graticule-strong)" },
      },
      borderColor: { DEFAULT: "var(--border-default)", strong: "var(--border-strong)" },
      borderRadius: { etch: "var(--radius-xs)", bezel: "var(--radius-sm)", screen: "var(--radius-md)" },
      boxShadow: {
        1: "var(--shadow-1)", 2: "var(--shadow-2)",
        edge: "var(--inner-edge)", glow: "var(--phos-glow)", focus: "var(--focus-ring)",
      },
      maxWidth: { bench: "940px" },
      backgroundImage: {
        graticule: "linear-gradient(var(--graticule) 1px, transparent 1px), linear-gradient(90deg, var(--graticule) 1px, transparent 1px)",
      },
      backgroundSize: { graticule: "28px 28px" },
      transitionTimingFunction: {
        standard: "cubic-bezier(.2, 0, 0, 1)",
        trace: "cubic-bezier(.3, .7, .1, 1)",
      },
      transitionDuration: { micro: "110ms", small: "190ms", large: "280ms", page: "380ms" },
    },
  },
  plugins: [],
};
