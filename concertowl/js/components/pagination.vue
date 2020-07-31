<template>
  <nav class="pagination" role="navigation" aria-label="pagination">
    <a
      :disabled="currentPage === 1"
      class="pagination-previous"
      @click="$emit('changePage', currentPage - 1)"
    >
      Previous
    </a>
    <a
      :disabled="currentPage === lastPage"
      class="pagination-next"
      @click="$emit('changePage', currentPage + 1)"
    >
      Next page
    </a>
    <ul class="pagination-list">
      <li v-for="i in pages" :key="i">
        <a
          :aria-label="`Goto page ${i}`"
          :class="{'is-current': i === currentPage}"
          class="pagination-link"
          @click="$emit('changePage', i)"
        >
          {{ i }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<script>
module.exports = {
  props: ['lastPage', 'currentPage'],
  computed: {
    pages() {
      return Array.from(Array(this.lastPage + 1).keys()).slice(1);
    },
  },
};
</script>
