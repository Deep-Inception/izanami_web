<template>
  <div class="flex flex-col min-h-screen">
    <Header></Header>
    <section class="text-gray-600 body-font flex-auto">
      <div class="container px-0 py-12 mx-auto">
        <div class="flex flex-col text-center w-full mb-4">
          <h1 class="sm:text-3xl text-2xl font-medium title-font mb-2 text-gray-900">過去予想結果</h1>
          <p class="mx-auto leading-relaxed text-base">条件を指定してIzanamiを使用した場合の収益を確認できます。</p>
        </div>
        <div class="flex flex-wrap mt-3">
          <div class="flex flex-col text-center w-full mb-5">
            <h2 class="text-3xl tracking-widest font-medium title-font mb-1">条件</h2>
          </div>
          <div class="p-4 lg:w-1/3 w-full">
            <div class="flex rounded-lg h-full bg-gray-100 p-8 flex-col">
              <div class="flex items-center mb-3">
                <div class="w-8 h-8 mr-3 inline-flex items-center justify-center rounded-full bg-indigo-500 text-white flex-shrink-0">
                  <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-5 h-5" viewBox="0 0 24 24">
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                  </svg>
                </div>
                <h2 class="text-gray-900 text-lg title-font font-medium">船券の種類</h2>
              </div>
              <div class="flex-grow">
                <div class="relative">
                  <select class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="ticketType" name="ticketType">
                    <option>単勝</option>
                  </select>
                  <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="p-4 lg:w-1/3 w-full">
            <div class="flex rounded-lg h-full bg-gray-100 p-8 flex-col">
              <div class="flex items-center mb-3">
                <div class="w-8 h-8 mr-3 inline-flex items-center justify-center rounded-full bg-indigo-500 text-white flex-shrink-0">
                  <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-5 h-5" viewBox="0 0 24 24">
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                  </svg>
                </div>
                <h2 class="text-gray-900 text-lg title-font font-medium">日付</h2>
              </div>
              <div class="flex-grow">
                <div class="relative">
                  <input type="date" class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-3 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="raceDate" name="raceDate">
                </div>
              </div>
            </div>
          </div>
          <div class="p-4 lg:w-1/3 w-full">
            <div class="flex rounded-lg h-full bg-gray-100 p-8 flex-col">
              <div class="flex items-center mb-3">
                <div class="w-8 h-8 mr-3 inline-flex items-center justify-center rounded-full bg-indigo-500 text-white flex-shrink-0">
                  <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-5 h-5" viewBox="0 0 24 24">
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                  </svg>
                </div>
                <h2 class="text-gray-900 text-lg title-font font-medium">会場</h2>
              </div>
              <div class="flex-grow">
                <div class="relative">
                  <select class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="place" name="place">
                    <option>01# 桐生</option><option>02# 戸田</option><option>03# 江戸川</option><option>04# 平和島</option><option>05# 多摩川</option><option>06# 浜名湖</option>
                    <option>07# 蒲郡</option><option>08# 滑</option><option>09# 津</option><option>10# 三国</option><option>11# びわこ</option><option>12# 住之江</option>
                    <option>13# 尼崎</option><option>14# 鳴門</option><option>15# 丸亀</option><option>16# 児島</option><option>17# 宮島</option><option>18# 徳山</option>
                    <option>19# 下関</option><option>20# 若松</option><option>21# 芦屋</option><option>22# 福岡</option><option>23# 唐津</option><option>24# 大村</option>
                  </select>
                  <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                    <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <button class="flex mx-auto text-white bg-indigo-500 border-0 py-2 px-8 focus:outline-none hover:bg-indigo-600 rounded text-lg" v-on:click="checkResult">結果確認</button>
        </div>
        <div class="flex flex-col text-center w-full  mt-10 mb-5">
          <h2 class="text-3xl tracking-widest font-medium title-font mb-1">結果</h2>
          <div id="NGMessage" class="text-m text-gray-500 mt-3 text-red-400"></div>
        </div>
        <div class="flex flex-wrap mt-3 w-4/5 mx-auto">
          <div class="p-4 lg:w-1/2 w-full">
            <div class="bg-gray-100 rounded flex p-4 h-full items-center">
              <div class="w-8 h-8 mr-3 inline-flex items-center justify-center rounded-full text-white flex-shrink-0">
                <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" class="text-indigo-500 w-6 h-6 flex-shrink-0 mr-4" viewBox="0 0 24 24">
                  <path d="M22 11.08V12a10 10 0 11-5.93-9.14"></path>
                  <path d="M22 4L12 14.01l-3-3"></path>
                </svg>
              </div>
              <h2 class="text-gray-900 text-lg title-font font-medium">回収率</h2>
              <div class="ml-auto flex">
                <h2 id="recoveryRate" class="title-font font-medium text-black"></h2>
                <h2 class="title-font font-medium text-black">%</h2>
              </div>
            </div>
          </div>
          <div class="p-4 lg:w-1/2 w-full">
            <div class="bg-gray-100 rounded flex p-4 h-full items-center">
              <div class="w-8 h-8 mr-3 inline-flex items-center justify-center rounded-full text-white flex-shrink-0">
                <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" class="text-indigo-500 w-6 h-6 flex-shrink-0 mr-4" viewBox="0 0 24 24">
                  <path d="M22 11.08V12a10 10 0 11-5.93-9.14"></path>
                  <path d="M22 4L12 14.01l-3-3"></path>
                </svg>
              </div>
              <h2 class="text-gray-900 text-lg title-font font-medium">的中率</h2>
              <div class="ml-auto flex">
                 <h2 id="hitRate" class="title-font font-medium text-black"></h2>
                 <h2 class="title-font font-medium text-black">%</h2>
              </div>
            </div>
          </div>
          <div class="p-4 lg:w-1/2 w-full">
            <div class="bg-gray-100 rounded flex p-4 h-full items-center">
              <div class="w-8 h-8 mr-3 inline-flex items-center justify-center rounded-full text-white flex-shrink-0">
                <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" class="text-indigo-500 w-6 h-6 flex-shrink-0 mr-4" viewBox="0 0 24 24">
                  <path d="M22 11.08V12a10 10 0 11-5.93-9.14"></path>
                  <path d="M22 4L12 14.01l-3-3"></path>
                </svg>
              </div>
              <h2 class="text-gray-900 text-lg title-font font-medium">購入金額</h2>
              <div class="ml-auto flex">
                 <h2 id="purchaseAmount" class="title-font font-medium text-black"></h2>
                 <h2 class="title-font font-medium text-black">円</h2>
              </div>
            </div>
          </div>
          <div class="p-4 lg:w-1/2 w-full">
            <div class="bg-gray-100 rounded flex p-4 h-full items-center">
              <div class="w-8 h-8 mr-3 inline-flex items-center justify-center rounded-full text-white flex-shrink-0">
                <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" class="text-indigo-500 w-6 h-6 flex-shrink-0 mr-4" viewBox="0 0 24 24">
                  <path d="M22 11.08V12a10 10 0 11-5.93-9.14"></path>
                  <path d="M22 4L12 14.01l-3-3"></path>
                </svg>
              </div>
              <h2 class="text-gray-900 text-lg title-font font-medium">購入回数</h2>
              <div class="ml-auto flex">
                 <h2 id="purchaseCount" class="title-font font-medium text-black"></h2>
                 <h2 class="title-font font-medium text-black">回</h2>
              </div>
            </div>
          </div>
          <div class="p-4 w-full">
            <div class="bg-gray-100 rounded flex p-4 h-full items-center">
              <div class="w-8 h-8 mr-3 inline-flex items-center justify-center rounded-full text-white flex-shrink-0">
                <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" class="text-indigo-500 w-6 h-6 flex-shrink-0 mr-4" viewBox="0 0 24 24">
                  <path d="M22 11.08V12a10 10 0 11-5.93-9.14"></path>
                  <path d="M22 4L12 14.01l-3-3"></path>
                </svg>
              </div>
              <h2 class="text-gray-900 text-lg title-font font-medium">収支</h2>
              <div class="ml-auto flex">
                 <h2 id="balance" class="title-font font-medium text-black"></h2>
                 <h2 class="title-font font-medium text-black">円</h2>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from './header.vue'
import Footer from './footer.vue'
import backendApi from '../mixins/backendApi.js'
export default {
  name: 'statistics',
  components: { Header, Footer },
  data: function () {
    return {
      ticketType: '',
      raceDate: '',
      place: ''
    }
  },
  mounted () {
    var objDate = new Date()
    objDate.setDate(objDate.getDate() - 1)
    var year = objDate.getFullYear()
    var month = objDate.getMonth() + 1
    var day = objDate.getDate()
    document.getElementById('raceDate').value = year + '-' + ('00' + month).slice(-2) + '-' + ('00' + day).slice(-2)
  },
  methods: {
    checkResult: function (event) {
      document.getElementById('recoveryRate').innerHTML = null
      document.getElementById('hitRate').innerHTML = null
      document.getElementById('purchaseAmount').innerHTML = null
      document.getElementById('purchaseCount').innerHTML = null
      document.getElementById('balance').innerHTML = null
      document.getElementById('NGMessage').innerHTML = null
      const axios = backendApi()
      // axiosのthenメソッドの中ではthisがvueコンポーネントを指さなくなるので別の変数に割り当てておく
      // var self = this
      // バックエンドのAPIサーバにリクエストを送信
      axios.get('api/statistics', {
        // クエリパラメータをセット
        params: {
          ticketType: document.getElementById('ticketType').value,
          raceDate: document.getElementById('raceDate').value,
          place: document.getElementById('place').value.slice(0, 2)
        }
      }).then(function (response) {
        if (response.data.result === 'success') {
          document.getElementById('recoveryRate').innerHTML = response.data.recoveryRate
          document.getElementById('hitRate').innerHTML = response.data.hitRate
          document.getElementById('purchaseAmount').innerHTML = response.data.purchaseAmount.toLocaleString()
          document.getElementById('purchaseCount').innerHTML = response.data.purchaseCount
          var balance = response.data.balance
          if (balance >= 0) {
            document.getElementById('balance').innerHTML = '+' && balance.toLocaleString()
          } else {
            document.getElementById('balance').innerHTML = balance.toLocaleString()
          }
        } else {
          document.getElementById('NGMessage').innerHTML = '結果を取得できませんでした。'
        }
      })
    }
  }
}
</script>

<style>
</style>
