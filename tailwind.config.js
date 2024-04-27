/** @type {import('tailwindcss').Config} */
export default {
  content: ["./app/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'amber': {
          DEFAULT: '#FFC344',
          100: '#402c00',
          200: '#815800',
          300: '#c18400',
          400: '#ffaf02',
          500: '#ffc344',
          600: '#ffcf68',
          700: '#ffdb8e',
          800: '#ffe7b4',
          900: '#fff3d9'
        },
        'sunglow': {
          DEFAULT: '#FFD15B',
          100: '#453200',
          200: '#8b6300',
          300: '#d09500',
          400: '#ffbd16',
          500: '#ffd15b',
          600: '#ffda7c',
          700: '#ffe39d',
          800: '#ffedbe',
          900: '#fff6de'
        },
        'denim': {
          DEFAULT: '#0067C5',
          100: '#001528',
          200: '#002950',
          300: '#003e77',
          400: '#00529f',
          500: '#0067c5',
          600: '#0687ff',
          700: '#44a5ff',
          800: '#83c3ff',
          900: '#c1e1ff'
        },
        'azul': {
          DEFAULT: '#0573CE',
          100: '#011729',
          200: '#022e52',
          300: '#03457a',
          400: '#045ca3',
          500: '#0573ce',
          600: '#1492f9',
          700: '#4fadfa',
          800: '#8ac9fc',
          900: '#c4e4fd'
        },
        'mint': {
          DEFAULT: '#3EC3A4',
          100: '#0c2721',
          200: '#184e41',
          300: '#247562',
          400: '#309c83',
          500: '#3ec3a4',
          600: '#63cfb6',
          700: '#8adbc8',
          800: '#b1e7da',
          900: '#d8f3ed'
        },
        'emerald': {
          DEFAULT: '#6FD7A3',
          100: '#0e3321',
          200: '#1c6641',
          300: '#2a9a62',
          400: '#3cc983',
          500: '#6fd7a3',
          600: '#8cdfb6',
          700: '#a9e7c8',
          800: '#c5efda',
          900: '#e2f7ed'
        },
      },
    },
    plugins: [],
  }
};

/**
  * To generate the style.css file according to used classes
  * dev:
  * tailwindcss -i ./tailwind.input.css -o ./app/static/style.css --watch
  *
  * build:
  * tailwindcss -i ./tailwind.input.css -o ./app/static/style.css --minify
  */
