<!-- src/pages/RequestDetailPage.vue -->
<template>
    <div class="p-6 bg-gray-50 min-h-screen mx-auto pb-16">
        <!-- Заголовок и кнопка "Назад" -->
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">Запрос #{{ requestId }}</h1>
            <router-link
                    to="/requests"
                    class="inline-flex items-center px-4 py-2 bg-gray-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-gray-700 transition-colors duration-200"
            >
                <svg class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
                Назад
            </router-link>
        </div>

        <!-- Информация о запросе -->
        <div v-if="request" class="bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-500 mb-6">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-2xl font-bold text-gray-900">{{ request.subject }}</h2>
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

            <p class="text-gray-600 mb-4">{{ request.task_description }}</p>

            <div class="space-y-2 text-sm text-gray-700">
                <p class="flex items-center">
                    <svg class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 10h16m-8-3V4M7 7V4m10 3V4M5 20h14a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1Zm3-7h.01v.01H8V13Zm4 0h.01v.01H12V13Zm4 0h.01v.01H16V13Zm-8 4h.01v.01H8V17Zm4 0h.01v.01H12V17Zm4 0h.01v.01H16V17Z"/>
                    </svg>
                    {{ formatTime(request.preferred_time) }}
                </p>
                <p class="flex items-center">
                    <svg class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M12 15a6 6 0 1 0 0-12 6 6 0 0 0 0 12Zm0 0v6M9.5 9A2.5 2.5 0 0 1 12 6.5"
                        />
                    </svg>
                    {{ request.location || 'Не указано' }}
                </p>
                <p class="flex items-center">
                    <svg class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M7.556 8.5h8m-8 3.5H12m7.111-7H4.89a.896.896 0 0 0-.629.256.868.868 0 0 0-.26.619v9.25c0 .232.094.455.26.619A.896.896 0 0 0 4.89 16H9l3 4 3-4h4.111a.896.896 0 0 0 .629-.256.868.868 0 0 0 .26-.619v-9.25a.868.868 0 0 0-.26-.619.896.896 0 0 0-.63-.256Z"
                        />
                    </svg>
                    {{ request.meeting_format_info.name }}
                </p>
                <p class="flex items-center">
                    <svg class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                        />
                    </svg>
                    {{ request.course }}, {{ request.study_type }}
                </p>
                <p class="flex items-center">
                    <svg class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                    </svg>
                    Предметы:
                    <span v-if="!subjectsDisplay.length" class="ml-2 text-gray-500">Не указаны</span>
                    <span v-else class="ml-2 flex flex-wrap gap-2">
                        <span
                                v-for="subject in request.subjects_info"
                                :key="subject.id"
                                class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full"
                        >
                            {{ subject.name }}
                        </span>
                    </span>
                </p>
                <p v-if="request.additional_notes" class="flex items-center">
                    <svg class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                        />
                    </svg>
                    Заметки: {{ request.additional_notes }}
                </p>
            </div>

            <!-- Кнопки редактирования и удаления (только для создателя) -->
            <div v-if="isOwner" class="mt-6 flex gap-4">
                <button
                        @click="editMode = true"
                        class="flex-1 px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
                >
                    Редактировать
                </button>
                <button
                        @click="deleteRequest"
                        class="flex-1 px-4 py-2 bg-red-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-red-700 transition-colors duration-200"
                >
                    Удалить
                </button>
            </div>

            <!-- Кнопка "Предложить себя в помощь" (если пользователь не создатель) -->
            <div v-else class="mt-6">
                <button
                        @click="applyToRequest"
                        class="w-full px-4 py-2 bg-green-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-green-700 transition-colors duration-200"
                >
                    Предложить себя в помощь
                </button>
            </div>
        </div>

        <!-- Форма редактирования -->
        <div v-if="editMode" class="bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-500 mb-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">Редактировать запрос</h2>
            <form @submit.prevent="updateRequest" class="space-y-4">
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
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                          d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                            </button>
                        </span>
                    </div>
                    <div v-if="subjectSearchResults.length"
                         class="mt-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg bg-white">
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
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                          d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                            </button>
                        </span>
                    </div>
                    <div
                            v-if="formatSearchResults.length"
                            class="mt-2 max-h-40 overflow-y-auto border border-gray-200 rounded-lg bg-white"
                    >
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

                <!-- Кнопки сохранения и отмены -->
                <div class="flex gap-4">
                    <button
                            type="submit"
                            class="flex-1 px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
                    >
                        Сохранить
                    </button>
                    <button
                            @click="editMode = false"
                            type="button"
                            class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 text-sm font-semibold rounded-lg shadow-md hover:bg-gray-300 transition-colors duration-200"
                    >
                        Отмена
                    </button>
                </div>
            </form>
        </div>

        <!-- Список откликнувшихся (только для создателя) -->
        <div v-if="isOwner && applications.length > 0" class="bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-500">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">Откликнувшиеся</h2>
            <div class="space-y-4">
                <div
                        v-for="application in applications"
                        :key="application.id"
                        class="p-4 bg-gray-50 rounded-lg"
                >
                    <div class="flex items-center justify-between mb-2">
                        <div>
                            <!-- Здесь выводим ФИО из applicant_user, если оно найдено -->
                            <p class="text-gray-900 font-semibold">
                                <!-- Если пользователь не найден, отображаем запасной текст -->
                                {{ application.applicant_user
                                ? application.applicant_user.fio
                                : 'Неизвестный пользователь' }}
                            </p>
                            <p class="text-sm text-gray-600">Статус: {{ application.status }}</p>
                        </div>
                        <div class="flex gap-2">
                            <button
                                    v-if="application.status === 'pending'"
                                    @click="confirmApplication(application.id)"
                                    class="px-4 py-2 bg-green-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-green-700 transition-colors duration-200"
                            >
                                Одобрить
                            </button>
                            <button
                                    v-if="application.status === 'pending'"
                                    @click="declineApplication(application.id)"
                                    class="px-4 py-2 bg-red-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-red-700 transition-colors duration-200"
                            >
                                Отклонить
                            </button>
                            <button
                                    @click="viewFeedback(application.applicant_uid)"
                                    class="px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
                            >
                                Посмотреть отзывы
                            </button>
                        </div>
                    </div>
                    <!-- Форма отзыва (только для одобренных заявок) -->
                    <div v-if="application.status === 'confirmed'" class="mt-4">
                        <button
                                @click="openFeedbackForm(application.applicant_uid)"
                                class="w-full px-4 py-2 bg-purple-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-purple-700 transition-colors duration-200"
                        >
                            Оставить отзыв
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div v-else-if="isOwner" class="bg-white p-6 rounded-xl shadow-lg border-l-4 border-blue-500">
            <p class="text-gray-600">Пока никто не откликнулся на ваш запрос.</p>
        </div>

        <!-- Модальное окно для отзывов -->
        <div
                v-if="showFeedbackModal"
                id="feedback-modal"
                tabindex="-1"
                class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
        >
            <div class="relative w-full max-w-md p-6 bg-white rounded-xl shadow-lg">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-xl font-bold text-gray-900">Отзывы о пользователе</h3>
                    <button
                            @click="showFeedbackModal = false"
                            class="text-gray-500 hover:text-gray-700"
                    >
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <div v-if="feedbacks.length > 0" class="space-y-4 max-h-96 overflow-y-auto">
                    <div
                            v-for="feedback in feedbacks"
                            :key="feedback.id"
                            class="p-4 bg-gray-50 rounded-lg"
                    >
                        <p class="text-gray-900 font-semibold">Оценка: {{ feedback.rating }}/5</p>
                        <p class="text-gray-600">{{ feedback.comment }}</p>
                        <p class="text-sm text-gray-500">От: {{ feedback.author_fio }}</p>
                    </div>
                </div>
                <div v-else class="text-gray-600">
                    У этого пользователя пока нет отзывов.
                </div>
            </div>
        </div>

        <!-- Модальное окно для отправки отзыва -->
        <div
                v-if="showFeedbackFormModal"
                id="feedback-form-modal"
                tabindex="-1"
                class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
        >
            <div class="relative w-full max-w-md p-6 bg-white rounded-xl shadow-lg">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-xl font-bold text-gray-900">Оставить отзыв</h3>
                    <button
                            @click="showFeedbackFormModal = false"
                            class="text-gray-500 hover:text-gray-700"
                    >
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>
                <form @submit.prevent="submitFeedback" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Оценка (1-5)</label>
                        <input
                                v-model.number="feedbackForm.rating"
                                type="number"
                                min="1"
                                max="5"
                                class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                                required
                        />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Комментарий</label>
                        <textarea
                                v-model="feedbackForm.comment"
                                placeholder="Опишите ваш опыт"
                                class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                                rows="4"
                                required
                        ></textarea>
                    </div>
                    <div class="flex gap-4">
                        <button
                                type="submit"
                                class="flex-1 px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors duration-200"
                        >
                            Отправить
                        </button>
                        <button
                                @click="showFeedbackFormModal = false"
                                type="button"
                                class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 text-sm font-semibold rounded-lg shadow-md hover:bg-gray-300 transition-colors duration-200"
                        >
                            Отмена
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import api from '@/services/api';
    import { mapGetters } from 'vuex';

    export default {
        name: 'RequestDetailPage',
        data() {
            return {
                requestId: this.$route.params.id,
                request: null,
                // Для явного контроля, является ли пользователь владельцем
                isOwner: false,
                editMode: false,
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
                applications: [],
                feedbacks: [],
                showFeedbackModal: false,
                showFeedbackFormModal: false,
                feedbackForm: {
                    user_uid: '',
                    rating: 5,
                    comment: '',
                },
            };
        },
        computed: {
            ...mapGetters('auth', ['authParams']),

            // Отдельный удобный геттер для предметов
            subjectsDisplay() {
                if (!this.request || !this.request.subjects) return [];
                return this.request.subjects.map(subject => {
                    if (typeof subject === 'string') {
                        return { id: subject, name: subject };
                    }
                    return subject;
                });
            },
        },
        async mounted() {
            await this.fetchRequest();
            // Проверяем, владелец ли текущий пользователь
            if (this.request && this.authParams.uid) {
                this.isOwner = (this.request.creator_uid == this.authParams.uid);
                if (this.isOwner) {
                    await this.fetchApplications();
                }
            }
        },
        methods: {
            async fetchRequest() {
                try {
                    const response = await api.get(`/requests/${this.requestId}`);
                    this.request = response.data.data;

                    // Заполняем форму редактирования данными запроса
                    this.form = {
                        subject: this.request.subject,
                        task_description: this.request.task_description,
                        meeting_format: this.request.meeting_format_info,
                        preferred_time: new Date(this.request.preferred_time).toISOString().slice(0, 16),
                        location: this.request.location,
                        additional_notes: this.request.additional_notes,
                        course: this.request.course,
                        study_type: this.request.study_type,
                        subjects: this.request.subjects || [],
                    };
                } catch (error) {
                    console.error('Ошибка загрузки запроса:', error);
                }
            },

            // ГЛАВНЫЙ МЕТОД: загружаем заявки, потом получаем к ним ФИО через /users/search
            async fetchApplications() {
                try {
                    // Шаг 1. Получаем список заявок
                    const response = await api.get(`/requests/${this.requestId}/applications`);
                    this.applications = response.data.data || [];

                    // Шаг 2. Собираем все ID пользователей (helper_id) в уникальный массив
                    const uniqueHelperIds = [...new Set(this.applications.map(app => app.helper_id))];

                    console.log("Unique Helper IDs:", uniqueHelperIds);
                    if (!uniqueHelperIds.length) return; // Если пусто – не делаем лишний запрос

                    // Шаг 3. Формируем query-параметры для /users/search.
                    // Согласно Вашему примеру, можно передавать несколько ids вот так: ?ids=7&ids=10&...
                    const params = new URLSearchParams();
                    uniqueHelperIds.forEach(id => {
                        params.append('uids', id);
                    });

                    // Шаг 4. Делаем запрос на /users/search, чтобы получить объекты пользователей
                    const usersResponse = await api.get('/users/search', { params });
                    const usersData = usersResponse.data.data || [];

                    // Шаг 5. Строим «мапу» (словарь) userId -> userObject
                    // Предположим, что в ответе пользователь приходит в виде { id: 7, fio: "Иванов", ... }
                    const userMap = {};
                    for (const user of usersData) {
                        userMap[user.id] = user;
                    }

                    // Шаг 6. «Обогащаем» каждую заявку информацией о пользователе, у которого helper_id совпадает
                    this.applications = this.applications.map(app => {
                        return {
                            ...app,
                            helper_user: userMap[app.helper_id] || null,
                        };
                    });
                } catch (error) {
                    console.error('Ошибка загрузки заявок:', error);
                }
            },

            async searchSubjects() {
                if (this.searchSubjectQuery.length < 3) {
                    this.subjectSearchResults = [];
                    return;
                }
                try {
                    const response = await api.get('/subject/search/', {
                        params: { query_str: this.searchSubjectQuery },
                    });
                    // Фильтруем результаты, чтобы не добавлять уже выбранные
                    this.subjectSearchResults = response.data.data.filter(
                        s => !this.form.subjects.some(sub => sub.id === s.id)
                    );
                } catch (error) {
                    console.error('Ошибка поиска предметов:', error);
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

            async searchMeetingFormats() {
                if (this.searchFormatQuery.length < 3) {
                    this.formatSearchResults = [];
                    return;
                }
                try {
                    const response = await api.get('/meeting-format/', {
                        params: { query: this.searchFormatQuery },
                    });
                    this.formatSearchResults = response.data.data.filter(
                        f => !this.form.meeting_format || f.id !== this.form.meeting_format.id
                    );
                } catch (error) {
                    console.error('Ошибка поиска форматов встреч:', error);
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

            async updateRequest() {
                try {
                    const requestData = {
                        subject: this.form.subject,
                        task_description: this.form.task_description,
                        meeting_format_id: this.form.meeting_format ? this.form.meeting_format.id : null,
                        preferred_time: this.form.preferred_time
                        ? new Date(this.form.preferred_time).toISOString()
                        : null,
                        location: this.form.location || null,
                        additional_notes: this.form.additional_notes || null,
                        course: this.form.course ? Number(this.form.course) : null,
                        study_type: this.form.study_type || null,
                        subjects: this.form.subjects.map(s => s.id),
                    };
                    await api.patch(`/requests/${this.requestId}`, requestData);
                    this.editMode = false;
                    await this.fetchRequest();
                } catch (error) {
                    console.error('Ошибка обновления запроса:', error);
                }
            },

            async deleteRequest() {
                if (!confirm('Вы уверены, что хотите удалить этот запрос?')) return;
                try {
                    await api.delete(`/requests/${this.requestId}`);
                    this.$router.push('/requests');
                } catch (error) {
                    console.error('Ошибка удаления запроса:', error);
                }
            },

            async applyToRequest() {
                try {
                    const uid = this.authParams.uid;
                    await api.post(`/requests/${this.requestId}/apply`, { uid });
                    alert('Заявка успешно подана!');
                } catch (error) {
                    console.error('Ошибка подачи заявки:', error);
                }
            },

            async confirmApplication(applicationId) {
                try {
                    await api.patch(`/requests/${this.requestId}/applications/${applicationId}/confirm`, {
                        status: 'confirmed',
                    });
                    alert('Заявка одобрена!');
                    await this.fetchApplications();
                } catch (error) {
                    console.error('Ошибка одобрения заявки:', error);
                }
            },
            async declineApplication(applicationId) {
                try {
                    await api.patch(`/requests/${this.requestId}/applications/${applicationId}/update`, {
                        status: 'declined',
                    });
                    alert('Заявка отклонена!');
                    await this.fetchApplications();
                } catch (error) {
                    console.error('Ошибка отклонения заявки:', error);
                }
            },

            async viewFeedback(userUid) {
                try {
                    const response = await api.get(`/feedback/by-user/${userUid}`);
                    this.feedbacks = response.data.data || [];
                    this.showFeedbackModal = true;
                } catch (error) {
                    console.error('Ошибка загрузки отзывов:', error);
                }
            },

            openFeedbackForm(userUid) {
                this.feedbackForm.user_uid = userUid;
                this.feedbackForm.rating = 5;
                this.feedbackForm.comment = '';
                this.showFeedbackFormModal = true;
            },
            async submitFeedback() {
                try {
                    await api.post('/feedback/', {
                        user_uid: this.feedbackForm.user_uid,
                        rating: this.feedbackForm.rating,
                        comment: this.feedbackForm.comment,
                    });
                    alert('Отзыв успешно отправлен!');
                    this.showFeedbackFormModal = false;
                } catch (error) {
                    console.error('Ошибка отправки отзыва:', error);
                }
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
