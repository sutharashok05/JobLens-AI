import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  BriefcaseBusiness,
  CalendarDays,
  CheckCircle2,
  ExternalLink,
  MapPin,
  Sparkles,
} from "lucide-react";
import { useLocation, useNavigate, useParams } from "react-router-dom";

function JobDetails() {
  const location = useLocation();
  const navigate = useNavigate();
  const { jobId } = useParams();

  // First priority: job passed through React Router state
  const [job, setJob] = useState(location.state?.job || null);

  /*
   * Fallback:
   * If the page is refreshed directly on /jobs/:jobId,
   * restore the job from sessionStorage.
   */
  useEffect(() => {
    if (job) {
      return;
    }

    try {
      const prefix = "joblens-job-";

      for (const key of Object.keys(sessionStorage)) {
        if (!key.startsWith(prefix)) {
          continue;
        }

        const rawJob = sessionStorage.getItem(key);

        if (!rawJob) {
          continue;
        }

        const storedJob = JSON.parse(rawJob);

        if (!storedJob) {
          continue;
        }

        if (
          String(storedJob.external_id || "") ===
          String(jobId)
        ) {
          setJob(storedJob);
          break;
        }
      }
    } catch (error) {
      console.error(
        "Unable to restore job details:",
        error
      );
    }
  }, [job, jobId]);

  /*
   * If no job is available, show a friendly fallback page.
   */
  if (!job) {
    return (
      <div className="min-h-[calc(100vh-64px)] bg-slate-50 px-5 py-10">
        <div className="mx-auto max-w-4xl">
          <button
            type="button"
            onClick={() => navigate("/jobs")}
            className="mb-6 flex items-center gap-2 text-sm font-medium text-slate-500 transition hover:text-indigo-600"
          >
            <ArrowLeft size={16} />
            Back to Jobs
          </button>

          <div className="rounded-2xl border border-slate-200 bg-white px-6 py-16 text-center shadow-sm">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
              <BriefcaseBusiness size={24} />
            </div>

            <h1 className="mt-5 text-xl font-bold text-slate-900">
              Job not found
            </h1>

            <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
              This job is no longer available in the
              current search session.
            </p>

            <button
              type="button"
              onClick={() => navigate("/jobs")}
              className="mt-6 rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-700"
            >
              Find Jobs
            </button>
          </div>
        </div>
      </div>
    );
  }

  /*
   * Extract JobLens metadata safely.
   */
  const sourceMetadata =
    job.source_metadata || {};

  const matching =
    sourceMetadata.matching || {};

  const ranking =
    sourceMetadata.ranking || {};

  const verification =
    sourceMetadata.verification || {};

  const matchScore =
    Number(matching.match_score) || 0;

  const matchedSkills =
    Array.isArray(matching.matched_skills)
      ? matching.matched_skills
      : [];

  const missingSkills =
    Array.isArray(matching.missing_skills)
      ? matching.missing_skills
      : [];

  const jobUrl =
    job.apply_url ||
    job.job_url ||
    job.url ||
    "#";

  /*
   * Go back to the jobs page.
   *
   * IMPORTANT:
   * We do NOT clear Redux/localStorage jobs here.
   * Therefore /jobs can restore the previous search.
   */
  const handleBackToJobs = () => {
    navigate("/jobs");
  };

  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-50">
      {/* Background decoration */}
      <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
        <div className="absolute left-[10%] top-20 h-72 w-72 rounded-full bg-indigo-200/20 blur-[100px]" />

        <div className="absolute right-[5%] top-[35%] h-80 w-80 rounded-full bg-violet-200/20 blur-[110px]" />
      </div>

      <main className="mx-auto max-w-5xl px-5 py-8 sm:px-6 lg:px-8">
        {/* Back button */}
        <button
          type="button"
          onClick={handleBackToJobs}
          className="mb-6 flex items-center gap-2 text-sm font-medium text-slate-500 transition hover:text-indigo-600"
        >
          <ArrowLeft size={16} />
          Back to Jobs
        </button>

        {/* Main Job Card */}
        <motion.div
          initial={{
            opacity: 0,
            y: 18,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.45,
          }}
          className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm"
        >
          {/* =========================
              JOB HEADER
          ========================== */}
          <div className="border-b border-slate-100 p-6 sm:p-8">
            <div className="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
              {/* Job Identity */}
              <div className="flex min-w-0 gap-4">
                <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
                  <BriefcaseBusiness size={24} />
                </div>

                <div className="min-w-0">
                  {/* Source + Verification */}
                  <div className="flex flex-wrap items-center gap-2">
                    {job.source && (
                      <span className="rounded-md bg-slate-100 px-2 py-1 text-[10px] font-bold uppercase tracking-wide text-slate-500">
                        {job.source}
                      </span>
                    )}

                    {verification.verified === true && (
                      <span className="flex items-center gap-1 rounded-md bg-emerald-50 px-2 py-1 text-[10px] font-semibold text-emerald-700">
                        <CheckCircle2 size={12} />
                        Verified
                      </span>
                    )}
                  </div>

                  {/* Job Title */}
                  <h1 className="mt-3 break-words text-2xl font-bold tracking-tight text-slate-950 sm:text-3xl">
                    {job.title ||
                      "Job title not specified"}
                  </h1>

                  {/* Company */}
                  <p className="mt-2 text-sm font-medium text-slate-500">
                    {job.company ||
                      "Company not specified"}
                  </p>
                </div>
              </div>

              {/* Resume Match */}
              <div className="flex shrink-0 flex-col items-start gap-1 sm:items-end">
                <span className="text-xs font-medium text-slate-400">
                  Resume Match
                </span>

                <span
                  className={`text-3xl font-bold ${
                    matchScore >= 80
                      ? "text-emerald-600"
                      : matchScore >= 60
                        ? "text-indigo-600"
                        : matchScore >= 40
                          ? "text-amber-600"
                          : "text-slate-600"
                  }`}
                >
                  {Math.round(matchScore)}%
                </span>
              </div>
            </div>

            {/* Job Meta Information */}
            <div className="mt-6 flex flex-wrap gap-x-5 gap-y-3 text-sm text-slate-500">
              {/* Location */}
              {job.location && (
                <span className="flex items-center gap-2">
                  <MapPin size={16} />
                  {job.location}
                </span>
              )}

              {/* Employment Type */}
              {job.employment_type && (
                <span className="flex items-center gap-2">
                  <BriefcaseBusiness size={16} />
                  {job.employment_type}
                </span>
              )}

              {/* Posted Date */}
              {job.posted_at && (
                <span className="flex items-center gap-2">
                  <CalendarDays size={16} />
                  {formatDate(job.posted_at)}
                </span>
              )}
            </div>
          </div>

          {/* =========================
              JOB CONTENT
          ========================== */}
          <div className="grid gap-8 p-6 sm:p-8 lg:grid-cols-[1fr_300px]">
            {/* LEFT COLUMN */}
            <section>
              {/* Job Description Heading */}
              <div className="flex items-center gap-2">
                <Sparkles
                  size={18}
                  className="text-indigo-600"
                />

                <h2 className="text-lg font-bold text-slate-900">
                  Job Description
                </h2>
              </div>

              {/* Job Description */}
              <p className="mt-4 whitespace-pre-line text-sm leading-7 text-slate-600">
                {job.description ||
                  "No description available."}
              </p>

              {/* =========================
                  MATCHED SKILLS
              ========================== */}
              {matchedSkills.length > 0 && (
                <div className="mt-8">
                  <h3 className="text-sm font-bold text-slate-900">
                    Skills You Match
                  </h3>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {matchedSkills.map(
                      (skill, index) => (
                        <span
                          key={`${skill}-${index}`}
                          className="rounded-lg bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700"
                        >
                          {skill}
                        </span>
                      )
                    )}
                  </div>
                </div>
              )}

              {/* =========================
                  MISSING SKILLS
              ========================== */}
              {missingSkills.length > 0 && (
                <div className="mt-7">
                  <h3 className="text-sm font-bold text-slate-900">
                    Skills to Improve
                  </h3>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {missingSkills.map(
                      (skill, index) => (
                        <span
                          key={`${skill}-${index}`}
                          className="rounded-lg bg-amber-50 px-3 py-1.5 text-xs font-medium text-amber-700"
                        >
                          {skill}
                        </span>
                      )
                    )}
                  </div>
                </div>
              )}

              {/* =========================
                  ADDITIONAL JOB INFO
              ========================== */}
              {(job.salary ||
                job.salary_min ||
                job.salary_max ||
                job.category) && (
                <div className="mt-8 rounded-2xl border border-slate-200 bg-slate-50 p-5">
                  <h3 className="text-sm font-bold text-slate-900">
                    Additional Information
                  </h3>

                  <div className="mt-4 grid gap-3 sm:grid-cols-2">
                    {job.salary && (
                      <InfoItem
                        label="Salary"
                        value={job.salary}
                      />
                    )}

                    {!job.salary &&
                      job.salary_min && (
                        <InfoItem
                          label="Minimum Salary"
                          value={job.salary_min}
                        />
                      )}

                    {!job.salary &&
                      job.salary_max && (
                        <InfoItem
                          label="Maximum Salary"
                          value={job.salary_max}
                        />
                      )}

                    {job.category && (
                      <InfoItem
                        label="Category"
                        value={job.category}
                      />
                    )}
                  </div>
                </div>
              )}
            </section>

            {/* =========================
                RIGHT SIDEBAR
            ========================== */}
            <aside className="h-fit rounded-2xl border border-slate-200 bg-slate-50 p-5">
              <h3 className="text-sm font-bold text-slate-900">
                JobLens Recommendation
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-500">
                This opportunity is ranked using
                your skills, preferred roles,
                location and job freshness.
              </p>

              {/* Ranking Score */}
              {ranking.final_score !==
                undefined &&
                ranking.final_score !== null && (
                  <div className="mt-5 flex items-center justify-between border-t border-slate-200 pt-4">
                    <span className="text-xs font-medium text-slate-500">
                      Ranking Score
                    </span>

                    <span className="text-sm font-bold text-slate-900">
                      {Number(
                        ranking.final_score
                      ).toFixed(1)}
                    </span>
                  </div>
                )}

              {/* Match Score */}
              <div className="mt-4 flex items-center justify-between">
                <span className="text-xs font-medium text-slate-500">
                  Resume Match
                </span>

                <span className="text-sm font-bold text-indigo-600">
                  {Math.round(matchScore)}%
                </span>
              </div>

              {/* Verification */}
              {verification.verified === true && (
                <div className="mt-4 flex items-center gap-2 rounded-xl bg-emerald-50 px-3 py-2.5 text-xs font-medium text-emerald-700">
                  <CheckCircle2 size={15} />
                  Job verified
                </div>
              )}

              {/* Apply Button */}
              <a
                href={jobUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={`mt-6 flex w-full items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-semibold text-white shadow-lg transition ${
                  jobUrl === "#"
                    ? "pointer-events-none bg-slate-400 shadow-none"
                    : "bg-indigo-600 shadow-indigo-600/20 hover:bg-indigo-700"
                }`}
                aria-disabled={jobUrl === "#"}
              >
                Apply Now
                <ExternalLink size={16} />
              </a>

              {/* Back Button */}
              <button
                type="button"
                onClick={handleBackToJobs}
                className="mt-3 flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-indigo-200 hover:text-indigo-600"
              >
                <ArrowLeft size={16} />
                Back to Jobs
              </button>
            </aside>
          </div>
        </motion.div>
      </main>
    </div>
  );
}

/*
 * Small reusable information item.
 */
function InfoItem({ label, value }) {
  if (
    value === undefined ||
    value === null ||
    value === ""
  ) {
    return null;
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-3">
      <p className="text-[11px] font-medium uppercase tracking-wide text-slate-400">
        {label}
      </p>

      <p className="mt-1 break-words text-sm font-semibold text-slate-700">
        {String(value)}
      </p>
    </div>
  );
}

/*
 * Format posted date.
 */
function formatDate(value) {
  try {
    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
      return "";
    }

    return date.toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  } catch {
    return "";
  }
}

export default JobDetails;