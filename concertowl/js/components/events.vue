<template>
  <div class="container">
    <event
      v-for="event in events"
      :key="(event.title || event.artists) + event.start_time"
      :default-title="event.title"
      :venue="event.venue"
      :address="event.address"
      :city="event.city"
      :country="event.country"
      :start-datetime="event.start_time"
      :end-datetime="event.end_time"
      :ticket-url="event.ticket_url"
      :picture-url="event.picture_url"
      :artists="event.artists"
      class="box"
    />
  </div>
</template>

<script>
const Event = require('./event.vue');

module.exports = {
  props: ['events'],
  components: { Event },
};
</script>
