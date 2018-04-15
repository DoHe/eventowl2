<template>
  <div class="container">
    <artist
      v-for="artist in artistsData"
      :key="artist.name"
      :artist-name="artist.name"
      :image-url="artist.picture_url"
      :description="artist.description"
      :url="artist.url" />
    <div class="has-text-centered add-button" @click="showAddArtist">
      <div class="button is-large">
        <span class="icon is-large">
          <i class="fa fa-plus"/>
        </span>
      </div>
    </div>
    <div class="js-add-modal modal">
      <div class="modal-background" @click="closeModal"/>
      <div class="modal-content">
        <div class="box">
          <div class="field">
            <label class="label">Artist name</label>
            <div class="control has-icons-left">
              <input
                class="js-artist-input input"
                type="text"
                placeholder="Artist name"
                @keyup.enter="addArtist">
              <span class="icon is-small is-left">
                <i class="fas fa-music"/>
              </span>
            </div>
            <p
              :class="{ isInvisible: addWarning === '' }"
              class="js-artist-warning help is-danger">
              {{ addWarning }}
            </p>
          </div>
          <div class="field">
            <div class="control">
              <button class="button is-link" @click="addArtist">Add</button>
            </div>
          </div>
        </div>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="closeModal"/>
    </div>
  </div>
</template>

<script>
const { callBackend } = require('../helpers');
const Artist = require('./artist.vue');

module.exports = {
  props: ['artists'],
  data() {
    return {
      artistsData: this.artists,
      addWarning: '',
    };
  },
  methods: {
    showAddArtist() {
      const input = this.$el.querySelector('.js-artist-input');
      input.value = '';
      this.$el.querySelector('.js-add-modal').classList.add('is-active');
      input.focus();
    },
    closeModal() {
      this.addWarning = '';
      this.$el.querySelector('.js-add-modal').classList.remove('is-active');
    },
    addArtist() {
      let artistName = this.$el.querySelector('.js-artist-input').value;
      if (!artistName) {
        this.addWarning = 'You have to provide a name!';
        return;
      }
      artistName = artistName.toLowerCase();
      if (this.artistsData.some(artist => artistName === artist.name)) {
        this.addWarning = 'You already follow this artist!';
        return;
      }
      this.artistsData.push({ name: artistName, picture_url: '/static/default_artist.jpg' });
      this.closeModal();
      callBackend(`/artists/${artistName}/`, { method: 'post' })
        .then(response => response.json())
        .then((newArtist) => {
          this.artistsData.forEach((artist, index) => {
            if (artist.name === newArtist.name) {
              this.$set(this.artistsData, index, newArtist);
            }
          });
        });
    },
    removeArtist(artistName) {
      this.artistsData = this.artistsData.filter(artist => artist.name !== artistName);
    },
  },
  mounted() {
    this.$on('remove_artist', this.removeArtist);
  },
  components: { Artist },
};
</script>

<style>
  .add-button {
    margin-top: 20px;
  }
</style>
