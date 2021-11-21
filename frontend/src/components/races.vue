<template>
  <div class="flex flex-col min-h-screen">
    <Header></Header>
    <section class="text-gray-600 body-font flex-auto">
      <div class="container px-0 py-12 mx-auto">
        <div class="flex flex-col text-center w-full mb-4">
          <h1 class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900">レース一覧</h1>
          <p class="lg:w-2/3 mx-auto leading-relaxed text-base">過去100万以上のレースデータをもとに作られた競艇予想の人工知能（AI）Izanamiがレース結果の予想を教えてくれます。</p>
          <p class="lg:w-2/3 mx-auto leading-relaxed text-base">Races with results are shown in gray, the next race is shown in red, and the race after that is shown in blue. If you want to see the details, click on the race.</p>
        </div>
        <ul v-for='place_data in races' :key="place_data.place">
          <h1 class="text-2xl font-medium title-font text-gray-900 mt-3 mb-1 text-center">{{getPlace(place_data.place)}}</h1>
          <div class="flex flex-wrap">
            <div v-for="race in place_data.races" :key="race.race_number" v-bind:race="race">
              <div class="flex p-2 lg:w-1/12 md:w-1/6 w-full">
                <router-link :to="{name: 'raceDetail', query: {date: date, place: place_data.place, race: race.race_number}}" class="h-full flex items-center border-gray-200 border p-4 rounded-lg" :class="backgroundColor(race.deadline, getPlace(place_data.place))">
                  <div class="flex-grow">
                    <h2 class="text-gray-900 title-font font-medium text-center underline">{{race.race_number}}R</h2>
                    <p class="text-gray-900 text-center">{{race.deadline}}</p>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </ul>
      </div>
    </section>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from './header.vue'
import Footer from './footer.vue'
import backendApi from '../mixins/backendApi.js'
let now = new Date()
let todayStr = now.getFullYear() + ('00' + (now.getMonth() + 1)).slice(-2) + ('00' + now.getDate()).slice(-2)
let flag
flag = 0
let place

export default {
  components: { Header, Footer },
  data: function () {
    return {races: [],
      map: new Map([['01', '桐生'], ['02', '戸田'], ['03', '江戸川'], ['04', '平和島'],
        ['05', '多摩川'], ['06', '浜名湖'], ['07', '蒲郡'], ['08', '常滑'], ['09', '津'],
        ['10', '三国'], ['11', 'びわこ'], ['12', '住之江'], ['13', '尼崎'], ['14', '鳴門'], ['15', '丸亀'],
        ['16', '児島'], ['17', '宮島'], ['18', '徳山'], ['19', '下関'], ['20', '若松'], ['21', '芦屋'],
        ['22', '福岡'], ['23', '唐津'], ['24', '大村']]
      ),
      date: this.$route.query.date ? this.$route.query.date : todayStr
    }
  },
  mounted () {
    const axios = backendApi()
    axios.get('api/races', {params: { date: this.date, token: process.env.API_KEY }}).then(response => { this.races = response.data })
  },
  methods: {
    getPlace: function (id) {
      return this.map.get(id)
    },
    twoDigit: function (num) {
      let ret
      if (num < 10) {
        ret = '0' + num
      } else {
        ret = num
      }
      return ret
    },
    backgroundColor: function (deadline, racePlace) {
      if (this.$route.query.date > todayStr) {
        return 'blue'
      } else if (this.$route.query.date < todayStr) {
        return 'gray'
      }
      if (place !== racePlace) {
        flag = 0
        place = racePlace
      }
      if (deadline < this.twoDigit(now.getHours()) + ':' + this.twoDigit(now.getMinutes())) {
        flag = 0
        return 'gray'
      } else if (flag === 0) {
        flag = 1
        return 'red'
      }
      return 'blue'
    }
  }
}
</script>

<style>
.gray {
  background-color: rgba(229, 231, 235)
}
.red {
  background-color: rgba(254, 202, 202)
}
.blue {
  background-color: rgba(219, 234, 254)
}
</style>
