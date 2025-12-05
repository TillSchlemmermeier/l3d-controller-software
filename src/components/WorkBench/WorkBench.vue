<template>
  <div class="pl-6 overflow-hidden">
    <div class="grid grid-cols-9 mt-2 ml-1 select-none">
      <div class="col-span-8">
        <div class="flex">
          <draggable
            v-model="coreState.channels"
            item-key="channel"
            :group="{ 
              name: 'channel',
              pull: 'clone',
              put: true,
              revertClone: true
            }"
            :delay="50"
            :delayOnTouchOnly="true"
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
                  />
                </div>
                <div class="relative">
                  <GeneratorComponent
                    :channel="index"
                    :context="whichContext(index, 9)"
                    @click="handleClick(index, 9)"
                    @dblclick="handleDoubleClick(index, 9)"
                  />
                </div>
              </div>
            </template>
          </draggable>
          <template v-if="coreState.channels.length < 8">
            <div class="w-40">
              <draggable
                :v-model="newChannel"
                item-key="newchannel"
                class="h-[85px] mx-3 mt-1 border-2 border-dashed border-zinc-500 rounded-lg"
                :group="{ 
                  name: 'channel-copy',
                  put: true, 
                  pull: false,
                  revertClone: true
                }"
                @add="copyChannel"
                :data-name="'newChannel'"
                @click="toggleDialog('newChannel', coreState.channels.length)"
              >
                <template #item>
                </template>
              </draggable>

            </div>
          </template>
        </div>

        <div class="flex gap-2 mt-3">
          <template v-for="(channel, channelIndex) in coreState.channels":key="channelIndex">
            <div class="flex flex-col gap-2">
              <div
                class="px-2 mb-[-5px]"
                @click="uiState.channelIndex = channelIndex">
                <div
                  class="h-6 w-full rounded border relative"
                  :class="channel.color?.gradient ? 'border-zinc-500' : 'border-zinc-600 bg-zinc-700'"
                  :style="channel.color?.gradient ? { background: generateGradientCSS(channel.color.gradient) } : {}"
                  :title="channel.color?.gradient ? '' : 'No gradient set'"
                >
                  <!-- Animated ring overlay -->
                  <div
                    v-if="channelIndex === uiState.channelIndex"
                    class="absolute inset-0 ring-3 ring-white ring-offset-3 ring-offset-zinc-700 rounded pointer-events-none animate-pulse"
                  ></div>
                </div>
              </div>
              <draggable
                v-model="coreState.channels[channelIndex].effects"
                item-key="effect"
                :id="channelIndex"
                @start="startEffectDrag(channelIndex)"
                @end="endEffectDrag($event, channelIndex)"
                :group="{ name: 'effects', pull: 'clone', revertClone: true }"
                :delay="50"
                :delayOnTouchOnly="true"
                :animation="300"
                class="w-[162px] transition-all duration-200"
                :class="{ 'min-h-[65vh] pb-20 bg-zinc-900/20 rounded-lg': uiState.isDragging }"
              >
                <template #item="{ index }">
                  <div class="">
                    <EffectComponent
                      :channel="channelIndex"
                      :effectNumber="index"
                      :context="whichContext(channelIndex, index)"
                      @dblclick="handleDoubleClick(channelIndex, index)"
                      @click="handleClick(channelIndex, index)"
                    />
                  </div>
                </template>
              </draggable>
              <template v-if="coreState.channels[channelIndex].effects.length < 6">
                <div
                  class="flex items-center justify-center h-[75px] m-3 border-2 border-dashed border-zinc-500 rounded-lg text-4xl text-zinc-500"
                  @click="
                    newEffect(channelIndex, coreState.channels[channelIndex].effects.length)
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
        <div
          class="px-2 my-2"
          @click="uiState.channelIndex = 9">
          <div
            class="h-6 w-full rounded border relative"
            :class="coreState.globalColor?.gradient ? 'border-zinc-500' : 'border-zinc-600 bg-zinc-700'"
            :style="coreState.globalColor?.gradient ? { background: generateGradientCSS(coreState.globalColor.gradient) } : {}"
            :title="coreState.globalColor?.gradient ? '' : 'No gradient set'"
          >
            <!-- Animated ring overlay -->
            <div
              v-if="uiState.channelIndex === 9"
              class="absolute inset-0 ring-3 ring-white ring-offset-3 ring-offset-zinc-700 rounded pointer-events-none animate-pulse"
            ></div>
          </div>
        </div>
        <draggable
          v-model="coreState.globalEffects"
          item-key="effect"
          id=9
          @start="startEffectDrag(9)"
          @end="endEffectDrag($event, 9)"
          :group="{ name: 'effects', pull: 'clone', revertClone: true }"
          :animation="300"
          :delay="50"
          :delayOnTouchOnly="true"
          class="transition-all duration-200"
          :class="{ 'min-h-[25vh] pb-20 bg-zinc-900/20 rounded-lg': uiState.isDragging }"
        >
          <template #item="{ index }">
            <div>
              <EffectComponent
                :channel="9"
                :effectNumber="index"
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
            newEffect(9, coreState.globalEffects.length)
          "
        >
          +
        </div>
        <TrashZone @click="uiState.deleteActive = !uiState.deleteActive" />
      </div>
    </div>
    <ContextSelector />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import draggable from 'vuedraggable'
import { useCoreStateStore } from '../../stores/coreState'
import { useUiStateStore } from '../../stores/uiState'
import GeneratorComponent from './GeneratorComponent.vue'
import EffectComponent from './EffectComponent.vue'
import ChannelParameters from './ChannelParameters.vue'
import CubeParameters from './CubeParameters.vue'
import ContextSelector from './ContextSelector.vue'
import TrashZone from './TrashZone.vue'

const coreState = useCoreStateStore()
const uiState = useUiStateStore()
const oldIndex = ref(0)
const newIndex = ref(0)
const newChannel = ref([])

function handleClick(index: number, element_id: number) {
  uiState.channelIndex = index
  if(uiState.deleteActive) {
    if (element_id == 9) {
      coreState.removeChannel(index)
      uiState.channelIndex -= 1
      selectParameters(uiState.channelIndex, element_id)
    } else {
      if (index == 9) {
        coreState.removeEffect(9, element_id)
      } else {
        coreState.removeEffect(index, element_id)
      }
    }
    uiState.deleteActive = false
  } else {
    // if (coreState.shift_activated) {
    //   if (element_id == 9) {
    //     selectParameters(index, element_id)
    //   } else {
    //     coreState.toggleEffect(index, element_id)
    //   }
    // } else {
    //   selectParameters(index, element_id)
    // }
    if (uiState.clickBehavior == 'select') {
      selectParameters(index, element_id)
    } else if (uiState.clickBehavior == 'edit') {
      selectParameters(index, element_id)
      if (element_id == 9) {
        newGenerator(index)
      } else {
        newEffect(index, element_id)
      }
    } else if (uiState.clickBehavior == 'IO') {
      if (element_id == 9) {
        selectParameters(index, element_id)
      } else {
        coreState.toggleEffect(index, element_id)
      }
    }
  }
}

function handleDoubleClick(index: number, element_id: number) {
  // if (element_id == 9) {
  //   newGenerator(index)
  // } else {
  //   newEffect(index, element_id)
  // }
  if (uiState.clickBehavior == 'select') {
    if (element_id == 9) {
      newGenerator(index)
    } else {
      newEffect(index, element_id)
    }
  } 
  else if (uiState.clickBehavior == 'edit') {
    selectParameters(index, element_id)
  } else {
    {}
  }
}

// open the selection dialog for generators, effects or presets
function toggleDialog(type: string, channelIndex: number, effectIndex?: number) {
  uiState.elementType = type
  uiState.channelIndex = channelIndex
  if (effectIndex !== undefined && effectIndex !== null) {
    uiState.effectIndex = effectIndex
  }
  uiState.dialogOpen = !uiState.dialogOpen
}

// open the dialog to add a new effect to a channel
function newEffect(channelIndex: number, effectIndex: number) {
  uiState.elementType = 'effect'
  uiState.channelIndex = channelIndex
  uiState.effectIndex = effectIndex
  uiState.dialogOpen = true
}

// open the dialog to add a new generator to a channel
function newGenerator(channelIndex: number) {
  uiState.elementType = 'generator'
  uiState.channelIndex = channelIndex
  uiState.effectIndex = 9
  uiState.dialogOpen = true
}

// select an effect or generator to change its parameters with the MIDI Controller
function selectParameters(channelIndex: number, index: number) {
  const contextIndex = uiState.contextIndex
  if (index !== undefined && index !== null) {
    coreState.select(contextIndex, channelIndex, index)
  } else {
    // if a generator is selected, we give it the index 9
    coreState.select(contextIndex, channelIndex, 9)
  }
}

function whichContext(channelIndex: number, effectIndex: number) {
  if (coreState.context[0][0] === channelIndex && coreState.context[0][1] === effectIndex) {
    return 0
  } else if (coreState.context[1][0] === channelIndex && coreState.context[1][1] === effectIndex) {
    return 1
  } else if (coreState.context[2][0] === channelIndex && coreState.context[2][1] === effectIndex) {
    return 2
  } else if (coreState.context[3][0] === channelIndex && coreState.context[3][1] === effectIndex) {
    return 3
  } else {
    return 4
  }
}

// copy a channel
function copyChannel() {
  coreState.copyChannel(oldIndex.value)
}

// start dragging a column
function startColumnDrag(event: { oldIndex: number }) {
  oldIndex.value = event.oldIndex
  uiState.lastTypeDragged = 'channel'
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
  uiState.lastTypeDragged = 'channel'
  if (oldIndex.value !== newIndex.value) {
    coreState.moveChannel(oldIndex.value, newIndex.value)
  }
}

// start dragging an effect
function startEffectDrag(channelIndex: number) {
  uiState.draggedChannelIndex = channelIndex
  uiState.lastTypeDragged = 'effect'
  uiState.isDragging = true
}

// start dragging an effect
function endEffectDrag(event: { to: any, oldIndex: number; newIndex: number }, channelIndex: number) {
  // Skip processing if dropped in trash zone
  uiState.isDragging = false
  if (event.to.dataset.name === 'trashZone') {
    return
  }

  if (!event.to || !event.to.attributes || !event.to.attributes.id) {
    console.log('Invalid drop target')
    return
  }
  const newChannelIndex = Number(event.to.attributes.id.nodeValue)
  console.log(newChannelIndex, uiState.draggedChannelIndex)
  
  if (newChannelIndex !== uiState.draggedChannelIndex) {
    coreState.copyEffect(
      uiState.draggedChannelIndex,
      event.oldIndex,
      newChannelIndex,
      event.newIndex,
    )
  } else {
    coreState.moveEffect(channelIndex, event.oldIndex, event.newIndex)
  }
}

function generateGradientCSS(gradientData: Array<[number, string]>): string {
  if (!gradientData || gradientData.length === 0) {
    return 'linear-gradient(to right, #666666, #666666)' // Fallback for empty/invalid data
  }

  const stopStrings = gradientData.map(([position, color]) => `${color} ${position}%`)
  return `linear-gradient(to right, ${stopStrings.join(', ')})`
}

</script>

<style>
  .sortable-chosen {
    transform: scale(1.05);
    opacity: 0.9;
    z-index: 50;
    cursor: grabbing;
    transition: transform 0s, opacity 0s;
  }

  :not(.sortable-chosen) {
    transition: transform 0.1s 0.1s, opacity 0.1s 0.1s; /* 0.1s delay before shrinking */
  }

  .sortable-ghost {
    opacity: 0.5;
    transform: scale(1) !important;
  }
</style>
