<template>
  <div class="box">
    <button class="delete is-pulled-right" v-on:click="remove"></button>
    <article class="media">
      <figure class="media-left">
        <p class="image is-96x96">
          <img :src="imageUrl">
        </p>
      </figure>
      <div class="media-content">
        <div class="content">
          <p><strong>{{ artistName }}</strong></p>
          <p v-if="description">{{ description }}<span v-if="url"></br>See more on <a :href="url" target="_blank">Wikipedia</a>.</span></p>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
module.exports = {
  props: ['description', 'url', 'artistName', 'imageUrl'],
  methods: {
    remove() {
      window.fetch(`/artists?name=${this.artistName}`, { method: 'delete' });
    },
  },
};
</script>
