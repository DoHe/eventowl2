module.exports = {
    "extends": [
    	"airbnb-base",
    	"plugin:vue/recommended"
    ],
    "env": {
        "browser": true,
        "node": true,
        "es6": true
    },
    "rules": {
        'no-new': 0,
        "vue/max-attributes-per-line": [2, {
            "singleline": 3,
            "multiline": {
                "max": 1,
                "allowFirstLine": false
            }
        }]
    }
};
