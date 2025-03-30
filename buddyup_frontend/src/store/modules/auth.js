import axios from 'axios';

const API_BASE_URL = 'https://buddyup.hab.mishanikolaev.ru'; // Замените на фактический базовый URL вашего API

// Создаём экземпляр axios с заданным базовым URL
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000
});

const STORAGE_KEY = "authParams";

function getStoredAuthParams() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
        try {
            return JSON.parse(stored);
        } catch (error) {
            console.error("Ошибка парсинга authParams из localStorage", error);
        }
    }
    return null;
}

function setStoredAuthParams(params) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(params));
}

function clearStoredAuthParams() {
    localStorage.removeItem(STORAGE_KEY);
}

export default {
    namespaced: true,
    state: {
        fio: "",
        gn: "",
        uid: "",
        // дополнительные поля можно добавить по необходимости
    },
    mutations: {
        SET_AUTH_PARAMS(state, params) {
            state.fio = params.fio;
            state.gn = params.gn;
            state.uid = params.uid;
        }
    },
    actions: {
        initAuthParams({ commit }) {
            const urlParams = new URLSearchParams(window.location.search);
            const fio = urlParams.get("fio")?.trim();
            const gn = urlParams.get("gn")?.trim();
            const uid = urlParams.get("uid")?.trim();

            if (fio && gn && uid) {
                // Если данные присутствуют в URL, сбрасываем ранее сохранённые параметры
                clearStoredAuthParams();
                // Выполняем запрос к API /users/profile с данными из URL
                apiClient.get('/users/profile', { params: { uid, fio, gn } })
                    .then(response => {
                    if (response.data && response.data.status === "success") {
                        // Извлекаем данные профиля из ответа API
                        const profileData = response.data.data;
                        // Обновляем состояние Vuex
                        commit("SET_AUTH_PARAMS", {
                            fio: profileData.fio,
                            gn: profileData.group_number,
                            uid: profileData.uid,
                        });
                        // Сохраняем данные в localStorage
                        setStoredAuthParams({
                            fio: profileData.fio,
                            gn: profileData.group_number,
                            uid: profileData.uid,
                        });
                    } else {
                        alert("Ошибка получения профиля: " + response.data.message);
                    }
                })
                    .catch(error => {
                    alert("Ошибка запроса к API: " + error.message);
                });
            } else {
                // Если в URL отсутствуют параметры, пробуем получить их из localStorage
                const stored = getStoredAuthParams();
                if (stored && stored.fio && stored.gn && stored.uid) {
                    commit("SET_AUTH_PARAMS", stored);
                } else {
                    alert("Отсутствуют параметры авторизации.");
                }
            }
        },
        updateAuthParams({ commit }, params) {
            setStoredAuthParams(params);
            commit("SET_AUTH_PARAMS", params);
        }
    },
    getters: {
        authParams: (state) => ({
            fio: state.fio,
            gn: state.gn,
            uid: state.uid
        })
    }
};
