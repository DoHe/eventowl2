<template>
  <div :class="{ 'is-active': active }" class="dropdown is-right" @click="active = !active">
    <div class="tags has-addons">
      <span class="js-notification-count dropdown-trigger tag is-rounded is-white">
        {{ notificationsData.length }}
      </span>
      <span class="tag is-rounded is-white">
        <span class="icon is-small">
          <i class="fas icon-bell-alt"/>
        </span>
      </span>
    </div>
    <div class="dropdown-menu" role="menu">
      <div class="js-notification-dropdown dropdown-content">
        <div
          v-for="notification in notificationsData"
          :key="(notification.title || notification.artists) + notification.start_time"
          class="dropdown-item">
          <p class="has-text-weight-bold">{{ notification.title }}</p>
          <p>{{ localizedTime(notification.start_time) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const { callBackend } = require('../helpers');

module.exports = {
  props: ['notifications'],
  data() {
    return {
      notificationsData: this.notifications,
      active: false,
    };
  },
  methods: {
    localizedTime(timeString) {
      const d = new Date(timeString);
      if (d.getUTCHours() || d.getUTCMinutes()) {
        return d.toLocaleString([], { timeZone: 'UTC' });
      }
      return d.toLocaleDateString([], { timeZone: 'UTC' });
    },
    poll() {
      callBackend('/notifications/')
        .then(data => data.json())
        .then((json) => { this.notificationsData = json.notifications; });
    },
  },
  mounted() {
    window.setInterval(this.poll, 20000);
  },
};
</script>
