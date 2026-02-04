/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-green': '#0B3D2E',
        'medium-green': '#0B8043',
        'light-green': '#2E7D32',
      },
    },
  },
  plugins: [],
}
