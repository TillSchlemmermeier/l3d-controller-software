<template>
  <div
    class="p-1"
    :style="isSelected
      ? 'background: radial-gradient(circle, red 80%, black 100%)'
      : 'background: black'"
  >
      <div
        class="w-[492px] h-[425px] bg-black p-2 border-2 flex flex-col"
        @click="selectSpectrum"
      >
        <!-- the sequencer and the selector legend, centred together above the chart. -->
        <div class="shrink-0 flex justify-center items-center gap-5 pb-1 text-white" :style="{ font: `${FONT.size}px ${FONT.family}` }">
          <!-- one step per beat, like a sequencer. Red in the groove, grey in a break -->
          <div class="flex gap-1">
            <div v-for="i in 4" :key="i" class="w-3 h-3 rounded-sm" :style="stepStyle(i - 1)"></div>
          </div>
          <!-- the selector legend -->
          <div v-for="(color, i) in COLORS" :key="color" class="flex items-center gap-2">
            <div class="w-10 h-[5px]" :style="{ background: color }"></div>{{ i }}
          </div>
        </div>
        <div class="relative flex-1 min-h-0">
          <canvas ref="chart"></canvas>
        </div>
      </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted, watch, computed } from 'vue'
import { Chart, ChartConfiguration } from 'chart.js/auto'
import { useCoreStateStore } from '../stores/coreState'

const coreState = useCoreStateStore()
const chart = ref<HTMLCanvasElement | null>(null)
let chartInstance: Chart | null = null
let freqAxis: number[] = []
let disposeSpectrum: (() => void) | null = null
  
const beatOn = ref(false)
const grooveOn = ref(false)
const step = ref(0)
let lastTrigger: number | null = null

function stepStyle(i: number) {
  const color = grooveOn.value ? '#ff7171' : '#8a8a8a'
  if (i !== step.value) return `background:${color}; opacity:0.35`
  return beatOn.value
    ? `background:${color}; box-shadow:0 0 12px 2px ${color}; transition:none`
    : `background:${color}; transition:box-shadow 70ms`
}

const COLORS = ['red', 'green', 'blue', 'orange'] as const
const FONT = { size: 16, family: "'DejaVu Sans'" }

const scales = {
  x: {
    type: "logarithmic" as const,
    min: 30,
    max: 16000,
    grid: {
      color: 'rgba(255, 255, 255, 0.1)'
    },
    ticks: {
      callback: function (tickValue: string | number) {
        const values = [50, 100, 200, 500, 1000, 2000, 5000, 10000]
        return values.includes(Number(tickValue)) ? tickValue : null
      },
      color: 'white',
      autoSkip: false,
      maxRotation: 0,
      font: FONT
    }
  },
  y: {
    min: -0.1,
    max: 2,
    grid: {
      color: 'rgba(255, 255, 255, 0.1)'
    },
    ticks: {
      color: 'white',
      callback: function (tickValue: string | number) {
        const values = [0, 0.5, 1, 1.5, 2]
        return values.includes(Number(tickValue)) ? tickValue : null
      },
      font: FONT
    }
  }
}

function createSpectrumDataset() {
  return {
    label: 'Spectrum',
    data: Array(60).fill(0),
    borderColor: 'white',
    borderWidth: 3,
    tension: 0.1,
    pointRadius: 0,
    order: 3
  }
}

function createSelectorDatasets() {
  return COLORS.map((color, i) => ({
    label: `${i}`,
    data: [],
    borderColor: color,
    borderWidth: 5,
    pointRadius: 0,
    order: 2,
  }))
}

function createThresholdDatasets() {
  return COLORS.map((color, i) => ({
    label: `Threshold ${i + 1}`,
    data: [],
    borderColor: color,
    borderWidth: 6,
    pointRadius: 0,
    order: 1,
  }))
}

// the level a beat needs in the kick band, drawn across 40-110 Hz.
// BeatDetector.LEVEL_GATE in s2l_engine.py
const BEAT_GATE = 0.5

function createBeatGateDataset() {
  return {
    label: 'Beat gate',
    data: [{ x: 40, y: BEAT_GATE }, { x: 110, y: BEAT_GATE }],
    borderColor: '#ff7171',
    borderWidth: 3,
    borderDash: [6, 4],
    pointRadius: 0,
    order: 0,
  }
}

const config: ChartConfiguration = {
    type: 'line',
    data: {
      labels: freqAxis,
      datasets: [
      createSpectrumDataset(),
      ...createSelectorDatasets(),
      ...createThresholdDatasets(),
      createBeatGateDataset()
    ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 0 },
      scales,
      plugins: {
        // drawn in the template instead, next to the sequencer
        legend: { display: false },
      }
    }
  }

function updateSpectrum(newData: number[]) {
  if (!chartInstance) return
  chartInstance.data.datasets[0].data = newData
  chartInstance.update('none')
}

function updateSelectorsAndThresholds() {
  const selectors = coreState.s2l_values.map((value: number) => (value ** 2) * 10000)
  const thresholds = coreState.s2l_thresholds

  selectors.forEach((freq: number, i: number) => {
    updateSelectorLine(freq, i)
    updateThresholdLine(freq, thresholds[i], i)
  })

  chartInstance?.update('none')
}

function updateSelectorLine(freq: number, index: number) {
  chartInstance!.data.datasets[index + 1].data = [
    { x: freq, y: -0.1 },
    { x: freq, y: 2 }
  ]
}

function updateThresholdLine(freq: number, threshold: number, index: number) {
  chartInstance!.data.datasets[index + 5].data = [
    { x: freq * 0.86, y: threshold },
    { x: freq * 1.14, y: threshold }
  ]
}

const chartAreaBorder = {
  id: 'chartAreaBorder',
  beforeDraw(chart: Chart) {
    const { ctx, chartArea: { left, top, width, height } } = chart;
    ctx.save();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 1;
    ctx.strokeRect(left, top, width, height);
    ctx.restore();
  }
};

function selectSpectrum() {
  coreState.select(0, 'panel', 's2l')
}

const isSelected = computed(() => {
  const [section, index] = coreState.context[0]
  return section === 'panel' && index === 's2l'
})

onMounted(() => {
  if (!chart.value) return
  const ctx = chart.value.getContext('2d')
  if (!ctx) return

  // Create frequency axis: same as freq_axis in s2l_engine.py: 60 bins from 30 Hz to 16 kHz
  freqAxis = Array.from({ length: 60 }, (_, i) =>
    30 * Math.pow(16000 / 30, i / 59)
  )
  config.data.labels = freqAxis


  Chart.register(chartAreaBorder)
  chartInstance = new Chart(ctx, config)
  updateSelectorsAndThresholds()

  disposeSpectrum = window.ipcRenderer.onSpectrumData((message: any) => {
    beatOn.value = lastTrigger !== null && message.trigger !== lastTrigger
    lastTrigger = message.trigger
    grooveOn.value = message.groove
    step.value = message.trigger % 4
    updateSpectrum(message.spectrum)
  })
})

watch(() => [
  coreState.s2l_values,
  coreState.s2l_thresholds
], () => {
  updateSelectorsAndThresholds()
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
  disposeSpectrum?.()
})
</script>

<style scoped></style>