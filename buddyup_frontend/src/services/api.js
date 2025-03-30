// src/services/api.js
import axios from "axios";
import store from "@/store";

const api = axios.create({
    baseURL: "https://buddyup.hab.mishanikolaev.ru"
});

api.interceptors.request.use((config) => {
    const authParams = store.getters["auth/authParams"];
    const currentParams = config.params || {};
    config.params = {
        ...currentParams,
        fio: authParams.fio,
        gn: authParams.gn,
        uid: authParams.uid,
    };
    return config;
}, (error) => Promise.reject(error));

export default api;


