import axios from "axios";

const api = axios.create({
  baseURL: "https://joblens-backend-new.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;