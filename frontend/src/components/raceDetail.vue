<template>
  <table>
    <thead>
      <td>コース</td><td>名前</td><td>年齢</td>
    </thead>
    <raceDetailRacerItem v-for='racer in data' :key="racer.couse"  v-bind:racer="racer" />
  </table>
</template>

<script>
import Axios from 'axios'
import raceDetailRacerItem from './raceDetailRacerItem.vue'
console.log('test')
export default {
  components: { raceDetailRacerItem },
  data: function () {
    return {data: []}
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
    let date = this.$route.query.date
    let place = this.$route.query.place
    let race = this.$route.query.race
    axios.get(`/races/${date}/${place}/${race}`).then(response => { this.data = response.data })
    console.log(this.data)
  }
}
</script>
