<template>
  <template v-if="loading">
    <div>Loading...</div>
  </template>
  <template v-else>
    <div class="grid grid-cols-9 mt-2 ml-1 select-none">
      <div class="col-span-8">
        <div class="flex">
          <draggable
            v-model="presentState.channels"
            item-key="channel"
            :group="{ 
              name: 'channel',
              pull: 'clone',
              put: true,
              revertClone: true
            }"
            :delay="50"
            :delayOnTouchOnly="false"
            @start="startColumnDrag"
            @end="endColumnDrag"
            :animation="300"
            class="flex gap-2"
          >
            <template #item="{ index }">
              <div class="flex flex-col gap-2 w-[162px]">
                <div>
                  <ChannelParameters
                    :channel="index"
                    @click="toggleDialog('channel', index)"
                    :isSelected="isSelected(index, 10)"
                  />
                </div>
                <div class="relative">
                  <GeneratorComponent
                    :channel="index"
                    :isSelected="isSelected(index, 9)"
                    :context="whichContext(index, 9)"
                    @click="handleClick(index, 9)"
                    @dblclick="handleDoubleClick(index, 9)"
                  />
                </div>
              </div>
            </template>
          </draggable>
          <template v-if="presentState.channels.length < 8">
            <div class="w-40 mt-2">
              <draggable
                :v-model="newChannel"
                item-key="newchannel"
                class="h-[75px] m-3 border-2 border-dashed border-zinc-500 rounded-lg"
                :group="{ 
                  name: 'channel-copy',
                  put: true, 
                  pull: false,
                  revertClone: true
                }"
                @add="copyChannel"
                :data-name="'newChannel'"
                @click="toggleDialog('newChannel', presentState.channels.length)"
              >
                <template #item>
                </template>
              </draggable>

            </div>
          </template>
        </div>

        <div class="flex gap-2 mt-2">
          <template v-for="(_, channelIndex) in presentState.channels" :key="channelIndex">
            <div class="flex flex-col gap-2">
              <draggable
                v-model="presentState.channels[channelIndex].effects"
                item-key="effect"
                :id="channelIndex"
                @start="startEffectDrag(channelIndex)"
                @end="endEffectDrag($event, channelIndex)"
                :group="{ name: 'effects', pull: 'clone', revertClone: true }"
                :delay="50"
                :animation="300"
                class="w-[162px]"
              >
                <template #item="{ index }">
                  <div class="">
                    <EffectComponent
                      :channel="channelIndex"
                      :effectNumber="index"
                      :isSelected="isSelected(channelIndex, index)"
                      :context="whichContext(channelIndex, index)"
                      @dblclick="handleDoubleClick(channelIndex, index)"
                      @click="handleClick(channelIndex, index)"
                    />
                  </div>
                </template>
              </draggable>
              <template v-if="presentState.channels[channelIndex].effects.length < 6">
                <div
                  class="flex items-center justify-center h-[75px] m-3 border-2 border-dashed border-zinc-500 rounded-lg text-4xl text-zinc-500"
                  @click="
                    newEffect(channelIndex, presentState.channels[channelIndex].effects.length)
                  "
                >
                  +
                </div>
              </template>
            </div>
          </template>
        </div>
      </div>
      <div class="col-span-1 flex flex-col pr-2">
        <CubeParameters 
          @click="toggleDialog('global', 9)"
        />
        <draggable
          v-model="presentState.globalEffects"
          item-key="effect"
          id=9
          @start="startEffectDrag(9)"
          @end="endEffectDrag($event, 9)"
          :group="{ name: 'effects', pull: 'clone', revertClone: true }"
          :animation="300"
          :delay="50"
          class=""
        >
          <template #item="{ index }">
            <div>
              <EffectComponent
                :channel="9"
                :effectNumber="index"
                :isSelected="isSelected(9, index)"
                :context="whichContext(9, index)"
                @click="handleClick(9, index)"
                @dblclick="handleDoubleClick(9, index)"
              />
            </div>
          </template>
        </draggable>
        <div
          class="flex items-center justify-center h-[75px] m-3 border-2 border-dashed border-zinc-500 rounded-lg text-4xl text-zinc-500"
          @click="
            newEffect(9, presentState.globalEffects.length)
          "
        >
          +
        </div>
        <TrashZone />
      </div>
    </div>
    <div class="absolute bottom-4 left-20 flex flex-row text-white gap-4">
        <div
          @click="sharedVariables.contextIndex = 0"
          class="p-12 rounded bg-red-500"
          :class="[
            sharedVariables.contextIndex == 0 ? 'border-3 border-white' : '',
          ]"
        />
        <div
          @click="sharedVariables.contextIndex = 1"
          class="p-12 rounded bg-green-500"
          :class="[
            sharedVariables.contextIndex == 1 ? 'border-3 border-white' : '',
          ]"
        />
        <div
          @click="sharedVariables.contextIndex = 2"
          class="p-12 rounded bg-orange-500"
          :class="[
            sharedVariables.contextIndex == 2 ? 'border-3 border-white' : '',
          ]"
        />
        <div
          @click="sharedVariables.contextIndex = 3"
          class="p-12 rounded bg-blue-500"
          :class="[
            sharedVariables.contextIndex == 3 ? 'border-3 border-white' : '',
          ]"
        />
      </div>
  </template>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import draggable from 'vuedraggable'
import { usePresentStateStore } from '../../stores/presentState'
import { useSharedVariablesStore } from '../../stores/sharedVariables'
import GeneratorComponent from './GeneratorComponent.vue'
import EffectComponent from './EffectComponent.vue'
import ChannelParameters from './ChannelParameters.vue'
import CubeParameters from './CubeParameters.vue'
import TrashZone from './TrashZone.vue'

const presentState = usePresentStateStore()
const sharedVariables = useSharedVariablesStore()
const loading = ref(true)
const oldIndex = ref(0)
const newIndex = ref(0)
const newChannel = ref([])

onMounted(async () => {
  loading.value = true
  
  loading.value = false
})

// send data through socket.io
const lastClickTime = ref(0)
function handleClick(index: number, element_id: number) {
  if (sharedVariables.clickBehavior == 'select') {
    selectParameters(index, element_id)
  } else if (sharedVariables.clickBehavior == 'edit') {
    selectParameters(index, element_id)
    if (element_id == 9) {
      newGenerator(index)
    } else {
      newEffect(index, element_id)
    }
  } else if (sharedVariables.clickBehavior == 'IO') {
    const now = Date.now()
    if (now - lastClickTime.value < 300) return  // Debounce, otherwise somehow executed twice
    lastClickTime.value = now
    presentState.toggleEffect(index, element_id)
  }
}

function handleDoubleClick(index: number, element_id: number) {
  if (sharedVariables.clickBehavior == 'select') {
    if (element_id == 9) {
      newGenerator(index)
    } else {
      newEffect(index, element_id)
    }
  } 
  else if (sharedVariables.clickBehavior == 'edit') {
    selectParameters(index, element_id)
  } else {
    {}
  }
}

// open the selection dialog for generators, effects or presets
function toggleDialog(type: string, channelIndex: number, effectIndex?: number) {
  sharedVariables.dialogType = type
  sharedVariables.channelIndex = channelIndex
  if (effectIndex !== undefined && effectIndex !== null) {
    sharedVariables.effectIndex = effectIndex
  }
  sharedVariables.dialogOpen = !sharedVariables.dialogOpen
}

// open the dialog to add a new effect to a channel
function newEffect(channelIndex: number, effectIndex: number) {
  sharedVariables.dialogType = 'effect'
  sharedVariables.channelIndex = channelIndex
  sharedVariables.effectIndex = effectIndex
  sharedVariables.dialogOpen = true
}

// open the dialog to add a new generator to a channel
function newGenerator(channelIndex: number) {
  sharedVariables.dialogType = 'generator'
  sharedVariables.channelIndex = channelIndex
  sharedVariables.effectIndex = 9
  sharedVariables.dialogOpen = true
}

// select an effect or generator to change its parameters with the MIDI Controller
function selectParameters(channelIndex: number, index: number) {
  const contextIndex = sharedVariables.contextIndex
  if (index !== undefined && index !== null) {
    presentState.select(contextIndex, channelIndex, index)
  } else {
    // if a generator is selected, we give it the index 9
    presentState.select(contextIndex, channelIndex, 9)
  }
}

// check if an effect or generator is selected
function isSelected(channelIndex: number, effectIndex: number) {
  console.log(presentState.context[0][0], presentState.context[0][1])
  return (
    presentState.context[0][0] === channelIndex && presentState.context[0][1] === effectIndex
  )
}

function whichContext(channelIndex: number, effectIndex: number) {
  if (presentState.context[0][0] === channelIndex && presentState.context[0][1] === effectIndex) {
    return 0
  } else if (presentState.context[1][0] === channelIndex && presentState.context[1][1] === effectIndex) {
    return 1
  } else if (presentState.context[2][0] === channelIndex && presentState.context[2][1] === effectIndex) {
    return 2
  } else if (presentState.context[3][0] === channelIndex && presentState.context[3][1] === effectIndex) {
    return 3
  } else {
    return 4
  }
}

// copy a channel
function copyChannel() {
  presentState.copyChannel(oldIndex.value)
}

// start dragging a column
function startColumnDrag(event: { oldIndex: number }) {
  oldIndex.value = event.oldIndex
  sharedVariables.lastTypeDragged = 'channel'
}

// end dragging a column
function endColumnDrag(event: {
  to: any, newIndex: number 
}) {
  // check if the column is dropped in the trash zone of copied to a new channel
  if (event.to.dataset.name == 'trashZone' || event.to.dataset.name == 'newChannel') {
    return
  }
  newIndex.value = event.newIndex
  sharedVariables.lastTypeDragged = 'channel'
  if (oldIndex.value !== newIndex.value) {
    presentState.moveChannel(oldIndex.value, newIndex.value)
  }
}

// start dragging an effect
function startEffectDrag(channelIndex: number) {
  sharedVariables.draggedChannelIndex = channelIndex
  sharedVariables.lastTypeDragged = 'effect'
  sharedVariables.isDragging = true
}

// start dragging an effect
function endEffectDrag(event: { to: any, oldIndex: number; newIndex: number }, channelIndex: number) {
  // Skip processing if dropped in trash zone
  sharedVariables.isDragging = false
  if (event.to.dataset.name === 'trashZone') {
    return
  }

  if (!event.to || !event.to.attributes || !event.to.attributes.id) {
    console.log('Invalid drop target')
    return
  }
  const newChannelIndex = Number(event.to.attributes.id.nodeValue)
  console.log(newChannelIndex, sharedVariables.draggedChannelIndex)
  
  if (newChannelIndex !== sharedVariables.draggedChannelIndex) {
    presentState.copyEffect(
      sharedVariables.draggedChannelIndex,
      event.oldIndex,
      newChannelIndex,
      event.newIndex,
    )
  } else {
    presentState.moveEffect(channelIndex, event.oldIndex, event.newIndex)
  }
}
</script>

<style>
  .sortable-chosen {
    transform: scale(1.1);
    opacity: 0.9;
    z-index: 50;
    cursor: grabbing;
  }

  .sortable-ghost {
    opacity: 0.5;
    transform: scale(1) !important;
  }
</style>
