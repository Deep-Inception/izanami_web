<template>
  <div class="flex flex-col min-h-screen">
    <Header></Header>
    <section class="text-gray-600 body-font flex-auto">
      <div class="container px-0 py-12 mx-auto">
        <div class="flex flex-col text-center w-full mb-4">
          <h1 class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900">免責事項</h1>
          <p class="lg:w-2/3 mx-auto leading-relaxed text-base">当サイトからのリンクやバナーなどで移動したサイトで提供される情報、サービス等について一切の責任を負いません。また当サイトのコンテンツ・情報について、できる限り正確な情報を提供するように努めておりますが、正確性や安全性を保証するものではありません。情報が古くなっていることもございます。当サイトに掲載された内容によって生じた損害等の一切の責任を負いかねますのでご了承ください。</p>
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
  name: 'Disclaimer',
  components: {
    Header,
    Footer
  }
}

</script>
