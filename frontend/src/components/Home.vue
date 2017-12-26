<template>
    <b-container>
      <b-form @reset="onReset" @submit="onSubmit">
        <b-row>
          <b-form-textarea id="classification-text"
                         v-model="text"
                         placeholder="Enter text to be classified"
                         :rows="18"
                         :max-rows="24">
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
    </b-container>
</template>

<script>
  const api = require('../../config/api').default

  export default {
    name: 'Home',
    data () {
      return {
        text: '',
        error: '',
        success: ''
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
            console.log(response.data.payload.id)
          } else {
            this.error = response.data.payload.error
          }
        }).catch((error) => {
          // TODO: display user-friendly error somehwere
          if (process.env.NODE_ENV !== 'production') console.log(error)
          this.error = 'Text classification failed, please try again.'
        })
      },
      getClassified () {
        // nada
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
