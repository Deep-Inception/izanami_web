<template>
  <div>
    <ul v-for='place_data in data' :key="place_data.place">
      レース会場 {{ place_data.place }}
      <div class='flex'>
          <raceListItem v-for="race in place_data.races" :key="race.race_number" v-bind:race="race">
          </raceListItem>
      </div>
    </ul>
  </div>
</template>

<script>
import raceListItem from './raceListItem.vue'
const data = [{place: '01', races: [{race_number: '01R', deadline: '12:34', place: '01'}, {race_number: '02R', deadline: '23:45', place: '01'}]}, {place: '02', races: [{ race_number: '01R', deadline: '22:34', place: '02' }, {race_number: '02R', deadline: '22:45', place: '02'}]}]

export default {
  components: { raceListItem },
  data: function () {
    return { data: data }
  }
}
</script>
