const Vue = require('vue');

const { clickableNavbarMenu } = require('./helpers');
const Artists = require('./components/artists.vue');
const Events = require('./components/events.vue');
const Preferences = require('./components/preferences.vue');
const Notifications = require('./components/notifications.vue');

document.addEventListener('DOMContentLoaded', () => {
  clickableNavbarMenu();
  new Vue({
    el: '#app',
    components: { Artists, Events, Preferences },
  });

  new Vue({
    el: '#notifications',
    components: { Notifications },
  });
});
