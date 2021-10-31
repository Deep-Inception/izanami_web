<template>
  <div class="flex flex-col min-h-screen">
    <Header></Header>
    <section class="text-gray-600 body-font flex-auto">
      <div class="container px-0 py-12 mx-auto">
        <div class="flex flex-col text-center w-full mb-4">
          <h1 class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900">プライバシーポリシー</h1>
          <h2 class="sm:text-2xl text-xl font-medium title-font mb-4 text-gray-700">個人情報の利用目的</h2>
          <p class="lg:w-2/3 mx-auto leading-relaxed text-base">当サイトでは、お問い合わせや記事へのコメントの際、名前やメールアドレス等の個人情報を入力いただく場合がございます。取得した個人情報は、お問い合わせに対する回答や必要な情報を電子メールなどをでご連絡する場合に利用させていただくものであり、これらの目的以外では利用いたしません。</p>
          <h2 class="sm:text-2xl text-xl font-medium title-font m-4 text-gray-700">広告について</h2>
          <p class="lg:w-2/3 mx-auto leading-relaxed text-base">
          当サイトでは、第三者配信の広告サービス（Googleアドセンス）を利用しており、ユーザーの興味に応じた商品やサービスの広告を表示するため、クッキー（Cookie）を使用しております。
          クッキーを使用することで当サイトはお客様のコンピュータを識別できるようになりますが、お客様個人を特定できるものではありません。
          Cookieを無効にする方法やGoogleアドセンスに関する詳細は「
          <a href="https://policies.google.com/technologies/ads?gl=jp" target="_blank" rel="noreferrer noopener" aria-label="広告 - ポリシーと規約 - Google (新しいタブで開く)">広告 – ポリシーと規約 – Google</a>
          」をご確認ください。</p>
          <h2 class="sm:text-2xl text-xl font-medium title-font m-4 text-gray-700">アクセス解析ツールについて</h2>
          <p class="lg:w-2/3 mx-auto leading-relaxed text-base">当サイトでは、Googleによるアクセス解析ツール「Googleアナリティクス」を利用しています。このGoogleアナリティクスはトラフィックデータの収集のためにクッキー（Cookie）を使用しております。トラフィックデータは匿名で収集されており、個人を特定するものではありません。</p>
        </div>
      </div>
    </section>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from './header.vue'
import Footer from './footer.vue'
export default {
  name: 'privacyPolicy',
  components: {
    Header,
    Footer
  }
}

</script>
