<script setup>
</script>

<template>
  <div class="watcher"></div>
</template>

<style scoped>
.watcher {
  height: 2.5px;
  background-color: color-mix(in hsl, var(--bs-primary) 75%, transparent 25%);
  width: 100%;
  position: absolute;
  bottom: 0px;
  z-index: 999;
  transform-origin: left;
  scale: 0 1;
  animation: scroll-watcher ease-in-out;
  animation-timeline: scroll();
}

@keyframes scroll-watcher {
  to {
    scale: 1 1;
  }
}
</style>