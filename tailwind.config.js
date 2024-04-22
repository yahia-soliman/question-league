/** @type {import('tailwindcss').Config} */
export default {
  content: ["./app/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
};

/**
  * To generate the style.css file according to used classes
  * dev:
  * tailwindcss -i ./tailwind.input.css -o ./app/static/style.css --watch
  *
  * build:
  * tailwindcss -i ./tailwind.input.css -o ./app/static/style.css --minify
  */
