const Vue = require('vue');

const { clickableNavbarMenu } = require('./helpers');
const Artists = require('./components/artists.vue');
const Events = require('./components/events.vue');
const Notifications = require('./components/notifications.vue');

document.addEventListener('DOMContentLoaded', () => {
  new Vue({
    el: '#app',
    components: { Artists, Events },
  });

  new Vue({
    el: '#notifications',
    components: { Notifications },
  });

  clickableNavbarMenu();
});
