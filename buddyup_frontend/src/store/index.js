// src/store/index.js
import { createStore } from "vuex";
import auth from "@/store/modules/auth";

const store = createStore({
    modules: {
        auth
    }
});

export default store;
