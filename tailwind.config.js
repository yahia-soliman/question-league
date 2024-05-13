/** @type {import('tailwindcss').Config} */
export default {
  content: ["./app/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        pumpkin: "#FB720D",
        cinnabar: "#EF441C",
        cerulean: "#266D87",
        prussian: "#0E344B",
        gunmetal: "#03212C",
      },
    },
    plugins: [],
  },
};

/**
 * To generate the style.css file according to used classes
 * dev:
 * tailwindcss -i ./tailwind.input.css -o ./app/static/style.css --watch
 *
 * build:
 * tailwindcss -i ./tailwind.input.css -o ./app/static/style.css --minify
 */
