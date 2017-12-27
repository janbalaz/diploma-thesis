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
        <h1>Topics</h1>
      </b-row>
      <b-row>
        <p>Please use slider to select how many words per topic should be displayed.</p>
      </b-row>
      <b-row>
        <vue-slider ref="slider" v-model="wordCount" v-bind="sliderOptions" @callback="getTopics"></vue-slider>
      </b-row>
    </b-container>
    <b-container class="topic-block" v-for="(topic, index) in topics" :key="index">
      <b-row class="text-left">
        <a :id="'topic-' + topic.id">
          <h2>Topic {{ topic.id }}</h2>
        </a>
      </b-row>
      <b-row class="text-left">
        <b-col cols="3" v-for="(word, index) in topic.words" :key="index">
          {{ word.word }} ({{ word.value | toPrecision(wordPrecision) }})
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
  import vueSlider from 'vue-slider-component'
  const api = require('../../config/api').default

  export default {
    name: 'Home',
    components: {
      vueSlider
    },
    data () {
      return {
        wordCount: 20,
        defaultWordCount: 20,
        wordPrecision: 4,
        error: '',
        topics: [],
        sliderOptions: {
          eventType: 'auto',
          width: '100%',
          height: 10,
          dotSize: 32,
          dotHeight: null,
          dotWidth: null,
          min: 5,
          max: 100,
          interval: 5,
          show: true,
          speed: 0.5,
          disabled: false,
          piecewise: true,
          piecewiseStyle: null,
          piecewiseLabel: true,
          tooltip: false,
          tooltipDir: 'top',
          reverse: false,
          data: null,
          clickable: true,
          realTime: false,
          lazy: true,
          formatter: null,
          bgStyle: null,
          sliderStyle: null,
          processStyle: null,
          piecewiseActiveStyle: null,
          tooltipStyle: null,
          labelStyle: null,
          labelActiveStyle: null
        }
      }
    },
    created () {
      this.getTopics(this.defaultWordCount)
    },
    methods: {
      getTopics (numWords) {
        api.get(`/categories/?num_words=${numWords}&model=lda`).then((response) => {
          this.topics = response.data
          this.error = ''
        }).catch((error) => {
          if (process.env.NODE_ENV !== 'production') console.log(error)
          this.error = 'Unfortunately topics could not be loaded, please try later.'
        })
      }
    }
  }
</script>

<style scoped>
  .topic-block {
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .alert {
    text-align: left;
    margin-top: 20px;
    width: 100%;
  }
</style>
