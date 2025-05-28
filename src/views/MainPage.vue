<template>
  <div class="flex flex-cols h-screen">
    <div class="w-[1530px]">
      <div class="grid grid-cols-9">
        <div class="col-span-8">
          <ChannelPreview ref="channelPreviewRef" />
        </div>
        <div class="col-span-1 bg-black"></div>
      </div>
      <WorkBench />
    </div>
    <div class="w-[500px] h-full flex flex-col">
      <CubePreview />
      <SoundSpectrum />
      <Dashboard class="flex-1" />
    </div>
    <PresetDialog
      v-if="sharedVariables.dialogOpen"
      :channel-preview-ref="channelPreviewRef!"
      @close="closeDialog"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, nextTick } from 'vue'
import WorkBench from '../components/WorkBench/WorkBench.vue'
import Dashboard from '../components/Dashboard.vue'
import CubePreview from '../components/CubePreview.vue'
import ChannelPreview from '../components/ChannelPreview.vue'
import SoundSpectrum from '../components/SoundSpectrum.vue'
import PresetDialog from '../components/PresetDialog/PresetDialog.vue'
import { useSharedVariablesStore } from '../stores/sharedVariables'
import { usePresentStateStore } from '../stores/presentState'

const sharedVariables = useSharedVariablesStore()
const presentState = usePresentStateStore()

const channelPreviewRef = ref<InstanceType<typeof ChannelPreview> | null>(null)

onMounted(async() => {
  await nextTick()
  console.log('MainPage is mounted')
  presentState.initializeIPC()
  presentState.requestStateUpdate()
})

function closeDialog() {
  sharedVariables.dialogOpen = false
}
</script>
