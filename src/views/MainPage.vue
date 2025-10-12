<template>
  <div class="flex flex-cols h-screen">
    <div class="w-[1560px]">
      <div class="grid grid-cols-9 bg-black pl-6">
        <div class="col-span-8">
          <ChannelPreview ref="channelPreviewRef" />
        </div>
        <div
          class="col-span-1"
          @dblclick="uiState.admin = !uiState.admin"
        ></div>
      </div>
      <WorkBench />
    </div>
    <div class="w-[500px] h-full flex flex-col">
      <CubePreview />
      <SoundSpectrum />
      <Dashboard class="flex-1" />
    </div>
    <SideBar />
    <PresetDialog
      v-if="uiState.dialogOpen"
      :channel-preview-ref="channelPreviewRef!"
      @close="closeDialog"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, nextTick } from 'vue'
import WorkBench from '../components/WorkBench/WorkBench.vue'
import Dashboard from '../components/Dashboard/Dashboard.vue'
import CubePreview from '../components/CubePreview.vue'
import ChannelPreview from '../components/ChannelPreview.vue'
import SoundSpectrum from '../components/SoundSpectrum.vue'
import PresetDialog from '../components/PresetDialog/PresetDialog.vue'
import SideBar from '../components/SideBar/SideBar.vue'
import { useUiStateStore } from '../stores/uiState'
import { useCoreStateStore } from '../stores/coreState'

const uiState = useUiStateStore()
const coreState = useCoreStateStore()

const channelPreviewRef = ref<InstanceType<typeof ChannelPreview> | null>(null)

onMounted(async() => {
  await nextTick()
  console.log('MainPage is mounted')
  coreState.initializeIPC()
  coreState.requestStateUpdate()
})

function closeDialog() {
  uiState.dialogOpen = false
}
</script>
