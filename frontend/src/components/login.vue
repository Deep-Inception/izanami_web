<template>
  <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Top</title>
    </head>
    <body>
      <Header :loginScreen="loginScreen"></Header>
      <section class="text-gray-600 body-font">
        <div class="container px-5 py-24 mx-auto flex flex-wrap items-center">
          <div class="lg:w-3/8 md:w-1/2 md:pr-16 lg:pr-0 pr-0">
            <h1 class="title-font font-medium text-3xl text-gray-900">競艇結果予測AI Izanami</h1>
            <p class="leading-relaxed mt-4">Mizuhanome is just urine of Izanami.</p>
          </div>
          <div class="lg:w-2/6 md:w-1/2 bg-gray-100 rounded-lg p-8 flex flex-col lg:ml-4 md:ml-auto w-full mt-10 md:mt-0">
            <h2 class="text-gray-900 text-lg font-medium title-font mb-5">Sign in to Izanami</h2>
            <div class="relative mb-4">
              <label for="Email" class="leading-7 text-sm text-gray-600">Email</label>
              <input type="text" id="Email" name="Email" class="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out">
            </div>
            <div class="relative mb-4">
              <label for="Password" class="leading-7 text-sm text-gray-600">Password</label>
              <input type="Password" id="Password" name="Password" class="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out">
            </div>
            <button class="text-white bg-indigo-500 border-0 py-2 px-8 focus:outline-none hover:bg-indigo-600 rounded text-lg" v-on:click="checklogin">Sign In</button>
            <p class="text-xs text-gray-500 mt-3"></p>
            <div id="loginResult" class="text-xs text-gray-500 mt-3 text-red-400"></div>
          </div>
        </div>
      </section>
      <Footer></Footer>
    </body>
  </html>
</template>

<script>
import Header from './header.vue'
import Footer from './footer.vue'
import backendApi from '../mixins/backendApi.js'
import { KJUR } from 'jsrsasign'
import router from '../router/index.js'
export default {
  name: 'login',
  components: {
    Header,
    Footer
  },
  data: function () {
    return {
      Email: '',
      Password: '',
      loginScreen: true
    }
  },
  methods: {
    checklogin: function (event) {
      document.getElementById('loginResult').innerHTML = ''
      // checkloginイベント(htmlファイル内で定義している)の内容を記述
      const axios = backendApi()
      var nextPage = 'index'

      // axiosのthenメソッドの中ではthisがvueコンポーネントを指さなくなるので別の変数に割り当てておく
      var self = this
      // バックエンドのAPIサーバにリクエストを送信
      axios.get('api/login', {
        // クエリパラメータをセット
        params: {
          email: document.getElementById('Email').value,
          password: document.getElementById('Password').value
        }
      }).then(function (response) {
        console.log(response)
        // 応答が戻ってきたら結果を処理。
        // "success" だったら次のページにジャンプし、失敗だったらその旨表示
        if (response.data.result === 'success') {
          // JWTトークンの生成
          var token = self.generateToken(document.getElementById('Email').value)
          // cookieとしてトークンを付与
          document.cookie = 'token=' + token
          // 次のページにジャンプ
          router.push({name: nextPage})
        } else {
          document.getElementById('loginResult').innerHTML = 'ログイン失敗'
        }
      })
    },
    generateToken: function (Email) {
      /* JWTトークンの生成 */
      // JWT用のシークレットトークンをセット(【注意】実際にはコードの中に書いてはいけない！)
      var secretToken = 'oreore'
      // JWTのヘッダー部を定義
      var oHeader = {alg: 'HS256', typ: 'JWT'}
      // JWTペイロードを作成
      var offset = Math.floor(Math.random() * Math.floor(25))
      var DO = new Date()
      DO.setSeconds(DO.getSeconds() + offset)
      var dY = DO.getFullYear()
      var dm = DO.getMonth() + 1
      var dd = DO.getDate()
      var dH = ('0' + DO.getHours()).slice(-2)
      var dM = ('0' + DO.getMinutes()).slice(-2)
      var dS = ('0' + DO.getSeconds()).slice(-2)
      var dStr = dY + '/' + dm + '/' + dd + ' ' + dH + ':' + dM + ':' + dS + ' +0900'
      var oPayload = {Email: Email, until: dStr}
      console.log(oHeader, oPayload)
      // JWTを生成
      var sJWT = KJUR.jws.JWS.sign('HS256', JSON.stringify(oHeader), JSON.stringify(oPayload), secretToken)
      console.log(sJWT)
      return sJWT
    }
  }
}
</script>
