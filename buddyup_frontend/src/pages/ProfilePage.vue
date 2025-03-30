<!-- src/pages/ProfilePage.vue -->
<template>
    <div class="p-6 bg-gray-50 min-h-screen mx-auto">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Мой профиль</h1>
            <button
                    @click="isEditing = !isEditing; if (!isEditing) updateProfile()"
                    class="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
            >
                <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                {{ isEditing ? 'Сохранить' : 'Редактировать' }}
            </button>
        </div>

        <!-- Отображение профиля -->
        <div v-if="!isEditing && profile" class="bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-500">
            <p class="text-gray-700"><span class="font-medium">ID:</span> {{ profile.id }}</p>
            <p class="text-gray-700 mt-2"><span class="font-medium">ФИО:</span> {{ profile.fio }}</p>
            <p class="text-gray-700 mt-2"><span class="font-medium">Группа:</span> {{ profile.group_number }}</p>
            <p class="text-gray-700 mt-2"><span class="font-medium">Курс:</span> {{ profile.course }}</p>
            <p class="text-gray-700 mt-2">
                <span class="font-medium">Предметы, по которым нужна помощь:</span>
                <span v-if="profile.subjects_need_help?.length">{{ profile.subjects_need_help.map(s => s.name).join(', ') }}</span>
                <span v-else>Не указаны</span>
            </p>
            <p class="text-gray-700 mt-2">
                <span class="font-medium">Предметы, по которым могу помочь:</span>
                <span v-if="profile.subjects_can_help?.length">{{ profile.subjects_can_help.map(s => s.name).join(', ') }}</span>
                <span v-else>Не указаны</span>
            </p>
            <p class="text-gray-700 mt-2">
                <span class="font-medium">Формат встречи:</span>
                {{ profile.preferred_meeting_format ? profile.preferred_meeting_format.name : 'Не указан' }}
            </p>
        </div>

        <!-- Загрузка -->
        <div v-else-if="!isEditing" class="flex flex-col items-center justify-center h-64 text-gray-500 bg-white rounded-xl shadow-md">
            <svg
                    class="h-20 w-20 mb-4 text-blue-400 animate-spin"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
            >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 12a8 8 0 018-8v8h8a8 8 0 01-16 0z" />
            </svg>
            <p class="text-xl font-semibold text-gray-700">Загрузка профиля...</p>
        </div>

        <!-- Редактирование профиля -->
        <form v-else-if="profile" @submit.prevent="updateProfile" class="space-y-6 bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-500">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">ФИО</label>
                <input
                        v-model="editForm.fio"
                        class="w-full p-2 bg-gray-100 border border-gray-300 text-gray-900 text-sm rounded-lg cursor-not-allowed"
                        disabled
                />
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Группа</label>
                <input
                        v-model="editForm.group_number"
                        class="w-full p-2 bg-gray-100 border border-gray-300 text-gray-900 text-sm rounded-lg cursor-not-allowed"
                        disabled
                />
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Курс</label>
                <input
                        v-model="editForm.course"
                        type="number"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
            </div>
            <!-- Предметы, по которым нужна помощь -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Предметы, по которым нужна помощь</label>
                <input
                        v-model="searchQueryNeed"
                        @input="searchSubjects('need')"
                        type="text"
                        placeholder="Введите минимум 3 символа..."
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <div class="mt-2 flex flex-wrap gap-2">
                    <span
                            v-for="subject in editForm.subjects_need_help"
                            :key="subject.id"
                            class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full"
                    >
                        {{ subject.name }}
                        <button
                                @click="removeSubject(subject.id, 'need')"
                                type="button"
                                class="ml-2 text-blue-600 hover:text-blue-800"
                        >
                            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </span>
                </div>
                <div v-if="searchResultsNeed.length" class="mt-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg bg-white">
                    <ul>
                        <li
                                v-for="result in searchResultsNeed"
                                :key="result.id"
                                @click="addSubject(result, 'need')"
                                class="p-2 hover:bg-gray-100 cursor-pointer"
                        >
                            {{ result.name }}
                        </li>
                    </ul>
                </div>
                <button
                        v-if="searchQueryNeed.length >= 3 && !searchResultsNeed.length"
                        @click="createNewSubject('need')"
                        type="button"
                        class="mt-2 text-sm text-blue-600 hover:text-blue-800"
                >
                    Создать новый предмет: "{{ searchQueryNeed }}"
                </button>
            </div>
            <!-- Предметы, по которым могу помочь -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Предметы, по которым могу помочь</label>
                <input
                        v-model="searchQueryCan"
                        @input="searchSubjects('can')"
                        type="text"
                        placeholder="Введите минимум 3 символа..."
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <div class="mt-2 flex flex-wrap gap-2">
                    <span
                            v-for="subject in editForm.subjects_can_help"
                            :key="subject.id"
                            class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full"
                    >
                        {{ subject.name }}
                        <button
                                @click="removeSubject(subject.id, 'can')"
                                type="button"
                                class="ml-2 text-blue-600 hover:text-blue-800"
                        >
                            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </span>
                </div>
                <div v-if="searchResultsCan.length" class="mt-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg bg-white">
                    <ul>
                        <li
                                v-for="result in searchResultsCan"
                                :key="result.id"
                                @click="addSubject(result, 'can')"
                                class="p-2 hover:bg-gray-100 cursor-pointer"
                        >
                            {{ result.name }}
                        </li>
                    </ul>
                </div>
                <button
                        v-if="searchQueryCan.length >= 3 && !searchResultsCan.length"
                        @click="createNewSubject('can')"
                        type="button"
                        class="mt-2 text-sm text-blue-600 hover:text-blue-800"
                >
                    Создать новый предмет: "{{ searchQueryCan }}"
                </button>
            </div>
            <!-- Формат встречи -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Формат встречи</label>
                <input
                        v-model="searchQueryFormat"
                        @input="searchMeetingFormats"
                        type="text"
                        placeholder="Введите минимум 3 символа..."
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <div class="mt-2 flex flex-wrap gap-2">
                    <span
                            v-if="editForm.preferred_meeting_format"
                            class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full"
                    >
                        {{ editForm.preferred_meeting_format.name }}
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
                <div v-if="searchResultsFormat.length" class="mt-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg bg-white">
                    <ul>
                        <li
                                v-for="result in searchResultsFormat"
                                :key="result.id"
                                @click="addMeetingFormat(result)"
                                class="p-2 hover:bg-gray-100 cursor-pointer"
                        >
                            {{ result.name }}
                        </li>
                    </ul>
                </div>
                <button
                        v-if="searchQueryFormat.length >= 3 && !searchResultsFormat.length"
                        @click="createNewMeetingFormat"
                        type="button"
                        class="mt-2 text-sm text-blue-600 hover:text-blue-800"
                >
                    Создать новый формат встречи: "{{ searchQueryFormat }}"
                </button>
            </div>
        </form>

        <!-- Мои запросы -->
        <h2 class="text-2xl font-bold text-gray-800 mt-8 mb-6">Мои запросы</h2>
        <div v-if="myRequests.length" class="grid grid-cols-1 gap-6">
            <router-link
                    v-for="req in myRequests"
                    :key="req.id"
                    :to="{ name: 'RequestDetail', params: { id: req.id } }"
                    class="block bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 border-l-4 border-blue-500"
            >
                <h3 class="text-xl font-bold text-gray-900">{{ req.subject }}</h3>
            </router-link>
        </div>
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
            <p class="text-xl font-semibold text-gray-700">У вас пока нет запросов</p>
        </div>
    </div>
</template>

<script>
    import api from '@/services/api';

    export default {
        name: 'ProfilePage',
        data() {
            return {
                profile: null,
                myRequests: [],
                isEditing: false,
                editForm: {
                    subjects_need_help: [],
                    subjects_can_help: [],
                    preferred_meeting_format: null,
                },
                searchQueryNeed: '',
                searchResultsNeed: [],
                searchQueryCan: '',
                searchResultsCan: [],
                searchQueryFormat: '',
                searchResultsFormat: [],
                allMeetingFormats: [], // Храним все форматы встреч для локальной фильтрации
            };
        },
        async mounted() {
            await this.fetchProfile();
            await this.fetchMyRequests();
            await this.fetchMeetingFormats(); // Загружаем форматы встреч при монтировании
        },
        methods: {
            async fetchProfile() {
                try {
                    const response = await api.get('/users/search-by-uid');
                    this.profile = response.data.data || {};
                    this.editForm = {
                        fio: this.profile.fio || '',
                        group_number: this.profile.group_number || '',
                        course: this.profile.course || '',
                        subjects_need_help: this.profile.subjects_need_help || [],
                        subjects_can_help: this.profile.subjects_can_help || [],
                        preferred_meeting_format: this.profile.preferred_meeting_format || null,
                    };
                } catch (error) {
                    console.error('Ошибка загрузки профиля:', error);
                    this.profile = {};
                }
            },
            async fetchMyRequests() {
                try {
                    const response = await api.get('/requests/my');
                    this.myRequests = response.data || [];
                } catch (error) {
                    console.error('Ошибка загрузки моих запросов:', error);
                    this.myRequests = [];
                }
            },
            async fetchMeetingFormats() {
                try {
                    const response = await api.get('/meeting-format/');
                    this.allMeetingFormats = response.data.data || [];
                } catch (error) {
                    console.error('Ошибка загрузки форматов встреч:', error);
                    this.allMeetingFormats = [];
                }
            },
            async searchSubjects(type) {
                const query = type === 'need' ? this.searchQueryNeed : this.searchQueryCan;
                const results = type === 'need' ? 'searchResultsNeed' : 'searchResultsCan';
                const selected = type === 'need' ? this.editForm.subjects_need_help : this.editForm.subjects_can_help;

                if (query.length < 3) {
                    this[results] = [];
                    return;
                }
                try {
                    const response = await api.get('/subject/search/', { params: { query_str: query } });
                    this[results] = response.data.data.filter(s => !selected.some(sub => sub.id === s.id));
                } catch (error) {
                    console.error('Ошибка поиска предметов:', error);
                    this[results] = [];
                }
            },
            addSubject(subject, type) {
                const selected = type === 'need' ? 'subjects_need_help' : 'subjects_can_help';
                this.editForm[selected].push(subject);
                if (type === 'need') {
                    this.searchQueryNeed = '';
                    this.searchResultsNeed = [];
                } else {
                    this.searchQueryCan = '';
                    this.searchResultsCan = [];
                }
            },
            removeSubject(id, type) {
                const selected = type === 'need' ? 'subjects_need_help' : 'subjects_can_help';
                this.editForm[selected] = this.editForm[selected].filter(s => s.id !== id);
            },
            async createNewSubject(type) {
                const query = type === 'need' ? this.searchQueryNeed : this.searchQueryCan;
                try {
                    const response = await api.post('/subject/', { name: query });
                    const newSubject = response.data.data;
                    if (newSubject && newSubject.id && newSubject.name) {
                        this.addSubject(newSubject, type);
                    } else {
                        console.error('Новый предмет не содержит id или name:', newSubject);
                    }
                } catch (error) {
                    console.error('Ошибка создания предмета:', error);
                }
            },
            async searchMeetingFormats() {
                if (this.searchQueryFormat.length < 3) {
                    this.searchResultsFormat = [];
                    return;
                }
                try {
                    const response = await api.get('/meeting-format/', { params: { query: this.searchQueryFormat } });
                    const queryLower = this.searchQueryFormat.toLowerCase();
                    this.searchResultsFormat = response.data.data
                        .filter(f => f.name.toLowerCase().includes(queryLower)) // Фильтруем по совпадению текста
                        .filter(f => !this.editForm.preferred_meeting_format || f.id !== this.editForm.preferred_meeting_format.id); // Исключаем уже выбранный
                } catch (error) {
                    console.error('Ошибка поиска форматов встреч:', error);
                    this.searchResultsFormat = [];
                }
            },
            addMeetingFormat(format) {
                this.editForm.preferred_meeting_format = format;
                this.searchQueryFormat = '';
                this.searchResultsFormat = [];
            },
            removeMeetingFormat() {
                this.editForm.preferred_meeting_format = null;
            },
            async createNewMeetingFormat() {
                const newFormatName = this.searchQueryFormat;
                if (!newFormatName) {
                    console.error('Название формата встречи не может быть пустым');
                    return;
                }
                try {
                    const response = await api.post('/meeting-format/', { name: newFormatName });
                    const newFormat = response.data.data; // Предполагаем, что API возвращает объект { id, name }
                    if (newFormat && newFormat.id && newFormat.name) {
                        this.allMeetingFormats.push(newFormat); // Добавляем в список всех форматов
                        this.addMeetingFormat(newFormat); // Устанавливаем как выбранный
                    } else {
                        console.error('Новый формат встречи не содержит id или name:', newFormat);
                    }
                } catch (error) {
                    console.error('Ошибка создания формата встречи:', error);
                }
            },
            async updateProfile() {
                const updateData = {
                    uid: this.profile.uid,
                    fio: this.editForm.fio,
                    group_number: this.editForm.group_number,
                    course: String(this.editForm.course), // Приведение к строке
                    subjects_need_help: this.editForm.subjects_need_help.map(s => s.id),
                    subjects_can_help: this.editForm.subjects_can_help.map(s => s.id),
                    preferred_meeting_format_id: this.editForm.preferred_meeting_format ? this.editForm.preferred_meeting_format.id : null,
                };
                try {
                    await api.put('/users/profile', updateData);
                    await this.fetchProfile();
                    this.isEditing = false;
                } catch (error) {
                    console.error('Ошибка обновления профиля:', error);
                }
            }
        },
    };
</script>
<style scoped>
    .bg-gray-50 {
        background: linear-gradient(to bottom, #f9fafb, #f1f5f9);
    }
</style>