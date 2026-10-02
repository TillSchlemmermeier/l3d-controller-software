<template>
  <div>
    <div
      @click="handleRotateCube"
      ref="scatterplot"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue'
import * as THREE from 'three'
import { createCircleTexture, createCubePoints } from './cubePoints'

const scatterplot = ref<HTMLDivElement | null>(null)
const rotateCube = ref(false)
let rotatingPoints: THREE.Points | null = null
let frameId = 0
let teardown: (() => void) | null = null
let colorAttribute: THREE.BufferAttribute | null = null
let needsRender = true
let disposeCubeData: (() => void) | null = null

function setupScene() {
  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000)
  camera.position.set(7, 14.5, 11.5) 
  camera.up.set(-1, 0, 0) 
  camera.lookAt(-1, 0, 0)
  
  const renderer = new THREE.WebGLRenderer()
  renderer.setSize(500, 500)

  return { scene, camera, renderer }
}

// Share texture across all renderers to save memory
const circleTexture = createCircleTexture()

function handleCubeData(data: any) {
  // data arrives as raw uint8 RGB bytes (Buffer); view them directly
  const bytes = new Uint8Array(data.buffer, data.byteOffset, data.byteLength)

  if (colorAttribute) {
    // copy the first 3000 bytes (1000 LEDs x RGB) into the existing buffer.
    ;(colorAttribute.array as Uint8Array).set(bytes.subarray(0, 3000))
    colorAttribute.needsUpdate = true
    needsRender = true
  }
}

function handleRotateCube() {
  rotateCube.value = !rotateCube.value
  if (rotatingPoints) {
    rotatingPoints.rotation.y = 0
    rotatingPoints.rotation.z = 0
  }
  needsRender = true
}

onMounted(() => {
  if (!window.ipcRenderer) {
    console.error('Electron API not available')
    return
  }

  disposeCubeData = window.ipcRenderer.onCubeData(handleCubeData)

  const { scene, camera, renderer } = setupScene()

  if (scatterplot.value) {
    scatterplot.value.appendChild(renderer.domElement)
  }

  const { points, colorAttr, geometry, material } = createCubePoints(circleTexture, {
    size: 0.8,
    opacity: 0.9,
    depthWrite: true
  })
  colorAttribute = colorAttr
  rotatingPoints = points
  scene.add(points)

  // everything that holds GPU memory or keeps the loop alive, released on unmount
  teardown = () => {
    cancelAnimationFrame(frameId)
    geometry.dispose()
    material.dispose()
    circleTexture.dispose()
    renderer.dispose()
    renderer.forceContextLoss()
  }

  // Animation loop: render only when something changed (new data or rotation)
  const animate = () => {
    frameId = requestAnimationFrame(animate)
    if (rotateCube.value) {
      points.rotation.y += 0.01
      points.rotation.z += 0.005
      needsRender = true
    }
    if (needsRender) {
      renderer.render(scene, camera)
      needsRender = false
    }
  }
  animate()

})

onUnmounted(() => {
  disposeCubeData?.()
  teardown?.()
})
</script>

<style scoped>
</style>
