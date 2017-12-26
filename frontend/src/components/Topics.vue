<template>
  <div>
    <b-container class="topic-block" v-for="(topic, index) in topics" :key="index">
      <b-row class="text-left">
        <h2>Topic {{ topic.id }}</h2>
      </b-row>
      <b-row class="text-left">
        <b-col cols="3" v-for="(word, index) in topic.words" :key="index">
          {{ word.word }} ({{ word.value | toPrecision(4) }})
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
  const api = require('../../config/api').default

  export default {
    name: 'Home',
    data () {
      return {
        topics: [],
        name: 'Welcome to Your Vue.js App'
      }
    },
    created () {
      this.getTopics()
    },
    methods: {
      getTopics () {
        api.get('/categories/?num_words=20&model=lda').then((response) => {
          this.topics = response.data
        }).catch((error) => {
          // TODO: display user-friendly error somehwere
          if (process.env.NODE_ENV !== 'production') console.log(error)
        })
      }
    },
    computed: {
      showAlert () {
        return this.name.length > 4
      }
    }
  }
</script>

<style scoped>
  .topic-block {
    margin-bottom: 20px;
  }
</style>
