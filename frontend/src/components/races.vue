<template>
  <div>
    <Header></Header>
    <div class="top-wrapper">
      <div class="container">
        <h1>当日レース一覧</h1>
      </div>
    </div>
    <div class="data-wrapper pb-8">
      <div class="container px-8">
        <ul v-for='place_data in races' :key="place_data.place">

          {{getPlace(place_data.place)}}
          <div class='flex'>
              <raceListItem v-for="race in place_data.races" :key="race.race_number" v-bind:race="race">
              </raceListItem>
          </div>
        </ul>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from './header.vue'
import Footer from './footer.vue'
import raceListItem from './raceListItem.vue'
import backendApi from '../mixins/backendApi.js'
export default {
  components: { Header, Footer, raceListItem },
  data: function () {
    return {races: [],
      map: new Map([['01', '桐生'], ['02', '戸田'], ['03', '江戸川'], ['04', '平和島'],
        ['05', '多摩川'], ['06', '浜名湖'], ['07', '蒲郡'], ['08', '常滑'], ['09', '津'],
        ['10', '三国'], ['11', 'びわこ'], ['12', '住之江'], ['13', '尼崎'], ['14', '鳴門'], ['15', '丸亀'],
        ['16', '児島'], ['17', '宮島'], ['18', '徳山'], ['19', '下関'], ['20', '若松'], ['21', '芦屋'],
        ['22', '福岡'], ['23', '唐津'], ['24', '大村']]
      )
    }
  },
  mounted () {
    const axios = backendApi()
    axios.get('api/races', {params: { date: this.$route.query.date }}).then(response => { this.races = response.data })
  },
  methods: {
    getPlace: function (id) {
      return this.map.get(id)
    }
  }
}
</script>
