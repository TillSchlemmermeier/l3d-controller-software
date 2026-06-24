<template>
  <div
    class="p-1"
    :style="isSelected
      ? 'background: radial-gradient(circle, red 80%, black 100%)'
      : 'background: black'"
  >
    <div 
      class="bg-black p-6 flex flex-col border-2 h-full"
      @click="selectDashboard"
    >
      <div class="flex flex-row flex-wrap mb-4 gap-4">
        <DashboardButton
          label="NORM S2L"
          :onClick="coreState.normalize"
        />
        <DashboardButton
        label="REBOOT CORE"
        :adminOnly="true"
        :onClick="coreState.rebootCore"
        />

        <!-- <DashboardButton
          label="REBOOT UI"
          :onClick="reloadUI"
        /> -->

        <DashboardButton
          label="UNDO RANDOM"
          :onClick="coreState.undoRandom"
        />

        <DashboardButton
          label="I/O CUBE"
          :adminOnly="true"
          :onClick="coreState.toggleCube"
          :active="coreState.IO"
        />
      </div>

      <RandomMode />

      <div class="mt-auto">
        <OneShots />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useCoreStateStore } from '../../stores/coreState'
import DashboardButton from './DashboardButton.vue'
import OneShots from './OneShots.vue'
import RandomMode from './RandomMode.vue'

const coreState = useCoreStateStore()

const isSelected = computed(() => {
  const [section, index] = coreState.context[0]
  return section === 10 && index === 1
})

function selectDashboard() {
  coreState.select(0, 10, 1)
}

function reloadUI() {
  window.location.reload()
}
</script>