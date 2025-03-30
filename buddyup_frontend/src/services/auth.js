// src/services/auth.js

const STORAGE_KEY = "authParams";

export function getAuthParams() {
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

export function setAuthParams(params) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(params));
}

export function initAuthParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const fio = urlParams.get("fio")?.trim();
    const gn = urlParams.get("gn")?.trim();
    const uid = urlParams.get("uid")?.trim();

    // Проверяем, что все параметры заданы и не пустые
    if (fio && gn && uid) {
        const params = { fio, gn, uid };
        setAuthParams(params);
        return params;
    }

    // Если в URL пусто или не заданы, пытаемся получить из localStorage
    const stored = getAuthParams();
    if (stored && stored.fio && stored.gn && stored.uid) {
        return stored;
    }

    // Если ничего не найдено – можно выбросить ошибку или вернуть null
    console.warn("Параметры авторизации не найдены или пусты");
    // В зависимости от логики приложения можно выбросить ошибку:
    // throw new Error("Необходимо указать параметры авторизации в URL");
    return { fio: "", gn: "", uid: "" };
}

