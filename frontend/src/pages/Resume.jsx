import { useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  CheckCircle2,
  FileText,
  Loader2,
  Sparkles,
  Trash2,
  Upload,
  X,
  UserRound,
  ArrowRight,
  ArrowRightIcon
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Resume() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const selectFile = (selectedFile) => {
    setError("");
    setMessage("");
    setResult(null);

    if (!selectedFile) {
      return;
    }

    if (selectedFile.type !== "application/pdf") {
      setError("Please upload a PDF resume.");
      return;
    }

    const maxSize = 10 * 1024 * 1024;

    if (selectedFile.size > maxSize) {
      setError("Resume size must be less than 10 MB.");
      return;
    }

    setFile(selectedFile);
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    selectFile(selectedFile);
  };

  const handleDrop = (event) => {
    event.preventDefault();

    setDragging(false);

    const droppedFile = event.dataTransfer.files?.[0];

    selectFile(droppedFile);
  };

  const removeFile = () => {
    setFile(null);
    setError("");
    setMessage("");
    setResult(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select your resume first.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");
      setResult(null);

      const formData = new FormData();

      formData.append("file", file);

      const response = await api.post(
        "/api/resumes/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data);

      setMessage(
        "Resume analyzed successfully!"
      );

    } catch (err) {
      console.error(err);

      const detail =
        err.response?.data?.detail;

      setError(
        typeof detail === "string"
          ? detail
          : "Unable to upload and analyze your resume."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-50">

      {/* Background */}
      <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">

        <div className="absolute left-[15%] top-20 h-72 w-72 rounded-full bg-indigo-200/30 blur-[100px]" />

        <div className="absolute bottom-10 right-[10%] h-72 w-72 rounded-full bg-violet-200/20 blur-[100px]" />

      </div>

      <div className="mx-auto max-w-6xl px-5 py-10 sm:px-6 lg:px-8">

        {/* Back */}
        <motion.button
          initial={{
            opacity: 0,
            x: -10,
          }}
          animate={{
            opacity: 1,
            x: 0,
          }}
          onClick={() => navigate("/")}
          className="mb-8 flex items-center gap-2 text-sm font-medium text-slate-500 transition hover:text-slate-900"
        >
          <ArrowLeft size={16} />
          Back to Dashboard
        </motion.button>

        {/* Header */}
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
          }}
          className="mx-auto max-w-2xl text-center"
        >

          <div className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-600 text-white shadow-lg shadow-indigo-600/20">
            <Sparkles size={22} />
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
            Let AI understand your resume
          </h1>

          <p className="mt-4 text-sm leading-6 text-slate-500 sm:text-base">
            Upload your resume and JobLens AI will extract your
            skills, experience, projects and career profile to find
            better job opportunities.
          </p>

        </motion.div>

        {/* Main content */}
        <div className="mx-auto mt-10 max-w-3xl">

          <AnimatePresence mode="wait">

            {!result ? (
              <motion.div
                key="upload"
                initial={{
                  opacity: 0,
                  y: 20,
                }}
                animate={{
                  opacity: 1,
                  y: 0,
                }}
                exit={{
                  opacity: 0,
                  y: -20,
                }}
                className="rounded-3xl border border-slate-200 bg-white p-6 shadow-xl shadow-slate-200/50 sm:p-8"
              >

                {/* Upload area */}
                <motion.div
                  animate={{
                    scale: dragging ? 1.01 : 1,
                  }}
                  onDragOver={(event) => {
                    event.preventDefault();
                    setDragging(true);
                  }}
                  onDragLeave={() => {
                    setDragging(false);
                  }}
                  onDrop={handleDrop}
                  onClick={() => {
                    if (!file && !loading) {
                      fileInputRef.current?.click();
                    }
                  }}
                  className={`relative flex min-h-[280px] cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 text-center transition ${
                    dragging
                      ? "border-indigo-500 bg-indigo-50"
                      : "border-slate-200 bg-slate-50 hover:border-indigo-300 hover:bg-indigo-50/40"
                  } ${
                    file
                      ? "cursor-default"
                      : ""
                  }`}
                >

                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,application/pdf"
                    className="hidden"
                    onChange={handleFileChange}
                  />

                  {!file ? (
                    <>
                      <motion.div
                        animate={{
                          y: [0, -5, 0],
                        }}
                        transition={{
                          duration: 2.5,
                          repeat: Infinity,
                          ease: "easeInOut",
                        }}
                        className="flex h-16 w-16 items-center justify-center rounded-2xl bg-white text-indigo-600 shadow-md ring-1 ring-slate-200"
                      >
                        <Upload size={26} />
                      </motion.div>

                      <h2 className="mt-6 text-lg font-bold text-slate-900">
                        Drag & drop your resume
                      </h2>

                      <p className="mt-2 text-sm text-slate-500">
                        or click to browse from your computer
                      </p>

                      <div className="mt-5 flex items-center gap-2 text-xs text-slate-400">
                        <span className="rounded-md bg-white px-2.5 py-1 ring-1 ring-slate-200">
                          PDF
                        </span>

                        <span>•</span>

                        <span>Maximum 10 MB</span>
                      </div>
                    </>
                  ) : (
                    <SelectedFile
                      file={file}
                      onRemove={removeFile}
                      loading={loading}
                    />
                  )}

                </motion.div>

                {/* Error */}
                <AnimatePresence>
                  {error && (
                    <motion.div
                      initial={{
                        opacity: 0,
                        y: -5,
                      }}
                      animate={{
                        opacity: 1,
                        y: 0,
                      }}
                      exit={{
                        opacity: 0,
                      }}
                      className="mt-4 flex items-start gap-3 rounded-xl border border-red-100 bg-red-50 p-4 text-sm text-red-700"
                    >
                      <X
                        size={17}
                        className="mt-0.5 shrink-0"
                      />

                      <span>{error}</span>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Success */}
                <AnimatePresence>
                  {message && (
                    <motion.div
                      initial={{
                        opacity: 0,
                        y: -5,
                      }}
                      animate={{
                        opacity: 1,
                        y: 0,
                      }}
                      exit={{
                        opacity: 0,
                      }}
                      className="mt-4 flex items-start gap-3 rounded-xl border border-emerald-100 bg-emerald-50 p-4 text-sm text-emerald-700"
                    >
                      <CheckCircle2
                        size={17}
                        className="mt-0.5 shrink-0"
                      />

                      <span>{message}</span>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Upload button */}
                <button
                  onClick={handleUpload}
                  disabled={!file || loading}
                  className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none"
                >

                  {loading ? (
                    <>
                      <Loader2
                        size={18}
                        className="animate-spin"
                      />

                      Analyzing Resume...
                    </>
                  ) : (
                    <>
                      <Sparkles size={18} />

                      Analyze Resume
                    </>
                  )}

                </button>

                {/* Privacy */}
                <p className="mt-5 text-center text-xs text-slate-400">
                  Your resume is used to build your personalized
                  JobLens profile and improve job matching.
                </p>

              </motion.div>
            ) : (
              <ProfileResult
                result={result}
                onSearchJobs={() => navigate("/jobs")}
                onViewProfile={() => navigate("/profile")}
              />
            )}

          </AnimatePresence>

        </div>

      </div>
    </div>
  );
}


/* =========================================================
   SELECTED FILE
========================================================= */

function SelectedFile({
  file,
  onRemove,
  loading,
}) {
  const fileSize =
    file.size / (1024 * 1024);

  return (
    <div className="w-full max-w-lg">

      <div className="flex items-center gap-4 rounded-2xl border border-indigo-100 bg-white p-4 shadow-sm">

        <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
          <FileText size={23} />
        </div>

        <div className="min-w-0 flex-1 text-left">

          <p className="truncate text-sm font-semibold text-slate-900">
            {file.name}
          </p>

          <p className="mt-1 text-xs text-slate-400">
            {fileSize.toFixed(2)} MB · PDF
          </p>

        </div>

        {!loading && (
          <button
            onClick={(event) => {
              event.stopPropagation();
              onRemove();
            }}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-slate-400 transition hover:bg-red-50 hover:text-red-500"
          >
            <Trash2 size={17} />
          </button>
        )}

      </div>

      {loading && (
        <div className="mt-5">

          <div className="mb-2 flex justify-between text-xs">
            <span className="font-medium text-slate-600">
              Analyzing your resume...
            </span>

            <span className="text-indigo-600">
              AI
            </span>
          </div>

          <div className="h-2 overflow-hidden rounded-full bg-slate-100">

            <motion.div
              initial={{
                width: "0%",
              }}
              animate={{
                width: "95%",
              }}
              transition={{
                duration: 8,
                ease: "easeOut",
              }}
              className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-violet-500"
            />

          </div>

        </div>
      )}

    </div>
  );
}


/* =========================================================
   PROFILE RESULT
========================================================= */

function ProfileResult({
  result,
  onSearchJobs,
  onViewProfile
}) {
  const skills =
    result.skills ||
    result.profile?.skills ||
    [];

  return (
    <motion.div
      initial={{
        opacity: 0,
        scale: 0.98,
      }}
      animate={{
        opacity: 1,
        scale: 1,
      }}
      className="rounded-3xl border border-slate-200 bg-white p-6 shadow-xl shadow-slate-200/50 sm:p-8"
    >

      {/* Success */}
      <div className="text-center">

        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-50 text-emerald-600">
          <CheckCircle2 size={28} />
        </div>

        <h2 className="mt-5 text-2xl font-bold text-slate-950">
          Resume analyzed successfully
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          Your JobLens profile is ready.
        </p>

      </div>

      {/* Resume information */}
      <div className="mt-8 grid gap-4 sm:grid-cols-3">

        <InfoBox
          label="Resume ID"
          value={
            result.resume_id ??
            "Created"
          }
        />

        <InfoBox
          label="Profile ID"
          value={
            result.profile_id ??
            "Created"
          }
        />

        <InfoBox
          label="Version"
          value={
            result.version ??
            "1"
          }
        />

      </div>

      {/* Skills */}
      {skills.length > 0 && (
        <div className="mt-8">

          <div className="flex items-center justify-between">

            <div>
              <h3 className="font-bold text-slate-900">
                Detected Skills
              </h3>

              <p className="mt-1 text-xs text-slate-400">
                Skills extracted from your resume
              </p>
            </div>

            <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-600">
              {skills.length} skills
            </span>

          </div>

          <div className="mt-4 flex flex-wrap gap-2">

            {skills.map((skill, index) => (
              <motion.span
                key={`${skill}-${index}`}
                initial={{
                  opacity: 0,
                  scale: 0.9,
                }}
                animate={{
                  opacity: 1,
                  scale: 1,
                }}
                transition={{
                  delay: index * 0.03,
                }}
                className="rounded-lg border border-indigo-100 bg-indigo-50 px-3 py-1.5 text-xs font-medium text-indigo-700"
              >
                {skill}
              </motion.span>
            ))}

          </div>

        </div>
      )}

      {/* CTA */}
      <div className="mt-9 grid gap-3 border-t border-slate-100 pt-7 sm:grid-cols-2">

        <button
            onClick={onViewProfile}
            className="flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3.5 text-sm font-semibold text-slate-700 transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700"
        >
            <UserRound size={17} />

            View My Profile
        </button>

        <button
            onClick={onSearchJobs}
            className="flex items-center justify-center gap-2 rounded-xl bg-slate-950 px-5 py-3.5 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-slate-800"
        >
            <Sparkles size={17} />

            Find Jobs for Me

            <ArrowRightIcon />
        </button>

        </div>

    </motion.div>
  );
}


/* =========================================================
   INFO BOX
========================================================= */

function InfoBox({
  label,
  value,
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">

      <p className="text-xs font-medium text-slate-400">
        {label}
      </p>

      <p className="mt-2 truncate text-sm font-bold text-slate-900">
        {value}
      </p>

    </div>
  );
}

export default Resume;