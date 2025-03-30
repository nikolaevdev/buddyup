<!-- src/pages/RequestsPage.vue -->
<template>
    <div class="p-6 bg-gray-50 min-h-screen mx-auto pb-16">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Запросы</h1>
            <router-link
                    to="/requests/new"
                    class="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
            >
                <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Новый запрос
            </router-link>
        </div>

        <!-- Поиск и фильтры -->
        <div class="mb-6 space-y-4">
            <!-- Поиск по теме -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Поиск по теме</label>
                <input
                        v-model="searchQuery"
                        @input="fetchRequests"
                        type="text"
                        placeholder="Введите тему для поиска..."
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
            </div>

            <!-- Фильтр по формату встречи -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Формат встречи</label>
                <input
                        v-model="formatSearchQuery"
                        @input="searchMeetingFormats"
                        type="text"
                        placeholder="Введите минимум 3 символа..."
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <div class="mt-2 flex flex-wrap gap-2">
          <span
                  v-if="filters.meeting_format"
                  class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full"
          >
            {{ filters.meeting_format.name }}
            <button
                    @click="removeMeetingFormat"
                    type="button"
                    class="ml-2 text-blue-600 hover:text-blue-800"
            >
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </span>
                </div>
                <div v-if="formatSearchResults.length" class="mt-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg bg-white">
                    <ul>
                        <li
                                v-for="result in formatSearchResults"
                                :key="result.id"
                                @click="addMeetingFormat(result)"
                                class="p-2 hover:bg-gray-100 cursor-pointer"
                        >
                            {{ result.name }}
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Фильтр по курсу -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Курс</label>
                <input
                        v-model="filters.course"
                        @input="applyFilters"
                        type="number"
                        min="1"
                        max="6"
                        placeholder="Введите номер курса"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
            </div>

            <!-- Фильтр по типу обучения -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Тип обучения</label>
                <select
                        v-model="filters.study_type"
                        @change="applyFilters"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                    <option value="">Все типы</option>
                    <option value="Бакалавриат">Бакалавриат</option>
                    <option value="Магистратура">Магистратура</option>
                    <option value="Аспирантура">Аспирантура</option>
                </select>
            </div>

            <!-- Фильтр по предметам -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Предметы</label>
                <input
                        v-model="subjectSearchQuery"
                        @input="searchSubjects"
                        type="text"
                        placeholder="Введите минимум 3 символа..."
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <div class="mt-2 flex flex-wrap gap-2">
          <span
                  v-for="subject in filters.subjects"
                  :key="subject.id"
                  class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full"
          >
            {{ subject.name }}
            <button
                    @click="removeSubject(subject.id)"
                    type="button"
                    class="ml-2 text-blue-600 hover:text-blue-800"
            >
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </span>
                </div>
                <div v-if="subjectSearchResults.length" class="mt-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg bg-white">
                    <ul>
                        <li
                                v-for="result in subjectSearchResults"
                                :key="result.id"
                                @click="addSubject(result)"
                                class="p-2 hover:bg-gray-100 cursor-pointer"
                        >
                            {{ result.name }}
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Кнопка сброса фильтров -->
            <div>
                <button
                        @click="resetFilters"
                        class="w-full px-4 py-2 bg-gray-200 text-gray-700 text-sm font-semibold rounded-lg shadow-md hover:bg-gray-300 transition-colors duration-200"
                >
                    Сбросить фильтры
                </button>
            </div>
        </div>

        <!-- Список запросов -->
        <div v-if="requests.length > 0" class="grid grid-cols-1 gap-6">
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
                        {{ request.location || 'Не указано' }}
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

        <!-- Если запросов нет -->
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
            <p class="text-xl font-semibold text-gray-700">Запросов не найдено</p>
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
        name: 'RequestsPage',
        data() {
            return {
                requests: [],
                searchQuery: '',
                filters: {
                    course: '',
                    study_type: '',
                    subjects: [],
                    meeting_format: null,
                },
                subjectSearchQuery: '',
                subjectSearchResults: [],
                formatSearchQuery: '',
                formatSearchResults: [],
                // Заглушка для обязательных параметров (в реальном приложении брать из контекста)
                userParams: {
                    fio: 'Николаев Михаил',
                    gn: '24401',
                    uid: '1',
                },
            };
        },
        async mounted() {
            await this.fetchRequests();
        },
        methods: {
            async fetchRequests() {
                try {
                    const params = {
                        subject: this.searchQuery || undefined,
                        meeting_format_id: this.filters.meeting_format ? this.filters.meeting_format.id : undefined,
                        fio: this.userParams.fio,
                        gn: this.userParams.gn,
                        uid: this.userParams.uid,
                    };
                    const response = await api.get('/requests', { params });
                    this.requests = response.data.data || [];
                } catch (error) {
                    console.error('Ошибка загрузки запросов:', error);
                    if (error.response && error.response.data && error.response.data.detail) {
                        console.error('Детали ошибки:', error.response.data.detail);
                    }
                    this.requests = [];
                }
            },
            async applyFilters() {
                try {
                    const params = {
                        course: this.filters.course ? Number(this.filters.course) : undefined,
                        study_type: this.filters.study_type || undefined,
                        subjects: this.filters.subjects.length > 0 ? this.filters.subjects.map(s => s.id) : undefined,
                        fio: this.userParams.fio,
                        gn: this.userParams.gn,
                        uid: this.userParams.uid,
                    };
                    const response = await api.get('/requests/filter', { params });
                    this.requests = response.data.data || [];
                } catch (error) {
                    console.error('Ошибка фильтрации запросов:', error);
                    if (error.response && error.response.data && error.response.data.detail) {
                        console.error('Детали ошибки:', error.response.data.detail);
                    }
                    this.requests = [];
                }
            },
            async searchSubjects() {
                if (this.subjectSearchQuery.length < 3) {
                    this.subjectSearchResults = [];
                    return;
                }
                try {
                    const response = await api.get('/subject/search/', {
                        params: {
                            query_str: this.subjectSearchQuery,
                            fio: this.userParams.fio,
                            gn: this.userParams.gn,
                            uid: this.userParams.uid,
                        },
                    });
                    this.subjectSearchResults = response.data.data.filter(
                        s => !this.filters.subjects.some(sub => sub.id === s.id)
                    );
                } catch (error) {
                    console.error('Ошибка поиска предметов:', error);
                    if (error.response && error.response.data && error.response.data.detail) {
                        console.error('Детали ошибки:', error.response.data.detail);
                    }
                    this.subjectSearchResults = [];
                }
            },
            addSubject(subject) {
                this.filters.subjects.push(subject);
                this.subjectSearchQuery = '';
                this.subjectSearchResults = [];
                this.applyFilters();
            },
            removeSubject(id) {
                this.filters.subjects = this.filters.subjects.filter(s => s.id !== id);
                this.applyFilters();
            },
            async searchMeetingFormats() {
                if (this.formatSearchQuery.length < 3) {
                    this.formatSearchResults = [];
                    return;
                }
                try {
                    const response = await api.get('/meeting-format/', {
                        params: {
                            query: this.formatSearchQuery,
                            fio: this.userParams.fio,
                            gn: this.userParams.gn,
                            uid: this.userParams.uid,
                        },
                    });
                    this.formatSearchResults = response.data.data.filter(
                        f => !this.filters.meeting_format || f.id !== this.filters.meeting_format.id
                    );
                } catch (error) {
                    console.error('Ошибка поиска форматов встреч:', error);
                    if (error.response && error.response.data && error.response.data.detail) {
                        console.error('Детали ошибки:', error.response.data.detail);
                    }
                    this.formatSearchResults = [];
                }
            },
            addMeetingFormat(format) {
                this.filters.meeting_format = format;
                this.formatSearchQuery = '';
                this.formatSearchResults = [];
                this.fetchRequests();
            },
            removeMeetingFormat() {
                this.filters.meeting_format = null;
                this.fetchRequests();
            },
            resetFilters() {
                this.searchQuery = '';
                this.filters = {
                    course: '',
                    study_type: '',
                    subjects: [],
                    meeting_format: null,
                };
                this.subjectSearchQuery = '';
                this.subjectSearchResults = [];
                this.formatSearchQuery = '';
                this.formatSearchResults = [];
                this.fetchRequests();
            },
            formatTime(time) {
                const date = new Date(time);
                return date.toLocaleString('ru-RU', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
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