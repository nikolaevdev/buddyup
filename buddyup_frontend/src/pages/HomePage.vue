<template>
  <div class="p-6 bg-gray-50 min-h-screen mx-auto">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Добро пожаловать в BuddyUp!</h1>
      <router-link
        to="/requests/new"
        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
      >
        <svg
          class="h-5 w-5 mr-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Новый запрос
      </router-link>
    </div>
    <p class="text-gray-700 mb-8">Здесь вы можете найти учебных напарников, создавать запросы и просматривать свои активные задачи.</p>

    <h2 class="text-2xl font-bold text-gray-800 mb-6">Ваши актуальные запросы</h2>

    <!-- Проверка наличия данных -->
    <div v-if="requests && requests.length > 0" class="grid grid-cols-1 gap-6">
      <!-- Карточка запроса -->
      <router-link
        v-for="request in requests"
        :key="request.id"
        :to="{ name: 'RequestDetail', params: { id: request.id } }"
        class="block bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 border-l-4 border-blue-500"
      >
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-bold text-gray-900">{{ request.subject }}</h3>
          <span
            class="inline-flex items-center px-3 py-1 text-sm font-semibold rounded-full"
            :class="request.is_confirmed ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
          >
            <svg
              v-if="request.is_confirmed"
              class="h-4 w-4 mr-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            {{ request.is_confirmed ? "Подтверждено" : "Ожидает" }}
          </span>
        </div>
        <p class="text-gray-600 mt-2">{{ request.task_description }}</p>
        <div class="mt-4 space-y-2 text-sm text-gray-700">
          <p class="flex items-center">
            <svg class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 10h16m-8-3V4M7 7V4m10 3V4M5 20h14a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1Zm3-7h.01v.01H8V13Zm4 0h.01v.01H12V13Zm4 0h.01v.01H16V13Zm-8 4h.01v.01H8V17Zm4 0h.01v.01H12V17Zm4 0h.01v.01H16V17Z"/>
            </svg>
            {{ formatTime(request.preferred_time) }}
          </p>
          <p class="flex items-center">
            <svg class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15a6 6 0 1 0 0-12 6 6 0 0 0 0 12Zm0 0v6M9.5 9A2.5 2.5 0 0 1 12 6.5"/>
            </svg>
            {{ request.location }}
          </p>
          <p class="flex items-center">
            <svg class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7.556 8.5h8m-8 3.5H12m7.111-7H4.89a.896.896 0 0 0-.629.256.868.868 0 0 0-.26.619v9.25c0 .232.094.455.26.619A.896.896 0 0 0 4.89 16H9l3 4 3-4h4.111a.896.896 0 0 0 .629-.256.868.868 0 0 0 .26-.619v-9.25a.868.868 0 0 0-.26-.619.896.896 0 0 0-.63-.256Z"/>
            </svg>
            {{ request.meeting_format_info.name }}
          </p>
          <p class="flex items-center">
            <svg class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            {{ request.course }}, {{ request.study_type }}
          </p>
        </div>
      </router-link>
    </div>

    <!-- Если данных нет -->
    <div v-else class="flex flex-col items-center justify-center h-64 text-gray-500 bg-white rounded-xl shadow-md">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-20 w-20 mb-4 text-blue-400"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
        />
      </svg>
      <p class="text-xl font-semibold text-gray-700">У вас пока нет активных запросов</p>
      <router-link
        to="/requests/new"
        class="mt-4 inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
      >
        Создать запрос
      </router-link>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: "HomePage",
  data() {
    return {
      requests: { data: [] },
    };
  },
  async mounted() {
    try {
      const response = await api.get('/requests/my');
      if (response.data && Array.isArray(response.data) && response.data.length > 0) {
        this.requests = response.data;
      } else {
        this.requests = { data: [] };
      }
    } catch (error) {
      console.error("Ошибка загрузки запросов", error);
      this.requests = { data: [] };
    }
  },
  methods: {
    formatTime(time) {
      const date = new Date(time);
      return date.toLocaleString("ru-RU", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
};
</script>

<style scoped>
.bg-gray-50 {
  background: linear-gradient(to bottom, #f9fafb, #f1f5f9);
}
</style>