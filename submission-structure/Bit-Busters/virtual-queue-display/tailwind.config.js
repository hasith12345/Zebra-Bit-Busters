/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'queue-primary': '#2563eb',
        'queue-secondary': '#f59e0b',
        'queue-success': '#10b981',
        'queue-danger': '#ef4444',
        'queue-warning': '#f59e0b',
      },
      animation: {
        'pulse-glow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-gentle': 'bounce 1s infinite',
      }
    },
  },
  plugins: [],
}