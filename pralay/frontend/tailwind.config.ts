/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        risk: {
          low: '#10b981',      // Green
          moderate: '#f59e0b', // Yellow/Orange
          high: '#ef4444',     // Red
          extreme: '#7c2d12',  // Dark red/brown
        },
      },
    },
  },
  plugins: [],
}
