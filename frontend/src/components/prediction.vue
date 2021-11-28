<template>
    <div>
      <div class="top-wrapper">
        <h1 class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900">AI予想</h1>
        <div class="lg:w-2/3 w-full mx-auto overflow-auto" v-if="data.size != 0">
          <table class="table-auto w-full text-left whitespace-no-wrap">
            <tbody>
              <tr v-if="data.exacta">
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100 rounded-tl rounded-bl">単勝</th>
                <td v-if="data.exacta.length >= 1" class="px-4 py-3">{{data.exacta[0][0]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
                <td v-if="data.exacta.length >= 1" class="px-4 py-3">{{data.exacta[0][1]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
                <td></td>
              </tr>
              <tr v-if="data.exacta">
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100 rounded-tl rounded-bl">二連単</th>
                <td v-if="data.exacta.length >= 1" class="border-t-2 border-gray-200 px-4 py-3">{{data.exacta[0][0]}} - {{data.exacta[0][1]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
                <td v-if="data.exacta.length >= 2" class="border-t-2 border-gray-200 px-4 py-3">{{data.exacta[1][0]}} - {{data.exacta[1][1]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
                <td v-if="data.exacta.length >= 3" class="border-t-2 border-gray-200 px-4 py-3">{{data.exacta[2][0]}} - {{data.exacta[2][1]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
              </tr>
              <tr v-if="data.trifecta">
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100 rounded-tl rounded-bl">三連単</th>
                <td v-if="data.trifecta.length >= 1" class="border-t-2 border-gray-200 px-4 py-3">{{data.trifecta[0][0]}} - {{data.trifecta[0][1]}} - {{data.trifecta[0][2]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
                <td class="border-t-2 border-gray-200 px-4 py-3"></td>
                <td class="border-t-2 border-gray-200 px-4 py-3"></td>
              </tr>
              <tr v-if="data.quinella">
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100 rounded-tl rounded-bl">二連複</th>
                <td v-if="data.quinella.length >= 1" class="border-t-2 border-gray-200 px-4 py-3">{{data.quinella[0][0]}} - {{data.quinella[0][1]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
                <td v-if="data.quinella.length >= 2" class="border-t-2 border-gray-200 px-4 py-3">{{data.quinella[1][0]}} - {{data.quinella[1][1]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
                <td v-if="data.quinella.length >= 3" class="border-t-2 border-gray-200 px-4 py-3">{{data.quinella[2][0]}} - {{data.quinella[2][1]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
              </tr>
              <tr v-if="data.trio">
                <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100 rounded-tl rounded-bl">三連複</th>
                <td v-if="data.trio.length >= 1" class="border-t-2 border-gray-200 px-4 py-3">{{data.trio[0][0]}} - {{data.trio[0][1]}} - {{data.trio[0][2]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
                <td v-if="data.trio.length >= 2" class="border-t-2 border-gray-200 px-4 py-3">{{data.trio[1][0]}} - {{data.trio[1][1]}} - {{data.trio[1][2]}}</td>
                <td v-else class="border-t-2 border-gray-200 px-4 py-3"></td>
                <td class="border-t-2 border-gray-200 px-4 py-3"></td>
              </tr>
            </tbody>
        </table>
        </div>
        <div v-else>
          予想データがありません。発送前のレースの場合は、少々お待ちください。
        </div>
      </div>
    </div>
</template>

<script>
import backendApi from '../mixins/backendApi.js'
export default {
  props: ['date', 'place', 'race'],
  data: function () {
    return {data: []}
  },
  mounted () {
    let axios = backendApi()
    let date = this.date
    let place = this.place
    let race = this.race
    axios.get(`api/view_prediction/${date}/${place}/${race}`, {params: { token: process.env.API_KEY }}).then(response => { this.data = response.data })
  }
}
</script>
