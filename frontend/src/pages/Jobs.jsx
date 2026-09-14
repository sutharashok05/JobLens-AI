import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setJobs, setLoading, setSearchParams } from "../store/jobsSlice";
import { motion, AnimatePresence } from "framer-motion";
import {
  AlertCircle,
  ArrowRight,
  BriefcaseBusiness,
  CalendarDays,
  CheckCircle2,
  ExternalLink,
  Filter,
  MapPin,
  RotateCcw,
  Search,
  Sparkles,
  X,
} from "lucide-react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";


function Jobs() {
  const [query, setQuery] = useState(() => {
    try {
      const saved = localStorage.getItem("joblens_search_params");
      const parsed = saved ? JSON.parse(saved) : null;
      return parsed?.query || "";
    } catch {
      return "";
    }
  });
  const dispatch = useDispatch();

  const jobs = useSelector((state) => state.jobs.jobs);
  const loading = useSelector((state) => state.jobs.loading);
  const reduxSearchParams = useSelector((state) => state.jobs.searchParams);

  const [searchParams, setLocalSearchParams] = useState(() => {
    try {
      const saved = localStorage.getItem("joblens_search_params");
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("joblens_jobs") || "[]").length > 0;
    } catch {
      return false;
    }
  });

  const [showFilters, setShowFilters] = useState(false);

  const [sortBy, setSortBy] = useState("match");
  const navigate = useNavigate();

  useEffect(() => {
    if (reduxSearchParams?.query) {
      setLocalSearchParams(reduxSearchParams);
      setQuery((current) => current || reduxSearchParams.query);
      setHasSearched(true);
    }
  }, [reduxSearchParams]);


  const searchJobs = async () => {
    if (!query.trim()) {
      setError("Please enter a job search.");
      return;
    }

    const params = {
      query: query.trim(),
    };

    try {
      dispatch(setLoading(true));
      setError("");
      setHasSearched(true);

      // Save the search so Refresh Jobs can repeat the same search.
      dispatch(setSearchParams(params));
      setLocalSearchParams(params);

      const response = await api.post(
        "/api/search/jobs",
        params
      );

      // Replace the previous result only after the new search succeeds.
      dispatch(setJobs(response.data.jobs || []));
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to search jobs. Please try again."
      );
    } finally {
      dispatch(setLoading(false));
    }
  };

  const refreshJobs = async () => {
    const params = searchParams || reduxSearchParams;

    if (!params?.query?.trim()) {
      setError("Please perform a job search first.");
      return;
    }

    try {
      dispatch(setLoading(true));
      setError("");

      const response = await api.post(
        "/api/search/jobs",
        params
      );

      // Only the explicit Refresh Jobs button replaces the current list.
      dispatch(setJobs(response.data.jobs || []));
      setHasSearched(true);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to refresh jobs. Please try again."
      );
    } finally {
      dispatch(setLoading(false));
    }
  };


  const clearSearch = () => {
    setQuery("");
    setError("");
    // Do NOT clear Redux/localStorage jobs here.
    // Existing jobs remain available until a new search or explicit refresh.
  };

  const useExampleQuery = (example) => {
    setQuery(example);
    setError("");
  };

  const handleQueryChange = (value) => {
    setQuery(value);
    if (error) setError("");
  };

  const sortedJobs = [...jobs].sort(
    (a, b) => {

      if (sortBy === "match") {
        return (
          getMatchScore(b) -
          getMatchScore(a)
        );
      }

      if (sortBy === "freshness") {
        return (
          getPostedTimestamp(b) -
          getPostedTimestamp(a)
        );
      }

      return 0;
    }
  );


  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-50">

      {/* =====================================================
          BACKGROUND
      ====================================================== */}

      <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">

        <div className="absolute left-[10%] top-20 h-72 w-72 rounded-full bg-indigo-200/20 blur-[100px]" />

        <div className="absolute right-[5%] top-[35%] h-80 w-80 rounded-full bg-violet-200/20 blur-[110px]" />

      </div>


      {/* =====================================================
          PAGE
      ====================================================== */}

      <main className="mx-auto max-w-7xl px-5 py-8 sm:px-6 lg:px-8">


        {/* ===================================================
            HEADER
        ==================================================== */}

        <motion.div
          initial={{
            opacity: 0,
            y: 15,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.5,
          }}
        >

          <div className="flex items-center gap-2 text-sm font-medium text-indigo-600">

            <Sparkles size={16} />

            AI Job Discovery

          </div>


          <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
            Find your next opportunity
          </h1>


          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
            Search for jobs and let JobLens rank them according
            to your resume, skills and preferences.
          </p>

        </motion.div>


        {/* ===================================================
            SEARCH BAR
        ==================================================== */}

        <motion.div
          initial={{
            opacity: 0,
            y: 20,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.5,
            delay: 0.1,
          }}
          className="mt-7 rounded-2xl border border-slate-200 bg-white p-3 shadow-sm"
        >

          <div className="flex flex-col gap-3 md:flex-row">

            {/* Input */}

            <div className="relative flex-1">

              <Search
                size={19}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
              />

              <input
                type="text"
                value={query}
                placeholder="Try: AI Engineer Bangalore"
                onChange={(event) =>
                  handleQueryChange(event.target.value)
                }
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    searchJobs();
                  }
                }}
                className="h-12 w-full rounded-xl border border-slate-200 bg-slate-50 pl-11 pr-11 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
              />

              {query && !loading && (
                <button
                  type="button"
                  onClick={() => handleQueryChange("")}
                  aria-label="Clear search"
                  className="absolute right-3 top-1/2 flex -translate-y-1/2 items-center justify-center rounded-md p-1.5 text-slate-400 transition hover:bg-slate-200 hover:text-slate-600"
                >
                  <X size={15} />
                </button>
              )}

            </div>


            {/* Filter */}

            <button
              onClick={() =>
                setShowFilters(!showFilters)
              }
              className={`flex h-12 items-center justify-center gap-2 rounded-xl border px-4 text-sm font-medium transition ${
                showFilters
                  ? "border-indigo-200 bg-indigo-50 text-indigo-700"
                  : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
              }`}
            >

              <Filter size={17} />

              Filters

            </button>


            {/* Search */}

            <motion.button
              whileHover={{
                y: -1,
              }}
              whileTap={{
                scale: 0.98,
              }}
              onClick={searchJobs}
              disabled={loading}
              className="flex h-12 items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none"
            >

              {loading ? (
                <>
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />

                  Searching...
                </>
              ) : (
                <>
                  <Search size={17} />

                  Search Jobs
                </>
              )}

            </motion.button>

          </div>


          {/* QUICK SEARCHES */}
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <span className="text-[11px] font-semibold uppercase tracking-wide text-slate-400">
              Try
            </span>
            {["AI Engineer Bangalore", "Python Developer Pune", "ML Engineer Hyderabad"].map((example) => (
              <button
                key={example}
                type="button"
                onClick={() => useExampleQuery(example)}
                className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-600 transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700"
              >
                {example}
              </button>
            ))}
          </div>

          {/* =================================================
              FILTER PANEL
          ================================================== */}

          <AnimatePresence>

            {showFilters && (
              <motion.div
                initial={{
                  opacity: 0,
                  height: 0,
                }}
                animate={{
                  opacity: 1,
                  height: "auto",
                }}
                exit={{
                  opacity: 0,
                  height: 0,
                }}
                className="overflow-hidden"
              >

                <div className="mt-3 border-t border-slate-100 pt-4">

                  <div className="flex flex-wrap items-center gap-3">

                    <label className="text-xs font-medium text-slate-500">
                      Sort by
                    </label>

                    <select
                      value={sortBy}
                      onChange={(event) =>
                        setSortBy(event.target.value)
                      }
                      className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 outline-none focus:border-indigo-400"
                    >

                      <option value="match">
                        Best Match
                      </option>

                      <option value="freshness">
                        Recently Posted
                      </option>

                    </select>

                  </div>

                </div>

              </motion.div>
            )}

          </AnimatePresence>

        </motion.div>


        {/* ===================================================
            ERROR
        ==================================================== */}

        <AnimatePresence>

          {error && (
            <motion.div
              initial={{
                opacity: 0,
                y: -10,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              exit={{
                opacity: 0,
              }}
              className="mt-5 flex items-center justify-between rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700"
            >

              <span>{error}</span>

              <button
                onClick={() => setError("")}
                className="text-red-400 hover:text-red-600"
              >
                <X size={17} />
              </button>

            </motion.div>
          )}

        </AnimatePresence>


        {/* ===================================================
            RESULTS HEADER
        ==================================================== */}

        {jobs.length > 0 && (
          <motion.div
            initial={{
              opacity: 0,
            }}
            animate={{
              opacity: 1,
            }}
            className="mt-8 flex flex-col justify-between gap-3 sm:flex-row sm:items-center"
          >

            <div>

              <h2 className="text-lg font-bold text-slate-900">
                Recommended Jobs
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                {jobs.length} opportunities found for your search
              </p>

            </div>


            <div className="flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={refreshJobs}
                disabled={loading || !(searchParams || reduxSearchParams)?.query}
                className="inline-flex items-center justify-center gap-2 rounded-lg border border-indigo-200 bg-white px-3 py-2 text-xs font-semibold text-indigo-700 transition hover:bg-indigo-50 disabled:cursor-not-allowed disabled:opacity-50"
                title="Run the same search again and replace the current jobs"
              >
                <RotateCcw
                  size={14}
                  className={loading ? "animate-spin" : ""}
                />
                {loading ? "Refreshing..." : "Refresh Jobs"}
              </button>

              <div className="flex items-center gap-2 rounded-lg bg-indigo-50 px-3 py-2 text-xs font-medium text-indigo-700">
                <Sparkles size={14} />
                Ranked by AI Match
              </div>
            </div>

          </motion.div>
        )}


        {/* ===================================================
            ERROR STATE
        ==================================================== */}

        {!loading && error && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-7 rounded-2xl border border-red-200 bg-red-50 p-5"
          >
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-start gap-3">
                <div className="mt-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-red-600 shadow-sm">
                  <AlertCircle size={20} />
                </div>
                <div>
                  <h2 className="font-semibold text-red-900">Search failed</h2>
                  <p className="mt-1 text-sm leading-6 text-red-700">{error}</p>
                </div>
              </div>

              <button
                type="button"
                onClick={searchJobs}
                disabled={!query.trim()}
                className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-600 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <RotateCcw size={15} />
                Try Again
              </button>
            </div>
          </motion.div>
        )}

        {/* ===================================================
            SEARCH SUMMARY
        ==================================================== */}

        {!loading && hasSearched && !error && jobs.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-7 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between"
          >
            <div>
              <p className="text-sm font-semibold text-slate-900">
                {jobs.length} {jobs.length === 1 ? "job" : "jobs"} found
              </p>
              <p className="mt-0.5 text-xs text-slate-500">
                Results personalized for <span className="font-medium text-slate-700">{query}</span>
              </p>
            </div>

            <button
              type="button"
              onClick={clearSearch}
              className="inline-flex items-center gap-1.5 self-start rounded-lg px-3 py-2 text-xs font-semibold text-slate-500 transition hover:bg-white hover:text-indigo-600 sm:self-auto"
            >
              <RotateCcw size={13} />
              New search
            </button>
          </motion.div>
        )}

        {/* ===================================================
            LOADING
        ==================================================== */}

        {loading && (
          <div className="mt-7 grid gap-5 lg:grid-cols-2">

            {[1, 2, 3, 4].map((item) => (
              <JobSkeleton key={item} />
            ))}

          </div>
        )}


        {/* ===================================================
            JOB GRID
        ==================================================== */}

        {!loading && sortedJobs.length > 0 && (
          <div className="mt-7 grid gap-5 lg:grid-cols-2">

            {sortedJobs.map(
              (job, index) => (
                <JobCard
                  key={`${job.source}-${job.external_id || index}`}
                  job={job}
                  index={index}
                  onOpen={() => {
                    const jobKey = `${job.source}-${job.external_id || index}`;

                    sessionStorage.setItem(
                      `joblens-job-${jobKey}`,
                      JSON.stringify(job)
                    );

                    navigate(
                      `/jobs/${encodeURIComponent(
                        job.external_id || index
                      )}`,
                      {
                        state: {
                          job,
                          jobKey,
                        },
                      }
                    );
                  }}
                />
              )
            )}

          </div>
        )}


        {/* ===================================================
            ERROR STATE
        ==================================================== */}

        {!loading && error && (
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-10 rounded-2xl border border-red-200 bg-white p-8 text-center shadow-sm"
          >
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-red-50 text-red-600">
              <AlertCircle size={22} />
            </div>
            <h2 className="mt-4 text-lg font-bold text-slate-900">
              We couldn't complete that search
            </h2>
            <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
              {error}
            </p>
            <button
              type="button"
              onClick={searchJobs}
              className="mt-5 inline-flex items-center gap-2 rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-600"
            >
              <RotateCcw size={15} />
              Try Again
            </button>
          </motion.div>
        )}

        {/* ===================================================
            EMPTY STATE
        ==================================================== */}

        {!loading && !error && !hasSearched && (
          <EmptyState onExampleClick={useExampleQuery} />
        )}

        {!loading && !error && hasSearched && jobs.length === 0 && (
          <NoResultsState
            query={query}
            onClear={clearSearch}
          />
        )}

      </main>

    </div>
  );
}


/* =========================================================
   JOB CARD
========================================================= */

function JobCard({
  job,
  index,
  onOpen,
}) {

  const matching =
    job.source_metadata?.matching || {};

  const ranking =
    job.source_metadata?.ranking || {};

  const verification =
    job.source_metadata?.verification || {};

  const matchScore =
    Number(matching.match_score) || 0;

  const matchedSkills =
    matching.matched_skills || [];

  const missingSkills =
    matching.missing_skills || [];


  return (
    <motion.article
      initial={{
        opacity: 0,
        y: 25,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      transition={{
        duration: 0.45,
        delay: Math.min(index * 0.06, 0.4),
      }}
      whileHover={{
        y: -4,
      }}
      onClick={onOpen}
      role="button"
      tabIndex={0}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onOpen?.();
        }
      }}
      className="group cursor-pointer rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-shadow hover:border-indigo-200 hover:shadow-xl hover:shadow-indigo-100/30"
    >

      {/* ===================================================
          TOP
      ==================================================== */}

      <div className="flex gap-4">

        {/* Company icon */}

        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-600 transition group-hover:bg-indigo-50 group-hover:text-indigo-600">

          <BriefcaseBusiness size={20} />

        </div>


        {/* Title */}

        <div className="min-w-0 flex-1">

          <h3 className="line-clamp-2 text-base font-bold text-slate-900">
            {job.title}
          </h3>

          <p className="mt-1 truncate text-sm font-medium text-slate-500">
            {job.company || "Company not specified"}
          </p>

        </div>


        {/* Match */}

        <MatchScore score={matchScore} />

      </div>


      {/* ===================================================
          META
      ==================================================== */}

      <div className="mt-5 flex flex-wrap gap-x-4 gap-y-2 text-xs text-slate-500">

        <span className="flex items-center gap-1.5">

          <MapPin size={14} />

          {job.location || "Location not specified"}

        </span>


        {job.employment_type && (
          <span className="flex items-center gap-1.5">

            <BriefcaseBusiness size={14} />

            {job.employment_type}

          </span>
        )}


        {job.posted_at && (
          <span className="flex items-center gap-1.5">

            <CalendarDays size={14} />

            {formatDate(job.posted_at)}

          </span>
        )}

      </div>


      {/* ===================================================
          DESCRIPTION
      ==================================================== */}

      {job.description && (
        <p className="mt-4 line-clamp-3 text-sm leading-6 text-slate-500">
          {job.description}
        </p>
      )}


      {/* ===================================================
          MATCHED SKILLS
      ==================================================== */}

      {matchedSkills.length > 0 && (
        <div className="mt-5">

          <div className="mb-2 flex items-center gap-2">

            <CheckCircle2
              size={15}
              className="text-emerald-500"
            />

            <span className="text-xs font-semibold text-slate-700">
              Matched Skills
            </span>

          </div>


          <div className="flex flex-wrap gap-1.5">

            {matchedSkills
              .slice(0, 7)
              .map((skill, skillIndex) => (
                <span
                  key={`${skill}-${skillIndex}`}
                  className="rounded-md bg-emerald-50 px-2 py-1 text-[11px] font-medium text-emerald-700"
                >
                  {skill}
                </span>
              ))}

          </div>

        </div>
      )}


      {/* ===================================================
          MISSING SKILLS
      ==================================================== */}

      {missingSkills.length > 0 && (
        <div className="mt-4">

          <div className="mb-2 text-xs font-semibold text-slate-700">
            Skills to Improve
          </div>

          <div className="flex flex-wrap gap-1.5">

            {missingSkills
              .slice(0, 5)
              .map((skill, skillIndex) => (
                <span
                  key={`${skill}-${skillIndex}`}
                  className="rounded-md bg-amber-50 px-2 py-1 text-[11px] font-medium text-amber-700"
                >
                  {skill}
                </span>
              ))}

          </div>

        </div>
      )}


      {/* ===================================================
          FOOTER
      ==================================================== */}

      <div className="mt-5 flex flex-col gap-3 border-t border-slate-100 pt-4 sm:flex-row sm:items-center sm:justify-between">

        {/* Source + verification */}

        <div className="flex flex-wrap items-center gap-2">

          <span className="rounded-md bg-slate-100 px-2 py-1 text-[10px] font-semibold uppercase tracking-wide text-slate-500">
            {job.source}
          </span>


          {verification.verified === true && (
            <span className="flex items-center gap-1 rounded-md bg-emerald-50 px-2 py-1 text-[10px] font-semibold text-emerald-700">

              <CheckCircle2 size={12} />

              Verified

            </span>
          )}

        </div>


        {/* Ranking */}

        {ranking.final_score !== undefined && (
          <span className="text-[11px] text-slate-400">
            Ranking {Number(
              ranking.final_score
            ).toFixed(1)}
          </span>
        )}


        {/* Apply */}

        <a
          href={
            job.apply_url ||
            job.job_url
          }
          target="_blank"
          rel="noopener noreferrer"
          onClick={(event) => event.stopPropagation()}
          className="group/apply flex items-center justify-center gap-2 rounded-lg bg-slate-950 px-4 py-2.5 text-xs font-semibold text-white transition hover:bg-indigo-600"
        >

          Apply Now

          <ExternalLink
            size={14}
            className="transition-transform group-hover/apply:translate-x-0.5 group-hover/apply:-translate-y-0.5"
          />

        </a>

      </div>

    </motion.article>
  );
}


/* =========================================================
   MATCH SCORE
========================================================= */

function MatchScore({
  score,
}) {

  const getScoreStyle = () => {

    if (score >= 80) {
      return {
        container:
          "border-emerald-200 bg-emerald-50",
        text:
          "text-emerald-700",
      };
    }

    if (score >= 60) {
      return {
        container:
          "border-indigo-200 bg-indigo-50",
        text:
          "text-indigo-700",
      };
    }

    if (score >= 40) {
      return {
        container:
          "border-amber-200 bg-amber-50",
        text:
          "text-amber-700",
      };
    }

    return {
      container:
        "border-slate-200 bg-slate-50",
      text:
        "text-slate-600",
    };
  };


  const style = getScoreStyle();


  return (
    <div
      className={`flex h-14 w-14 shrink-0 flex-col items-center justify-center rounded-full border ${style.container}`}
    >

      <span
        className={`text-sm font-bold ${style.text}`}
      >
        {Math.round(score)}%
      </span>

      <span className="text-[8px] font-medium text-slate-400">
        MATCH
      </span>

    </div>
  );
}


/* =========================================================
   SKELETON
========================================================= */

function JobSkeleton() {

  return (
    <div className="animate-pulse rounded-2xl border border-slate-200 bg-white p-5">

      <div className="flex gap-4">

        <div className="h-11 w-11 rounded-xl bg-slate-200" />

        <div className="flex-1">

          <div className="h-4 w-3/4 rounded bg-slate-200" />

          <div className="mt-2 h-3 w-1/2 rounded bg-slate-200" />

        </div>

        <div className="h-14 w-14 rounded-full bg-slate-200" />

      </div>


      <div className="mt-5 space-y-2">

        <div className="h-3 w-full rounded bg-slate-200" />

        <div className="h-3 w-5/6 rounded bg-slate-200" />

        <div className="h-3 w-2/3 rounded bg-slate-200" />

      </div>


      <div className="mt-5 flex gap-2">

        <div className="h-6 w-16 rounded bg-slate-200" />

        <div className="h-6 w-20 rounded bg-slate-200" />

        <div className="h-6 w-14 rounded bg-slate-200" />

      </div>

    </div>
  );
}


/* =========================================================
   EMPTY STATE
========================================================= */

function EmptyState({ onExampleClick }) {

  return (
    <motion.div
      initial={{
        opacity: 0,
        y: 20,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      className="mt-10 rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-16 text-center"
    >

      <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">

        <Search size={24} />

      </div>


      <h2 className="mt-5 text-lg font-bold text-slate-900">
        Start your job search
      </h2>


      <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
        Search for a role and location above. JobLens will
        discover opportunities and rank them based on your
        profile.
      </p>


      <div className="mt-6 flex flex-wrap justify-center gap-2">

        {[
          "AI Engineer Bangalore",
          "Python Developer Pune",
          "ML Engineer Hyderabad",
        ].map((example) => (
          <button
            key={example}
            type="button"
            onClick={() => onExampleClick?.(example)}
            className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-xs font-medium text-slate-600 transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700"
          >
            {example}
          </button>
        ))}

      </div>

    </motion.div>
  );
}


function NoResultsState({ query, onClear }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mt-10 rounded-2xl border border-slate-200 bg-white px-6 py-14 text-center shadow-sm"
    >
      <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-100 text-slate-500">
        <Search size={24} />
      </div>

      <h2 className="mt-5 text-lg font-bold text-slate-900">
        No matching jobs found
      </h2>

      <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-slate-500">
        We searched the connected job sources for <span className="font-semibold text-slate-700">"{query}"</span>, but nothing matched this search. Try a broader role, another location, or a different keyword.
      </p>

      <button
        type="button"
        onClick={onClear}
        className="mt-6 inline-flex items-center gap-2 rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-600"
      >
        <X size={15} />
        Start New Search
      </button>
    </motion.div>
  );
}


/* =========================================================
   HELPERS
========================================================= */

function getMatchScore(job) {

  return (
    Number(
      job.source_metadata
        ?.matching
        ?.match_score
    ) || 0
  );
}


function getPostedTimestamp(job) {

  if (!job.posted_at) {
    return 0;
  }

  const timestamp =
    new Date(job.posted_at).getTime();

  return Number.isNaN(timestamp)
    ? 0
    : timestamp;
}


function formatDate(value) {

  try {

    const date =
      new Date(value);

    if (Number.isNaN(
      date.getTime()
    )) {
      return "";
    }

    return date.toLocaleDateString(
      "en-IN",
      {
        day: "numeric",
        month: "short",
        year: "numeric",
      }
    );

  } catch {
    return "";
  }
}


export default Jobs;