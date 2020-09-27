<template>
      <div class='w-20 text-center p-0 m-4 bg-gray-200 text-sm max-w-sm'>
        <p class='border-b border-gray-800 p-1'>{{ race.race_number }}</p>
        <p class='p-1'>{{ race.deadline }}</p>
      </div>
</template>

<script>
export default {
  name: 'raceListItem',
  props: ['race']
}
</script>

<style>

</style>
