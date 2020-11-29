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
import Axios from 'axios'
import raceListItem from './raceListItem.vue'
export default {
  components: { raceListItem },
  data: function () {
    return {races: []}
  },
  mounted () {
    const axios = Axios.create({
      // axiosインスタンスの作成
      baseURL: 'http://127.0.0.1:5000/',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      responseType: 'json'
    })
    axios.get('/races', {params: { date: this.$route.query.date }}).then(response => { this.races = response.data })
  }
}
</script>
