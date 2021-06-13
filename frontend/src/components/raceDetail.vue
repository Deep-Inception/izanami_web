<template>
  <table>
    <thead>
      <td>コース</td><td>名前</td><td>年齢</td>
    </thead>
    <raceDetailRacerItem v-for='racer in data' :key="racer.couse"  v-bind:racer="racer" />
  </table>
</template>

<script>
import raceDetailRacerItem from './raceDetailRacerItem.vue'
import backendApi from '../mixins/backendApi.js'
export default {
  components: { raceDetailRacerItem },
  data: function () {
    return {data: []}
  },
  mounted () {
    let axios = backendApi()
    let date = this.$route.query.date
    let place = this.$route.query.place
    let race = this.$route.query.race
    axios.get(`api/races/${date}/${place}/${race}`).then(response => { this.data = response.data })
  }
}
</script>
