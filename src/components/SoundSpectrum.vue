<template>
  <div 
    class="w-[500px] h-[425px] bg-black p-2 border-2" 
    :class="{ 'border-red-600': isSelected, 'border-transparent': !isSelected }"
  >
    <canvas ref="chart" @click="selectSpectrum"></canvas>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted, watch, computed } from 'vue'
import { Chart, ChartConfiguration } from 'chart.js/auto'
import { usePresentStateStore } from '../stores/presentState'

const presentState = usePresentStateStore()
const chart = ref<HTMLCanvasElement | null>(null)
let chartInstance: Chart | null = null
let freqAxis: number[] = []
  
const COLORS = ['red', 'green', 'blue', 'orange'] as const
const FONT = { size: 16, family: "'DejaVu Sans'" }

const scales = {
  x: {
    type: "logarithmic" as const,
    min: 50,
    max: 10000,
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
    label: `${i + 1}`,
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

const config: ChartConfiguration = {
    type: 'line',
    data: {
      labels: freqAxis,
      datasets: [
      createSpectrumDataset(),
      ...createSelectorDatasets(),
      ...createThresholdDatasets()
    ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 0 },
      scales,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: 'white',
            font: FONT,
            filter: (legendItem) => {
            // Only show selector lines (datasets 1-4) in legend
            return (legendItem.datasetIndex ?? -1) > 0 && (legendItem.datasetIndex ?? -1) < 5;
          },
            usePointStyle: false,
            padding: 20,
            boxWidth: 40,
            boxHeight: 0
          }
        },
      }
    }
  }

function updateSpectrum(newData: number[]) {
  if (!chartInstance) return
  chartInstance.data.datasets[0].data = newData
  chartInstance.update('none')
}

function updateSelectorsAndThresholds() {
  const selectors = presentState.s2l_values.map((value: number) => (value ** 2) * 10000)
  const thresholds = presentState.s2l_thresholds

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
  presentState.select(10, 0)
}

const isSelected = computed(() => {
  const [section, index] = presentState.context
  return section === 10 && index === 0
})

onMounted(() => {
  if (!chart.value) return
  const ctx = chart.value.getContext('2d')
  if (!ctx) return

  // Create frequency axis
  freqAxis = Array.from({ length: 60 }, (_, i) => 
    Math.pow(10, i * (5 / 60))
  )
  config.data.labels = freqAxis


  Chart.register(chartAreaBorder)
  chartInstance = new Chart(ctx, config)
  updateSelectorsAndThresholds()

  window.ipcRenderer.onSpectrumData((message: any) => {
    updateSpectrum(message)
  })
})

watch(() => [
  presentState.s2l_values,
  presentState.s2l_thresholds
], () => {
  updateSelectorsAndThresholds()
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
  window.ipcRenderer?.removeWebSocketListener()
})
</script>

<style scoped></style>