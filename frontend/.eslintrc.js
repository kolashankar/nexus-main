module.exports = {
  extends: ['react-app', 'react-app/jest'],
  rules: {
    'react/prop-types': 'off', // Disable prop-types validation (we can use TypeScript for this)
    'no-undef': 'error',
    'react/react-in-jsx-scope': 'off', // Not needed with React 17+
  },
  env: {
    browser: true,
    es2021: true,
    jest: true,
    node: true,
  },
  globals: {
    process: 'readonly',
    module: 'readonly',
    require: 'readonly',
    __dirname: 'readonly',
  },
  overrides: [
    {
      files: ['**/*.test.js', '**/*.test.jsx', '**/*.spec.js', '**/*.spec.jsx'],
      env: {
        jest: true,
      },
      globals: {
        describe: 'readonly',
        it: 'readonly',
        test: 'readonly',
        expect: 'readonly',
        beforeEach: 'readonly',
        afterEach: 'readonly',
        beforeAll: 'readonly',
        afterAll: 'readonly',
        jest: 'readonly',
      },
    },
    {
      files: [
        'tailwind.config.js',
        'vite.config.js',
        'jest.config.js',
        'playwright.config.js',
        'craco.config.js',
        'postcss.config.js',
      ],
      env: {
        node: true,
      },
    },
  ],
};
