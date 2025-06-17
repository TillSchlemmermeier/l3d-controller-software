<template>
  <div :class="'simple-keyboard'"></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import Keyboard from 'simple-keyboard'
import 'simple-keyboard/build/css/index.css'

const props = defineProps({
  input: {
    type: String,
  },
})

const emit = defineEmits(['onChange', 'onKeyPress', 'save'])
const minimumLayout = {
  default: [
    '1 2 3 4 5 6 7 8 9 0 {bksp}',
    'q w e r t z u i o p',
    'a s d f g h j k l {enter}',
    'y x c v b n m - _',
  ],
  // shift: [
  //   '1 2 3 4 5 6 7 8 9 0 _ {bksp}',
  //   'Q W E R T Y U I O P',
  //   'A S D F G H J K L {enter}',
  //   'Z X C V B N M ; :',
  //   '{space}'
  // ]
}

const keyboard = ref<Keyboard | null>(null)

const onChange = (input: string) => {
  emit('onChange', input)
}

const onKeyPress = (button: string) => {
  emit('onKeyPress', button)

  if (button === '{shift}' || button === '{lock}') handleShift()
  if (button === '{enter}') save()
}

const handleShift = () => {
  if (keyboard.value) {
    const currentLayout = keyboard.value.options.layoutName
    const shiftToggle = currentLayout === 'default' ? 'shift' : 'default'

    keyboard.value.setOptions({
      layoutName: shiftToggle,
    })
  }
}

function save() {
  emit('save')
}

onMounted(() => {
  keyboard.value = new Keyboard('simple-keyboard', {
    onChange,
    onKeyPress,
    layout: minimumLayout,
  })
})

watch(
  () => props.input,
  (input) => {
    if (keyboard.value) {
      keyboard.value.setInput(input || '')
    }
  },
)
</script>

<style>

.simple-keyboard.hg-theme-default {
  background: oklch(0.705 0.015 286.067);
}

.simple-keyboard.hg-theme-default .hg-row {
  margin-bottom: 0.5rem;
}

.simple-keyboard.hg-theme-default .hg-button {
  height: 70px !important;
  font-size: 1.5rem !important;
  margin: 0.25rem;
  border-radius: 0.5rem;
  background: rgb(63 63 70) !important;
  color: rgb(244 244 245) !important;
}

.simple-keyboard.hg-theme-default .hg-button:active {
  background: rgb(82 82 91) !important;
  border-width: 0.25rem;
  border-color: rgb(244 244 245) 
}

.simple-keyboard.hg-theme-default .hg-button.hg-standardBtn {
  height: 70px !important;
}

.simple-keyboard.hg-theme-default .hg-button-enter {
  height: 157px !important;
  position: absolute;
  left: 2024px;
  top: 331px;
  width: 190px !important;
}

.simple-keyboard.hg-theme-default .hg-button.hg-button-bksp,
.simple-keyboard.hg-theme-default .hg-button.hg-button-enter
{
  background: rgb(82 82 91) !important;
}

.simple-keyboard.hg-theme-default .hg-row:nth-child(4) {
  padding-right: 210px; /* Enter key width + margin */
}.simple-keyboard.hg-theme-default .hg-row:nth-child(3) {
  padding-right: 210px; /* Enter key width + margin */
}
</style>
