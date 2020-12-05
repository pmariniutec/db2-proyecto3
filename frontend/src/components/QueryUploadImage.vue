<template>
  <v-row>
    <v-col
      cols="6"
      align="center"
      >
      <v-file-input
        id="file"
        chips
        label="Subir foto"
        :loading="loading"
        class="input is-rounded"
        @change="handleFileUpload"
        />
        <v-btn
          color="primary"
          :loading="loading"
          @click="uploadFile"
          >
          Buscar
        </v-btn>
    </v-col>

      <v-col
        cols="6"
        >
        <v-row
          v-if="cardLoading"
          dense
          >
          <v-col cols="6">
            <v-card
              :loading="loading"
              height="250px"
              />
          </v-col>
          <v-col cols="6">
            <v-card
              :loading="loading"
              height="250px"
              />
          </v-col>
        </v-row>
        <v-row
          v-else
          dense
          >
          <v-col
            v-for="(image, id) in images"
            :key="id"
            cols="6"
            >
            <v-card>
              <v-img :src="image.url" />
                <v-card-title v-text="image.title" />
                </v-card>
          </v-col>
        </v-row>
      </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'QueryImageUpload',
  data () {
    return {
      file: null,
      loading: false,
      cardLoading: false,
      images: []
    }
  },
  methods: {
    handleFileUpload (file) {
      this.file = file
    },
    uploadFile () {
      const formData = new FormData()
      formData.append('file', this.file)
      const instance = this.axios.create({
        baseURL: 'http://127.0.0.1:8000/',
        headers: {
          'content-type': 'multipart/form-data'
        }
      })
      this.loading = true
      this.cardLoading = true
      instance.post('api/query/', formData)
        .then(({ data }) => {
          this.images = data.images.map((image) => {
            return { url: 'http://127.0.0.1:8000' + image.url, title: image.title }
          })
          this.loading = false
          this.cardLoading = false
        })
        .catch((err) => {
          console.log(err)
          this.loading = false
          this.cardLoading = false
        })
    }
  }
}
</script>

<style lang="scss">
</style>
