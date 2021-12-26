<template>
  <header class="text-gray-600 body-font bg-blue-500">
    <div class="container mx-auto flex flex-wrap p-2 flex-col md:flex-row items-center text-white">
      <nav class="flex lg:w-2/5 flex-wrap items-center text-base md:ml-auto">
        <a href="/races" class="mr-5 hover:text-gray-200">Home</a>
        <a href="/statistics" class="mr-5 hover:text-gray-200">過去予想結果</a>
        <a href="/index" class="hover:text-gray-200">カレンダー</a>
      </nav>
      <a class="flex order-first lg:order-none lg:w-1/5 title-font font-medium items-center text-gray-900 lg:items-center lg:justify-center mb-4 md:mb-0">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-10 h-10 text-white p-2 bg-indigo-500 rounded-full" viewBox="0 0 24 24">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
        </svg>
        <span class="ml-3 text-xl text-white">Izanami</span>
      </a>
      <div class="lg:w-2/5 inline-flex lg:justify-end ml-5 lg:ml-0">
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header'
}
</script>
