<template>
    <b-container>
      <b-form @reset="onReset" @submit.prevent="onSubmit">
        <b-row>
          <b-form-textarea id="classification-text"
                         v-model="text"
                         placeholder="Enter text to be classified"
                         :rows="rows"
                         :max-rows="maxRows">
          </b-form-textarea>
        </b-row>
        <b-row id="button-row">
          <b-button type="submit" size="lg" variant="primary">Go!</b-button>
          <b-button type="reset" size="lg" variant="danger">Reset</b-button>
        </b-row>
      </b-form>
      <b-row v-show="error !== ''">
        <b-alert variant="danger" dismissible :show="error !== ''" @dismissed="error = ''">
          {{ error }}
        </b-alert>
      </b-row>
      <b-row v-show="success !== ''">
        <b-alert variant="success" dismissible :show="success !== ''" @dismissed="success = ''">
          {{ success }}
        </b-alert>
      </b-row>
      <h2 v-show="classified.length">Last classification</h2>
      <b-row v-for="(entry, index) in classified" :key="index">
        <b-col cols="10" class="text-left">{{ entry.text }}</b-col>
        <b-col cols="2">
          <b-row v-for="(topic, index) in entry.categories" :key="index" class="text-right">
            <router-link :to="`/topics#topic-${topic[0]}`">
              Topic {{ topic[0] }} = {{ topic[1] * 100 | toPrecision(topicPrecision) }}%
            </router-link>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
</template>

<script>
  const api = require('../../config/api').default

  export default {
    name: 'Home',
    data () {
      return {
        rows: 18,
        maxRows: 24,
        topicPrecision: 4,
        text: '',
        error: '',
        success: '',
        classified: []
      }
    },
    methods: {
      onReset () {
        this.text = ''
      },
      onSubmit () {
        if (this.text === '') {
          this.error = 'Please fill in the text for classification.'
          return
        }

        api({
          method: 'post',
          url: '/classify/?model=lda',
          data: {
            text: this.text
          }
        }).then((response) => {
          if (response.data.status === true) {
            this.text = ''
            this.error = ''
            this.success = 'Your text was successfully classified.'
            this.getClassified(response.data.payload.id)
          } else {
            this.error = response.data.payload.error
          }
        }).catch((error) => {
          if (process.env.NODE_ENV !== 'production') console.log(error)
          this.error = 'Text classification failed, please try again.'
        })
      },
      getClassified (id) {
        api.get('/classification/?model=lda&id=' + id).then((response) => {
          this.classified = response.data.payload.entries
        }).catch((error) => {
          if (process.env.NODE_ENV !== 'production') console.log(error)
        })
      }
    }
  }
</script>

<style scoped>
  #button-row {
    margin-top: 20px;
  }

  #button-row > button {
    min-width: 200px;
    margin-right: 20px;
  }

  .alert {
    text-align: left;
    margin-top: 20px;
    width: 100%;
  }
</style>
