import { createSlice } from "@reduxjs/toolkit";

const JOBS_STORAGE_KEY = "joblens_jobs";
const SEARCH_STORAGE_KEY = "joblens_search_params";
const UPDATED_STORAGE_KEY = "joblens_jobs_updated";

const loadFromStorage = (key, fallback) => {
  try {
    const value = localStorage.getItem(key);

    if (!value) {
      return fallback;
    }

    return JSON.parse(value);
  } catch (error) {
    console.error(`Failed to load ${key}:`, error);
    return fallback;
  }
};

const initialState = {
  jobs: loadFromStorage(JOBS_STORAGE_KEY, []),

  searchParams: loadFromStorage(
    SEARCH_STORAGE_KEY,
    null
  ),

  loading: false,

  lastUpdated:
    localStorage.getItem(UPDATED_STORAGE_KEY) || null,
};

const jobsSlice = createSlice({
  name: "jobs",

  initialState,

  reducers: {
    setJobs: (state, action) => {
      const jobs = action.payload || [];

      state.jobs = jobs;
      state.lastUpdated = new Date().toISOString();

      localStorage.setItem(
        JOBS_STORAGE_KEY,
        JSON.stringify(jobs)
      );

      localStorage.setItem(
        UPDATED_STORAGE_KEY,
        state.lastUpdated
      );
    },

    setLoading: (state, action) => {
      state.loading = action.payload;
    },

    setSearchParams: (state, action) => {
      state.searchParams = action.payload;

      localStorage.setItem(
        SEARCH_STORAGE_KEY,
        JSON.stringify(action.payload)
      );
    },

    clearJobs: (state) => {
      state.jobs = [];
      state.lastUpdated = null;

      localStorage.removeItem(JOBS_STORAGE_KEY);
      localStorage.removeItem(UPDATED_STORAGE_KEY);
    },

    clearSearchParams: (state) => {
      state.searchParams = null;

      localStorage.removeItem(SEARCH_STORAGE_KEY);
    },
  },
});

export const {
  setJobs,
  setLoading,
  setSearchParams,
  clearJobs,
  clearSearchParams,
} = jobsSlice.actions;

export default jobsSlice.reducer;