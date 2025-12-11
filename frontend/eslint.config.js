import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'

export default [
  // add more generic rulesets here, such as:
  // js.configs.recommended,
  ...pluginVue.configs['flat/vue2-recommended'],
  // ...pluginVue.configs['flat/vue2-recommended'], // Use this if you are using Vue.js 2.x.
  {
    rules: {
      // override/add rules settings here, such as:
      // 'vue/no-unused-vars': 'error'
      "vue/max-attributes-per-line": ["error", {
        "singleline": {
            "max": 4
            },      
            "multiline": {
            "max": 4
            }
        }],
      "vue/html-closing-bracket-newline": "off"
    },
    languageOptions: {
      parserOptions: {
        parser: '@typescript-eslint/parser',
        extraFileExtensions: ['.vue'],
        ecmaVersion: 2024,
      },
      sourceType: 'module',
      globals: {
        ...globals.browser
      }
    }
  }
]