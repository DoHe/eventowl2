const Vue = require('vue');

const { prepareNavbar } = require('./helpers');
const Artists = require('./components/artists.vue');
const Events = require('./components/events.vue');

document.addEventListener('DOMContentLoaded', () => {
  prepareNavbar();
  new Vue({
    el: '#app',
    components: { Artists, Events },
  });
});
