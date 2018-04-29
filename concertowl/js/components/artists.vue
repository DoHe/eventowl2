<template>
  <div class="container">
    <artist
      v-for="artist in artistsData.slice(page * perPage, (page + 1) * perPage)"
      :key="artist.name"
      :artist-name="artist.name"
      :image-url="artist.picture_url"
      :description="artist.description"
      :url="artist.url"
      @removeArtist="removeArtist" />
    <div class="has-text-centered add-button" @click="showAddArtistModal = true">
      <div class="button is-large">
        <span class="icon is-large">
          <i class="fa icon-plus"/>
        </span>
      </div>
    </div>
    <AddArtistModal
      :show="showAddArtistModal"
      :artists="artistsData"
      @haveArtist="addDefaultArtist"
      @updateArtistInfo="updateArtistInfo"
      @closeAddArtistModal="showAddArtistModal = false"
    />
    <Pagination
      :current-page="page"
      :last-page="Math.ceil(artists.length / perPage)"
      @changePage="changePage" />
  </div>
</template>

<script>
const Artist = require('./artist.vue');
const AddArtistModal = require('./addArtistModal.vue');
const Pagination = require('./pagination.vue');

module.exports = {
  props: ['artists'],
  data() {
    return {
      artistsData: this.artists,
      page: 0,
      perPage: 5,
      showAddArtistModal: false,
    };
  },
  methods: {
    addDefaultArtist(artistName) {
      this.artistsData.push({ name: artistName, picture_url: '/static/default_artist.jpg' });
    },
    updateArtistInfo(artistInfo) {
      this.artistsData.forEach((artist, index) => {
        if (artist.name === artistInfo.name) {
          this.$set(this.artistsData, index, artistInfo);
        }
      });
    },
    removeArtist(artistName) {
      this.artistsData = this.artistsData.filter(artist => artist.name !== artistName);
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
