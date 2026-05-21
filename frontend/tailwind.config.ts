import type { Config } from 'tailwindcss'
const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: { DEFAULT: '#14213D', light: '#1e3163', dark: '#0d1829' },
        burgundy: { DEFAULT: '#7A1E2C', light: '#9b2535', dark: '#5c1620' },
        gold: { DEFAULT: '#C9A227', light: '#ddb93a', dark: '#a8881f' },
        ivory: { DEFAULT: '#F7F1E5', dark: '#EDE3CC' },
        parchment: { DEFAULT: '#EFE3C8', dark: '#E0CFA8' },
        forest: { DEFAULT: '#1F5C4D', light: '#27745f', dark: '#164438' },
        terracotta: { DEFAULT: '#B86B4B', light: '#cc7d5a', dark: '#9a5438' },
        sand: '#FAF6EE',
        risk: { critical: '#B42318', high: '#B86B4B', medium: '#D97706', low: '#16834A' }
      },
      fontFamily: {
        serif: ['"Cormorant Garamond"', '"Playfair Display"', 'Georgia', 'serif'],
        sans: ['Manrope', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}
export default config
