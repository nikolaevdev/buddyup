<template>
  <div class="min-h-screen pb-16">
    <!-- Основная область для динамического контента -->
    <router-view />
    <!-- Нижнее меню -->
    <BottomNav />
  </div>
</template>

<script>
import BottomNav from "@/components/BottomNav.vue";

export default {
  name: "AppLayout",
  components: {
    BottomNav,
  },
}
</script>

<style scoped>
/* Дополнительные стили, если требуется */
</style>