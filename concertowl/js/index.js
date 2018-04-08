const Vue = require('vue');

const Artist = require('./components/artist.vue');
const Event = require('./components/event.vue');

document.addEventListener('DOMContentLoaded', () => {
  const navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
  navbarBurgers.forEach((el) => {
    el.addEventListener('click', () => {
      const target = document.getElementById(el.dataset.target);
      el.classList.toggle('is-active');
      target.classList.toggle('is-active');
    });
  });

  const app = new Vue({
    el: '#app',
    components: { Artist, Event },
  });
});
