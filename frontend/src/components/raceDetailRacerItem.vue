<template>
  <tr class='w-20 text-center p-0 m-4 bg-gray-200 text-sm max-w-sm'>
    <td class='border-b border-gray-800 p-1'>{{ racer.couse }}</td>
    <td class='border-b border-gray-800 p-1'>{{ racer.racer.name }}</td>
    <td class='p-1'>{{ racer.racer.age }}</td>
  </tr>
</template>

<script>
export default {
  name: 'raceDetailRacerItem',
  props: ['racer']
}
</script>
