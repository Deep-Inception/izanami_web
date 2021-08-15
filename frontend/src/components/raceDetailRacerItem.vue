<template>
  <tr>
    <td class="border-t-2 border-gray-200 px-4 py-3">{{ racer.couse }}</td>
    <td class="border-t-2 border-gray-200 px-4 py-3">{{ racer.racer.racer_id }}</td>
    <td class="border-t-2 border-gray-200 px-4 py-3">{{ racer.racer.name }} ( {{ racer.racer.age }}歳 / {{ racer.racer.weight }}kg )</td>
    <td class="border-t-2 border-gray-200 px-4 py-3">{{ racer.racer.rank }}</td>
    <td class="border-t-2 border-gray-200 px-4 py-3">{{ racer.racer.win_rate }} ({{ racer.racer.win_rate_place }})</td>
    <td class="border-t-2 border-gray-200 px-4 py-3">{{ racer.racer.exacta_rate }}  ({{ racer.racer.exacta_rate_place }})</td>
    <td class="border-t-2 border-gray-200 px-4 py-3">{{ racer.racer.exhibition_time }}</td>
    <td class="border-t-2 border-gray-200 px-4 py-3">{{ racer.racer.tilt }}</td>
    <td class="border-t-2 border-gray-200 px-4 py-3">{{ racer.racer.prize }}</td>
  </tr>
</template>

<script>
export default {
  name: 'raceDetailRacerItem',
  props: ['racer']
}
</script>
