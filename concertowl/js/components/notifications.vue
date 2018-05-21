<template>
  <div :class="{ 'is-active': active }" class="navbar-item has-dropdown" @click="activeClicked">
    <a class="navbar-link">
      <div class="tags has-addons">
        <span class="tag is-rounded is-white">
          {{ notificationsData.length }}
        </span>
        <span class="tag is-rounded is-white">
          <span class="icon">
            <i class="fas icon-bell-alt"/>
          </span>
        </span>
      </div>
    </a>
    <div class="navbar-dropdown">
      <a
        v-for="notification in notificationsData"
        :key="(notification.title || notification.artists) + notification.start_time"
        :href="`/events/${notification.event_id}`"
        class="dropdown-item">
        <p class="has-text-weight-bold">{{ notification.title }}</p>
        <p>{{ localizedTime(notification.start_time) }}</p>
      </a>
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
    activeClicked() {
      this.active = !this.active;
      if (this.active) {
        callBackend('/notifications/read/', {
          method: 'POST',
          body: new URLSearchParams(`ts=${Date.now()}`),
        });
      } else {
        this.poll();
      }
    },
  },
  mounted() {
    window.setInterval(this.poll, 5000);
  },
};
</script>
