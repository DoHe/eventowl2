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
          <i class="fa icon-plus"/>
        </span>
      </div>
    </div>
    <div class="js-add-modal modal">
      <div class="modal-background" @click="closeModal"/>
      <div class="modal-content">
        <div class="box">
          <div class="tabs is-boxed">
            <ul>
              <li :class="{'is-active': addMode==='manual'}" @click="addMode = 'manual'">
                <a>Manual</a>
              </li>
              <li :class="{'is-active': addMode==='spotify'}" @click="addMode = 'spotify'">
                <a>Spotify</a>
              </li>
            </ul>
          </div>
          <div v-if="addMode==='manual'">
            <div class="field">
              <label class="label">Artist name</label>
              <div class="control has-icons-left">
                <input
                  class="js-artist-input input"
                  type="text"
                  placeholder="Artist name"
                  @keyup.enter="addArtist">
                <span class="icon is-small is-left">
                  <i class="fas icon-music"/>
                </span>
              </div>
              <p
                :class="{ 'is-invisible': addWarning === '' }"
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
          <div v-else>
            <p>Import your artists from Spotify</p>
            <button
              :class="{ 'is-loading': importing }"
              class="button is-link"
              @click="importFromSpotify">
              Import
            </button>
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
const url = require('url');
const querystring = require('querystring');

module.exports = {
  props: ['artists'],
  data() {
    return {
      artistsData: this.artists,
      addWarning: '',
      addMode: 'manual',
      importing: false,
    };
  },
  methods: {
    showAddArtist() {
      const input = this.$el.querySelector('.js-artist-input');
      if (input) {
        input.value = '';
      }
      this.$el.querySelector('.js-add-modal').classList.add('is-active');
      if (input) {
        input.focus();
      }
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
    importFromSpotify() {
      this.importing = true;
      const spotifyUrl = url.parse('https://accounts.spotify.com/authorize');
      spotifyUrl.search = querystring.stringify({
        client_id: '4674d20a8f804e5d85c8cc13a2791b73',
        response_type: 'code',
        redirect_uri: 'http://0.0.0.0:8000/spotify',
        scope: 'user-library-read user-follow-read playlist-read-private playlist-read-collaborative',
        state: 'notrandom',
      });
      const spotifyWindow = window.open(url.format(spotifyUrl), '', 'width=500,height=500');
      spotifyWindow.onunload = () => {
        window.setTimeout(() => {
          console.log(spotifyWindow.location);
          spotifyWindow.close();
        }, 0);
      };
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
