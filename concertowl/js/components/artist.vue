<template>
  <div class="box">
    <div class="delete is-pulled-right" @click="remove"/>
    <article class="media">
      <figure class="media-left">
        <p class="image is-96x96">
          <img :src="imageUrl">
        </p>
      </figure>
      <div class="media-content">
        <div class="content">
          <p><strong><span class="is-capitalized">{{ artistName }}</span></strong></p>
          <p v-if="description">
            {{ description }}
            <span v-if="url">
              </br> See more on <a :href="url" target="_blank">Wikipedia</a>.
            </span>
          </p>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
const { callBackend } = require('../helpers');

module.exports = {
  props: ['description', 'url', 'artistName', 'imageUrl'],
  methods: {
    remove() {
      this.$parent.$emit('remove_artist', this.artistName);
      callBackend(`/artists/${this.artistName}/`, { method: 'delete' });
    },
  },
};
</script>
