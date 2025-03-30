<!-- src/pages/NewRequestPage.vue -->
<template>
    <div class="p-6 bg-gray-50 min-h-screen  mx-auto">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Создать запрос</h1>
            <router-link
                    to="/"
                    class="inline-flex items-center px-4 py-2 bg-gray-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-gray-700 transition-colors duration-200"
            >
                <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
                Назад
            </router-link>
        </div>

        <form @submit.prevent="submitRequest" class="space-y-6 bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-500">
            <!-- Тема -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Тема</label>
                <input
                        v-model="form.subject"
                        type="text"
                        placeholder="Введите тему запроса"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        required
                />
            </div>

            <!-- Описание задачи -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Описание задачи</label>
                <textarea
                        v-model="form.task_description"
                        placeholder="Опишите задачу"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        rows="4"
                        required
                ></textarea>
            </div>

            <!-- Предметы -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Предметы</label>
                <input
                        v-model="searchSubjectQuery"
                        @input="searchSubjects"
                        type="text"
                        placeholder="Введите минимум 3 символа..."
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <div class="mt-2 flex flex-wrap gap-2">
          <span
                  v-for="subject in form.subjects"
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
                <button
                        v-if="searchSubjectQuery.length >= 3 && !subjectSearchResults.length"
                        @click="createNewSubject"
                        type="button"
                        class="mt-2 text-sm text-blue-600 hover:text-blue-800"
                >
                    Создать новый предмет: "{{ searchSubjectQuery }}"
                </button>
            </div>

            <!-- Формат встречи -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Формат встречи</label>
                <input
                        v-model="searchFormatQuery"
                        @input="searchMeetingFormats"
                        type="text"
                        placeholder="Введите минимум 3 символа..."
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <div class="mt-2 flex flex-wrap gap-2">
          <span
                  v-if="form.meeting_format"
                  class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full"
          >
            {{ form.meeting_format.name }}
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
                <button
                        v-if="searchFormatQuery.length >= 3 && !formatSearchResults.length"
                        @click="createNewMeetingFormat"
                        type="button"
                        class="mt-2 text-sm text-blue-600 hover:text-blue-800"
                >
                    Создать новый формат: "{{ searchFormatQuery }}"
                </button>
            </div>

            <!-- Предпочитаемое время -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Предпочитаемое время</label>
                <input
                        v-model="form.preferred_time"
                        type="datetime-local"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        required
                />
            </div>

            <!-- Локация -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Локация</label>
                <input
                        v-model="form.location"
                        type="text"
                        placeholder="Введите место встречи"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
            </div>

            <!-- Дополнительные заметки -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Дополнительные заметки</label>
                <textarea
                        v-model="form.additional_notes"
                        placeholder="Дополнительная информация"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        rows="3"
                ></textarea>
            </div>

            <!-- Курс -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Курс</label>
                <input
                        v-model="form.course"
                        type="number"
                        min="1"
                        placeholder="Введите номер курса"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
            </div>

            <!-- Тип обучения -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Тип обучения</label>
                <select
                        v-model="form.study_type"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                    <option value="" disabled>Выберите тип обучения</option>
                    <option value="Бакалавриат">Бакалавриат</option>
                    <option value="Магистратура">Магистратура</option>
                    <option value="Аспирантура">Аспирантура</option>
                </select>
            </div>

            <!-- Кнопка отправки -->
            <button
                    type="submit"
                    class="w-full px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
            >
                Создать запрос
            </button>
        </form>
    </div>
</template>

<script>
    import api from '@/services/api';

    export default {
        name: 'NewRequestPage',
        data() {
            return {
                form: {
                    subject: '',
                    task_description: '',
                    meeting_format: null,
                    preferred_time: '',
                    location: '',
                    additional_notes: '',
                    course: null,
                    study_type: '',
                    subjects: [],
                },
                searchSubjectQuery: '',
                subjectSearchResults: [],
                searchFormatQuery: '',
                formatSearchResults: [],
            };
        },
        methods: {
            async searchSubjects() {
                if (this.searchSubjectQuery.length < 3) {
                    this.subjectSearchResults = [];
                    return;
                }
                try {
                    const response = await api.get('/subject/search/', { params: { query_str: this.searchSubjectQuery } });
                    this.subjectSearchResults = response.data.data.filter(
                        s => !this.form.subjects.some(sub => sub.id === s.id)
                    );
                } catch (error) {
                    console.error('Ошибка поиска предметов:', error);
                    this.subjectSearchResults = [];
                }
            },
            addSubject(subject) {
                this.form.subjects.push(subject);
                this.searchSubjectQuery = '';
                this.subjectSearchResults = [];
            },
            removeSubject(id) {
                this.form.subjects = this.form.subjects.filter(s => s.id !== id);
            },
            async createNewSubject() {
                try {
                    const response = await api.post('/subject/', { name: this.searchSubjectQuery });
                    const newSubject = response.data.data;
                    if (newSubject && newSubject.id && newSubject.name) {
                        this.addSubject(newSubject);
                    } else {
                        console.error('Новый предмет не содержит id или name:', newSubject);
                    }
                } catch (error) {
                    console.error('Ошибка создания предмета:', error);
                }
            },
            async searchMeetingFormats() {
                if (this.searchFormatQuery.length < 3) {
                    this.formatSearchResults = [];
                    return;
                }
                try {
                    const response = await api.get('/meeting-format/', { params: { query: this.searchFormatQuery } });
                    this.formatSearchResults = response.data.data.filter(
                        f => !this.form.meeting_format || f.id !== this.form.meeting_format.id
                    );
                } catch (error) {
                    console.error('Ошибка поиска форматов встреч:', error);
                    this.formatSearchResults = [];
                }
            },
            addMeetingFormat(format) {
                this.form.meeting_format = format;
                this.searchFormatQuery = '';
                this.formatSearchResults = [];
            },
            removeMeetingFormat() {
                this.form.meeting_format = null;
            },
            async createNewMeetingFormat() {
                try {
                    const response = await api.post('/meeting-format/', { name: this.searchFormatQuery });
                    const newFormat = response.data.data;
                    if (newFormat && newFormat.id && newFormat.name) {
                        this.addMeetingFormat(newFormat);
                    } else {
                        console.error('Новый формат не содержит id или name:', newFormat);
                    }
                } catch (error) {
                    console.error('Ошибка создания формата встречи:', error);
                }
            },
            async submitRequest() {
                const requestData = {
                    subject: this.form.subject,
                    task_description: this.form.task_description,
                    meeting_format_id: this.form.meeting_format ? this.form.meeting_format.id : null,
                    preferred_time: this.form.preferred_time ? new Date(this.form.preferred_time).toISOString() : null,
                    location: this.form.location || null,
                    additional_notes: this.form.additional_notes || null,
                    course: this.form.course ? Number(this.form.course) : null,
                    study_type: this.form.study_type || null,
                    subjects: this.form.subjects.map(s => s.id),
                };
                try {
                    const response = await api.post('/requests/', requestData);
                    const newRequestId = response.data.data.id;
                    this.$router.push(`/requests/${newRequestId}`);
                } catch (error) {
                    console.error('Ошибка создания запроса:', error);
                }
            },
        },
    };
</script>

<style scoped>
    .bg-gray-50 {
        background: linear-gradient(to bottom, #f9fafb, #f1f5f9);
    }
</style>