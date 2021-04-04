<template>
      <div class='w-20 text-center p-0 m-4 text-sm max-w-sm'>
        <p class='p-1 bg-blue-700 rounded-t-sm text-white'>{{ race.race_number }}R</p>
        <p class='p-1 bg-blue-500 rounded-b-sm text-white'>{{ race.deadline }}</p>
      </div>
</template>

<script>
export default {
  name: 'raceListItem',
  props: ['race']
}
</script>
