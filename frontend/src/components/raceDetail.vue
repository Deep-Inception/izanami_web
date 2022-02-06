<template>
    <div>
      <Header></Header>
      <div class="lg:flex xl:flex">
        <div class="top-wrapper flex-auto lg:w-4/5 xl:w-4/5">
          <h1 class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900 text-center">{{getPlaceName(this.$route.query.place)}} 第 {{ this.$route.query.race }} R</h1>
          <Prediction  :date="this.$route.query.date" :place="this.$route.query.place" :race="this.$route.query.race"></Prediction>
          <h1 class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900 text-center">レース情報</h1>
          <div class="lg:w-5/6 w-full mx-auto overflow-auto">
            <table class="table-auto w-full text-left whitespace-no-wrap">
              <thead>
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100 rounded-tl rounded-bl">コース</th>
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100">登録番号</th>
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100">名前（年齢/体重）</th>
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100">級別</th>
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100">勝率(当地)</th>
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100">連率(当地)</th>
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100">展示タイム</th>
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100">チルト</th>
                <th class="w-10 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100 rounded-tr rounded-br">順位</th>
              </thead>
              <raceDetailRacerItem v-for='racer in data' :key="racer.couse"  v-bind:racer="racer" />
            </table>
            <div class="flex pl-4 mt-4 w-full mx-auto">
              <a class="text-indigo-500 inline-flex items-center md:mb-2 lg:mb-0" :href="boatraceLink(this.$route.query.date, this.$route.query.place, this.$route.query.race)">レース詳細
                <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-4 h-4 ml-2" viewBox="0 0 24 24">
                  <path d="M5 12h14M12 5l7 7-7 7"></path>
                </svg>
              </a>
            </div>
          </div>
        </div>
        <SideBar id="sidebar" class="lg:mt-16 xl:mt-16 lg:w-1/6 xl:w-1/6 m-0 p-5 w-full lg:static h-auto overflow-visible"/>
      </div>
      <Footer></Footer>
    </div>
</template>

<script>
import Header from './header.vue'
import Footer from './footer.vue'
import Prediction from './prediction.vue'
import SideBar from './sidebar.vue'
import raceDetailRacerItem from './raceDetailRacerItem.vue'
import backendApi from '../mixins/backendApi.js'
import utilsMixin from '../mixins/utils.js'
export default {
  mixins: [utilsMixin],
  components: { Header, Footer, Prediction, raceDetailRacerItem, SideBar },
  data: function () {
    return {data: []}
  },
  mounted () {
    let axios = backendApi()
    let date = this.$route.query.date
    let place = this.$route.query.place
    let race = this.$route.query.race
    axios.get(`api/races/${date}/${place}/${race}`, {params: { token: process.env.API_KEY }}).then(response => { this.data = response.data })
  },
  methods: {
    boatraceLink: function (date, place, race) {
      return 'https://www.boatrace.jp/owpc/pc/race/racelist?rno=' + race + '&jcd=' + place + '&hd=' + date
    }
  }
}
</script>
