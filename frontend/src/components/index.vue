<template>
    <div>
      <Header></Header>
      <div class="top-wrapper">
        <div class="lg:w-3/4 w-full mx-auto overflow-auto">
          <h1 class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900">カレンダー</h1>
          <p>こちらの日付から当日のレース情報に遷移できます。</p>
          <Calendar :attributes="attrs" is-expanded @dayclick="onDayClick"></Calendar>
        </div>
      </div>
      <Footer></Footer>
    </div>
</template>

<script>
import Header from './header.vue'
import Footer from './footer.vue'
import Calendar from 'v-calendar/lib/components/calendar.umd'
export default {
  components: {Header, Footer, Calendar},
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
