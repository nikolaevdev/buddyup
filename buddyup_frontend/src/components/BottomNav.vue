<template>
  <nav class="fixed bottom-0 left-0 w-full bg-white shadow-lg border-t border-gray-200">
    <ul class="flex justify-around items-center py-1">
      <li>
        <router-link
          to="/"
          class="flex flex-col items-center p-2 text-gray-700 hover:text-blue-600 transition-colors duration-200"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M3 12l9-9 9 9M4 10v10h16V10"
            />
          </svg>
          <span class="text-xs font-medium mt-1">Главная</span>
        </router-link>
      </li>
      <li>
        <router-link
          to="/requests"
          class="flex flex-col items-center p-2 text-gray-700 hover:text-blue-600 transition-colors duration-200"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
          <span class="text-xs font-medium mt-1">Запросы</span>
        </router-link>
      </li>
      <li>
        <router-link
          to="/profile"
          class="flex flex-col items-center p-2 text-gray-700 hover:text-blue-600 transition-colors duration-200"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5.121 17.804A8 8 0 0112 15a8 8 0 016.879 2.804M15 11a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          <span class="text-xs font-medium mt-1">Мой профиль</span>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "BottomNav",
}
</script>

<style scoped>
/* Дополнительные стили можно добавить здесь, если нужно что-то специфическое */
</style>
