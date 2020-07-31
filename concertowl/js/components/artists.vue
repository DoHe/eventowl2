<template>
  <div class="container">
    <artist
      v-for="artist in artistsData.slice((page-1) * perPage, page * perPage)"
      :key="artist.name"
      :artist-name="artist.name"
      :image-url="artist.picture_url"
      :description="artist.description"
      :url="artist.url"
      @removeArtist="removeArtist"
    />
    <div class="has-text-centered add-button" @click="showAddArtistModal = true">
      <div class="button is-large">
        <span class="icon is-large">
          <i class="fa icon-plus" />
        </span>
      </div>
    </div>
    <AddArtistModal
      :show="showAddArtistModal"
      :artists="artistsData"
      :import-running="spotifyImportRunning"
      @haveArtist="addDefaultArtist"
      @updateArtistInfo="updateArtistInfo"
      @closeAddArtistModal="showAddArtistModal = false"
    />
    <Pagination
      :current-page="page"
      :last-page="Math.ceil(artists.length / perPage)"
      @changePage="changePage"
    />
  </div>
</template>

<script>
const Artist = require('./artist.vue');
const AddArtistModal = require('./addArtistModal.vue');
const Pagination = require('./pagination.vue');

module.exports = {
  props: ['artists', 'spotifyImportRunning'],
  data() {
    return {
      artistsData: this.artists,
      page: 1,
      perPage: 50,
      showAddArtistModal: false,
    };
  },
  methods: {
    addDefaultArtist(artistName) {
      const artistInfo = { name: artistName, picture_url: '/static/default_artist.jpg' };
      let added = false;
      let i = 0;
      for (i = 0; i < this.artistsData.length; i += 1) {
        if (this.artistsData[i].name > artistName) {
          this.artistsData.splice(i, 0, artistInfo);
          added = true;
          break;
        }
      }
      if (!added) {
        this.artistsData.push(artistInfo);
      }
    },
    updateArtistInfo(artistInfo) {
      this.artistsData.forEach((artist, index) => {
        if (artist.name === artistInfo.name) {
          this.$set(this.artistsData, index, artistInfo);
        }
      });
    },
    removeArtist(artistName) {
      this.artistsData = this.artistsData.filter((artist) => artist.name !== artistName);
    },
    changePage(page) {
      this.page = page;
    },
  },
  components: { Artist, AddArtistModal, Pagination },
};
</script>

<style>
  .add-button {
    margin-top: 20px;
  }
</style>
