<template>
  <div>
    <ul v-for='place_data in races' :key="place_data.place">
      レース会場 {{ place_data.place }}
      <div class='flex'>
          <raceListItem v-for="race in place_data.races" :key="race.race_number" v-bind:race="race">
          </raceListItem>
      </div>
    </ul>
  </div>
</template>

<script>
import raceListItem from './raceListItem.vue'
import backendApi from '../mixins/backendApi.js'
export default {
  components: { raceListItem },
  data: function () {
    return {races: []}
  },
  mounted () {
    const axios = backendApi()
    axios.get('/races', {params: { date: this.$route.query.date }}).then(response => { this.races = response.data })
  }
}
</script>
