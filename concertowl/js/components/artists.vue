<template>
  <div class="container">
    <div v-for="artist in artistsData" :key="artist.name">
      <artist
        :artist-name="artist.name"
        :image-url="artist.picture_url"
        :description="artist.description"
        :url="artist.url"/>
    </div>
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
            <p class="js-artist-warning help is-invisible is-danger">You have to provide an artist name</p>
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
const Artist = require('./artist.vue');

module.exports = {
  props: ['artists'],
  data() {
    return {
      artistsData: this.artists,
    };
  },
  methods: {
    showAddArtist() {
      this.$el.querySelector('.js-artist-warning').classList.add('is-invisible');
      const input = this.$el.querySelector('.js-artist-input');
      input.value = '';
      this.$el.querySelector('.js-add-modal').classList.add('is-active');
      input.focus();
    },
    closeModal() {
      this.$el.querySelector('.js-add-modal').classList.remove('is-active');
    },
    addArtist() {
      const artistName = this.$el.querySelector('.js-artist-input').value;
      if (!artistName) {
        this.$el.querySelector('.js-artist-warning').classList.remove('is-invisible');
        return;
      }
      this.artists.push({ name: artistName, picture_url: '/media/artist/default.jpg' });
      this.closeModal();
    },
    removeArtist(artistName) {
      console.log(`blub: ${artistName}`);
    },
  },
  components: { Artist },
};
</script>

<style>
  .add-button {
    margin-top: 20px;
  }
</style>
