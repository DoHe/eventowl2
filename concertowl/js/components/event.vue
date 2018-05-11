<template>
  <div class="box">
    <article class="media">
      <figure class="media-left">
        <p class="image is-96x96 is-square">
          <img :src="pictureUrl">
        </p>
      </figure>
      <div class="media-content">
        <div class="content" @click="openTicketUrl">
          <p><strong><span class="is-capitalized">{{ title }}</span></strong></p>
          <div class="is-hidden-mobile">
            <p>
              <span class="is-capitalized">{{ artists.join(', ') }}</span>
              will be playing at
              <span :title="`${address} (${city}, ${country})`" class="hover-text">
                {{ venue }}
              </span>.
              <span v-if="startTime">
                It starts at {{ startTime }} on {{ startDate }}.
              </span>
              <span v-else>
                It happens on {{ startDate }}.
              </span>
              <span v-if="endDatetime">
                <span v-if="endTime">
                  And ends at {{ endTime }} on {{ endDate }}.
                </span>
                <span v-else>
                  And ends on {{ endDate }}.
                </span>
              </span>
            </p>
            <p>
              Buy your tickets <a :href="ticketUrl" target="_blank">here</a>.
            </p>
          </div>
          <div class="is-hidden-tablet">
            {{ startDate }} at {{ venue }}
          </div>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
module.exports = {
  props: ['defaultTitle', 'venue', 'address', 'city', 'country',
    'startDatetime', 'endDatetime', 'ticketUrl', 'pictureUrl', 'artists'],
  computed: {
    title() {
      return this.defaultTitle || this.artists.join(', ');
    },
    startTime() {
      return this.localizedTime(this.startDatetime);
    },
    startDate() {
      return this.localizedDate(this.startDatetime);
    },
    endTime() {
      return this.localizedTime(this.endDatetime);
    },
    endDate() {
      return this.localizedDate(this.endDatetime);
    },
  },
  methods: {
    localizedTime(datetime) {
      if (!datetime) {
        return undefined;
      }
      const d = new Date(datetime);
      return d.getUTCHours() || d.getUTCMinutes()
        ? d.toLocaleTimeString([], { timeZone: 'UTC', hour: '2-digit', minute: '2-digit' })
        : undefined;
    },
    localizedDate(datetime) {
      if (!datetime) {
        return undefined;
      }
      return new Date(datetime).toLocaleDateString([], { timeZone: 'UTC' });
    },
    openTicketUrl() {
      window.open(this.ticketUrl, '_blank');
    },
  },
};
</script>

<style scoped>
  .hover-text {
    text-decoration-line: underline;
    text-decoration-style: dotted;
  }
</style>
