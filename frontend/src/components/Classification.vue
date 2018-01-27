<template>
  <div>
    <b-container v-show="error !== ''">
      <b-row>
        <b-alert variant="danger" dismissible :show="error !== ''" @dismissed="error = ''">
          {{ error }}
        </b-alert>
      </b-row>
    </b-container>
    <b-container>
      <b-row>
        <h1>Classified Texts</h1>
      </b-row>
      <b-row>
        <p>Below is history of all classified texts for given model.</p>
      </b-row>
    </b-container>
    <b-container class="block" v-for="(entry, index) in classified" :key="index">
      <b-row>
        <b-col cols="10" class="text-left">
          {{ entry.text }}
        </b-col>
        <b-col cols="2">
          <b-row v-for="(topic, index) in entry.categories" :key="index" class="text-right">
            <router-link :to="`/topics#topic-${topic[0]}`">
              Topic {{ topic[0] }} = {{ topic[1] * 100 | toPrecision(topicPrecision) }}%
            </router-link>
          </b-row>
        </b-col>
      </b-row>
      <hr />
    </b-container>
  </div>
</template>

<script>
  const api = require('../../config/api').default

  export default {
    name: 'Classification',
    data () {
      return {
        error: '',
        topicPrecision: 4,
        classified: []
      }
    },
    created () {
      this.getAllClassified()
    },
    methods: {
      getAllClassified () {
        api.get(`/classification/?model=lsi`).then((response) => {
          if (response.data.status === true) {
            this.classified = response.data.payload.entries
            this.error = ''
          } else {
            this.error = response.data.payload.error
          }
        }).catch((error) => {
          if (process.env.NODE_ENV !== 'production') console.log(error)
          this.error = 'Unfortunately topics could not be loaded, please try later.'
        })
      }
    }
  }
</script>

<style scoped>
  .block {
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .alert {
    text-align: left;
    margin-top: 20px;
    width: 100%;
  }
</style>
