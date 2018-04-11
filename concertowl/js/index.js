const Vue = require('vue');

const { nodeListToArray } = require('./helpers');
const Artists = require('./components/artists.vue');
const Event = require('./components/event.vue');

document.addEventListener('DOMContentLoaded', () => {
  nodeListToArray(document.querySelectorAll('.navbar-burger')).forEach((el) => {
    el.addEventListener('click', () => {
      const target = document.getElementById(el.dataset.target);
      el.classList.toggle('is-active');
      target.classList.toggle('is-active');
    });
  });

  const app = new Vue({
    el: '#app',
    components: { Artists, Event },
  });
});
