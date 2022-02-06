<template>
    <div class="flex flex-col min-h-screen">
      <Header></Header>
      <div class="lg:flex xl:flex">
        <div class="top-wrapper flex-auto lg:w-4/5 xl:w-4/5">
          <div class="lg:w-4/5 w-full mx-auto overflow-auto px-5">
            <h1 class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900">カレンダー</h1>
            <p>こちらの日付から当日のレース情報に遷移できます。</p>
            <Calendar :attributes="attrs" is-expanded @dayclick="onDayClick"></Calendar>
          </div>
        </div>
        <SideBar id="sidebar" class="lg:mt-16 xl:mt-16 lg:w-1/5 xl:w-1/5 m-0 p-5 w-full lg:static h-auto overflow-visible"/>
      </div>
      <Footer></Footer>
    </div>
</template>

<script>
import Header from './header.vue'
import Footer from './footer.vue'
import SideBar from './sidebar.vue'
import Calendar from 'v-calendar/lib/components/calendar.umd'
export default {
  components: {Header, Footer, Calendar, SideBar},
  methods: {
    onDayClick: function (date) {
      let month = '0' + date.month
      let day = '0' + date.day
      let url = '/races?date=' + date.year + month.substr(-2, 2) + day.substr(-2, 2)
      window.location.href = url
    }
  },
  data: function () {
    return {
      attrs: [
        {
          key: 'today',
          highlight: 'red',
          dates: new Date()
        }
      ]
    }
  }
}
</script>
