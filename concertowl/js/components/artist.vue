<template>
  <div>
    <div class="box" @click="showDescription = !showDescription">
      <div class="delete is-pulled-right" @click="remove" />
      <article class="media">
        <figure class="media-left">
          <p class="image is-96x96 is-square">
            <img :src="imageUrl">
          </p>
        </figure>
        <div class="media-content">
          <div class="content">
            <p><strong><span class="is-capitalized">{{ artistName }}</span></strong></p>
            <p v-if="description" class="is-hidden-mobile">
              {{ description }}
              <span v-if="url">
                <br> See more on <a :href="url" target="_blank">Wikipedia</a>.
              </span>
            </p>
            <p v-else class="is-hidden-mobile">
              We sadly couldn't find a description for this artist.
              <br> Try searching for it on <a :href="`https://ecosia.org/search?q=${artistName}&tt=eventowl`" target="_blank">Ecosia</a>.
            </p>
          </div>
        </div>
      </article>
    </div>
    <div
      :class="{'is-active': showDescription}"
      class="modal is-hidden-tablet"
    >
      <div class="modal-background" @click="showDescription=false" />
      <div class="modal-content">
        <div class="box">
          <div v-if="description">
            {{ description }}
            <span v-if="url">
              <br> See more on <a :href="url" target="_blank">Wikipedia</a>.
            </span>
          </div>
          <div v-else>
            We sadly couldn't find a description for this artist.
            <br> Try searching for it on <a :href="`https://ecosia.org/search?q=${artistName}&tt=eventowl`" target="_blank">Ecosia</a>.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const { callBackend } = require('../helpers');

module.exports = {
  props: ['description', 'url', 'artistName', 'imageUrl'],
  data() {
    return {
      showDescription: false,
    };
  },
  methods: {
    remove() {
      this.$emit('removeArtist', this.artistName);
      callBackend(`/artists/${this.artistName}/`, { method: 'delete' });
    },
  },
};
</script>
