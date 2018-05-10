<template>
  <div :class="{'is-active': show}" class="modal" >
    <div class="modal-background" @click="closeModal"/>
    <div class="modal-content">
      <div class="box">
        <div class="tabs is-boxed">
          <ul>
            <li :class="{'is-active': mode==='manual'}" @click="mode = 'manual'">
              <a>Manual</a>
            </li>
            <li :class="{'is-active': mode==='spotify'}" @click="mode = 'spotify'">
              <a>Spotify</a>
            </li>
          </ul>
        </div>
        <div v-if="mode==='manual'">
          <div class="field">
            <label class="label">Artist name</label>
            <div class="control has-icons-left">
              <input
                ref="artistInput"
                v-model="artistName"
                class="js-artist-input input"
                type="text"
                placeholder="Artist name"
                @keyup.enter="addArtist">
              <span class="icon is-small is-left">
                <i class="fas icon-music"/>
              </span>
            </div>
            <p
              :class="{ 'is-invisible': warning === '' }"
              class="help is-danger">
              {{ warning }}
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
          <p
            :class="{ 'is-invisible': !importing }"
            class="help is-warning">
            The import is running in the background. Feel free to close this window.
          </p>
        </div>
      </div>
    </div>
    <button class="modal-close is-large" aria-label="close" @click="closeModal"/>
  </div>
</template>

<script>
const { callBackend } = require('../helpers');
const url = require('url');
const querystring = require('querystring');

module.exports = {
  props: ['artists', 'show', 'importRunning'],
  data() {
    return {
      warning: '',
      mode: 'manual',
      importing: this.importRunning,
    };
  },
  watch: {
    show() {
      if (this.show) {
        this.focusInput();
      } else {
        this.closeModal();
      }
    },
    mode() {
      this.focusInput();
    },
  },
  methods: {
    focusInput() {
      if (this.mode !== 'manual') return;
      setTimeout(() => {
        this.$refs.artistInput.focus();
      });
    },
    closeModal() {
      this.warning = '';
      this.artistName = '';
      this.$emit('closeAddArtistModal');
    },
    addArtist() {
      if (!this.artistName) {
        this.warning = 'You have to provide a name!';
        return;
      }
      const artistName = this.artistName.toLowerCase();
      if (this.artists.some(artist => artistName === artist.name)) {
        this.warning = 'You already follow this artist!';
        return;
      }
      this.$emit('haveArtist', artistName);
      this.closeModal();
      callBackend(`/artists/${artistName}/`, { method: 'post' })
        .then(response => response.json())
        .then((artistInfo) => {
          this.$emit('updateArtistInfo', artistInfo);
        });
    },
    importFromSpotify() {
      this.importing = true;
      const spotifyUrl = url.parse('https://accounts.spotify.com/authorize');
      spotifyUrl.search = querystring.stringify({
        client_id: process.env.SPOTIFY_ID,
        response_type: 'code',
        redirect_uri: process.env.SPOTIFY_URL,
        scope: 'user-library-read user-follow-read playlist-read-private playlist-read-collaborative',
      });
      const spotifyWindow = window.open(url.format(spotifyUrl), '', 'width=500,height=500');
      spotifyWindow.onunload = () => {
        window.setTimeout(() => {
          spotifyWindow.close();
        }, 0);
      };
    },
  },
};
</script>
