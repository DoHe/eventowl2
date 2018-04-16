const Vue = require('vue');

const { nodeListToArray } = require('./helpers');
const Artists = require('./components/artists.vue');
const Events = require('./components/events.vue');

document.addEventListener('DOMContentLoaded', () => {
  nodeListToArray(document.querySelectorAll('.navbar-burger')).forEach((el) => {
    el.addEventListener('click', () => {
      const target = document.getElementById(el.dataset.target);
      el.classList.toggle('is-active');
      target.classList.toggle('is-active');
    });
  });

  new Vue({
    el: '#app',
    components: { Artists, Events },
  });
});
