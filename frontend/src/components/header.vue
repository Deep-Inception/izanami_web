<template>
  <header class="text-gray-600 body-font bg-blue-500">
    <div class="container mx-auto flex flex-wrap p-2 flex-col md:flex-row items-center">
      <nav class="flex lg:w-2/5 flex-wrap items-center text-base md:ml-auto">
        <router-link :to="{path: 'races', query: {date: date}}" class="mr-10 text-white hover:text-gray-200">Home</router-link>
        <a href="/statistics" class="mr-10 text-white hover:text-gray-200">過去予想結果</a>
        <a href="/index" class="mr-10 text-white hover:text-gray-200">カレンダー</a>
      </nav>
      <div class="flex order-first lg:order-none lg:w-1/5 title-font font-medium items-center text-gray-900 lg:items-center lg:justify-center mb-4 md:mb-0">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-10 h-10 text-white p-2 bg-indigo-500 rounded-full" viewBox="0 0 24 24">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
        </svg>
        <span class="ml-3 text-xl text-white">Izanami</span>
      </div>
      <div class="lg:w-2/5 inline-flex lg:justify-end ml-5 lg:ml-0">
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: ['loginScreen'],
  data: function () {
    return {
      date: this.getToday()
    }
  },
  methods: {
    getToday: function () {
      var dt = new Date()
      var y = dt.getFullYear()
      var m = ('00' + (dt.getMonth() + 1)).slice(-2)
      var d = ('00' + dt.getDate()).slice(-2)
      var result = y + m + d
      return result
    }
  }
}
</script>
