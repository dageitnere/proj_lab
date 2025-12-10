// tailwind.config.js
import hamburgers from "tailwind-hamburgers";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
          brandGreen: "#2F6235",
      },
      fontFamily: {
        libre: ['"Libre Baskerville"', "serif"],
      },
    },
  },
  plugins: [hamburgers],
};
