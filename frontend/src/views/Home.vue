<template>
  <v-container>
    <h3 class="headline">
      Face Recognition
    </h3>
    <QueryUploadImage />
  </v-container>
</template>

<script>
import QueryUploadImage from '@/components/QueryUploadImage.vue'

export default {
  name: 'Home',
  components: {
    QueryUploadImage
  }
}
</script>
