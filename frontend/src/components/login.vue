<template>
  <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Top</title>
    </head>
    <body>
      <Header></Header>
      <div class="top-wrapper">
        <div class="container">
          <h1>競艇結果AI予測</h1>
        </div>
      </div>
      <div class="login-wrapper">
        <div class="container">
          <div class="heading">
            <h2>ログイン</h2>
            <div id="loginResult"></div>
          </div>
          <div class="login">
            <p><input type="text" id="email" placeholder="email"></p>
            <p><input type="password" id="password" placeholder="password"></p>
            <p><button class="btn" v-on:click="checklogin">Login</button></p>
            <a href="/newcomer">新規登録はこちら</a>
          </div>
        </div>
      </div>
      <Footer></Footer>
    </body>
  </html>
</template>

<script>
import Header from './header.vue'
import Footer from './footer.vue'
import Axios from 'axios'
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
      email: '',
      password: ''
    }
  },
  methods: {
    checklogin: function (event) {
      // checkloginイベント(htmlファイル内で定義している)の内容を記述
      var axios = Axios.create({
        // axiosインスタンスの作成
        baseURL: 'http://127.0.0.1:5000/',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        responseType: 'json'
      })
      var nextPage = 'pageA'

      // axiosのthenメソッドの中ではthisがvueコンポーネントを指さなくなるので別の変数に割り当てておく
      var self = this
      // バックエンドのAPIサーバにリクエストを送信
      axios.get('/login', {
        // クエリパラメータをセット
        params: {
          email: document.getElementById('email').value,
          password: document.getElementById('password').value
        }
      }).then(function (response) {
        console.log(response)
        // 応答が戻ってきたら結果を処理。
        // "success" だったら次のページにジャンプし、失敗だったらその旨表示
        if (response.data.result === 'success') {
          // JWTトークンの生成
          var token = self.generateToken(document.getElementById('email').value)
          // cookieとしてトークンを付与
          document.cookie = 'token=' + token
          // 次のページにジャンプ
          router.push({name: nextPage})
        } else {
          document.getElementById('loginResult').innerHTML = 'Login Failed !!'
        }
      })
    },
    generateToken: function (email) {
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
      var oPayload = {email: email, until: dStr}
      console.log(oHeader, oPayload)
      // JWTを生成
      var sJWT = KJUR.jws.JWS.sign('HS256', JSON.stringify(oHeader), JSON.stringify(oPayload), secretToken)
      console.log(sJWT)
      return sJWT
    }
  }
}
</script>
