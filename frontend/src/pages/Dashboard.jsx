import { motion } from "framer-motion";
import {
  ArrowRight,
  BriefcaseBusiness,
  CheckCircle2,
  FileText,
  Search,
  Sparkles,
  Target,
  TrendingUp,
  Upload,
  Zap,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  const stats = [
    {
      label: "Jobs Discovered",
      value: "128",
      icon: BriefcaseBusiness,
      description: "Across multiple sources",
    },
    {
      label: "Average Match",
      value: "82%",
      icon: Target,
      description: "Based on your profile",
    },
    {
      label: "Skills Matched",
      value: "14",
      icon: CheckCircle2,
      description: "From your resume",
    },
  ];

  const features = [
    {
      icon: Sparkles,
      title: "AI Profile Intelligence",
      description:
        "JobLens understands your skills, projects, experience and career preferences from your resume.",
    },
    {
      icon: Search,
      title: "Multi-Source Discovery",
      description:
        "Discover relevant opportunities from job platforms, ATS systems and company career pages.",
    },
    {
      icon: Target,
      title: "Resume-Based Matching",
      description:
        "Every job is evaluated against your skills and preferred roles to find better opportunities.",
    },
  ];

  const steps = [
    {
      number: "01",
      icon: Upload,
      title: "Upload Resume",
      description:
        "Upload your latest resume and let JobLens extract your professional profile.",
    },
    {
      number: "02",
      icon: Sparkles,
      title: "AI Understands You",
      description:
        "Your skills, roles, projects and preferences are converted into a searchable profile.",
    },
    {
      number: "03",
      icon: BriefcaseBusiness,
      title: "Discover Better Jobs",
      description:
        "Search across multiple sources and get jobs ranked according to your profile.",
    },
  ];

  return (
    <div className="min-h-screen overflow-hidden bg-slate-50 text-slate-900">

      {/* =====================================================
          BACKGROUND
      ====================================================== */}

      <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">

        <div className="absolute left-[10%] top-[-200px] h-[500px] w-[500px] rounded-full bg-indigo-200/30 blur-[120px]" />

        <div className="absolute right-[-100px] top-[20%] h-[450px] w-[450px] rounded-full bg-violet-200/25 blur-[120px]" />

        <div className="absolute bottom-[-200px] left-[30%] h-[450px] w-[450px] rounded-full bg-cyan-200/20 blur-[120px]" />

      </div>

      {/* =====================================================
          HERO
      ====================================================== */}

      <main>

        <section className="relative">

          <div className="mx-auto max-w-7xl px-5 pb-20 pt-16 sm:px-6 lg:px-8 lg:pb-28 lg:pt-24">

            <div className="grid items-center gap-14 lg:grid-cols-[1.05fr_0.95fr]">

              {/* LEFT */}
              <div>

                {/* Badge */}
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
                  className="mb-7 inline-flex items-center gap-2 rounded-full border border-indigo-200 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700"
                >
                  <Sparkles size={15} />

                  AI-Powered Job Discovery

                  <span className="h-1.5 w-1.5 rounded-full bg-indigo-500" />
                </motion.div>

                {/* Heading */}
                <motion.h1
                  initial={{
                    opacity: 0,
                    y: 25,
                  }}
                  animate={{
                    opacity: 1,
                    y: 0,
                  }}
                  transition={{
                    duration: 0.6,
                    delay: 0.1,
                  }}
                  className="max-w-3xl text-5xl font-bold leading-[1.05] tracking-tight text-slate-950 sm:text-6xl lg:text-7xl"
                >
                  Find jobs that

                  <span className="block bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-500 bg-clip-text text-transparent">
                    actually fit you.
                  </span>
                </motion.h1>

                {/* Description */}
                <motion.p
                  initial={{
                    opacity: 0,
                    y: 20,
                  }}
                  animate={{
                    opacity: 1,
                    y: 0,
                  }}
                  transition={{
                    duration: 0.6,
                    delay: 0.2,
                  }}
                  className="mt-7 max-w-2xl text-base leading-7 text-slate-500 sm:text-lg"
                >
                  JobLens AI analyzes your resume, understands your
                  technical profile and discovers relevant jobs from
                  multiple sources — so you spend less time searching
                  and more time applying.
                </motion.p>

                {/* Buttons */}
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
                    duration: 0.6,
                    delay: 0.3,
                  }}
                  className="mt-9 flex flex-col gap-3 sm:flex-row"
                >

                  <motion.button
                    whileHover={{
                      y: -2,
                    }}
                    whileTap={{
                      scale: 0.98,
                    }}
                    onClick={() => navigate("/resume")}
                    className="group flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition hover:bg-indigo-700"
                  >
                    <FileText size={18} />

                    Upload Resume

                    <ArrowRight
                      size={17}
                      className="transition-transform duration-200 group-hover:translate-x-1"
                    />
                  </motion.button>

                  <motion.button
                    whileHover={{
                      y: -2,
                    }}
                    whileTap={{
                      scale: 0.98,
                    }}
                    onClick={() => navigate("/jobs")}
                    className="group flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-6 py-3.5 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700"
                  >
                    <Search size={18} />

                    Explore Jobs
                  </motion.button>

                </motion.div>

                {/* Trust line */}
                <motion.div
                  initial={{
                    opacity: 0,
                  }}
                  animate={{
                    opacity: 1,
                  }}
                  transition={{
                    duration: 0.6,
                    delay: 0.5,
                  }}
                  className="mt-7 flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-slate-400"
                >

                  <span className="flex items-center gap-2">
                    <CheckCircle2
                      size={15}
                      className="text-emerald-500"
                    />
                    Resume-based matching
                  </span>

                  <span className="flex items-center gap-2">
                    <CheckCircle2
                      size={15}
                      className="text-emerald-500"
                    />
                    Multiple job sources
                  </span>

                </motion.div>

              </div>

              {/* RIGHT - PRODUCT PREVIEW */}
              <motion.div
                initial={{
                  opacity: 0,
                  x: 40,
                }}
                animate={{
                  opacity: 1,
                  x: 0,
                }}
                transition={{
                  duration: 0.8,
                  delay: 0.2,
                }}
                className="relative"
              >

                {/* Floating badge */}
                <motion.div
                  animate={{
                    y: [0, -8, 0],
                  }}
                  transition={{
                    duration: 4,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  className="absolute -right-3 -top-5 z-20 hidden rounded-xl border border-emerald-100 bg-white px-4 py-3 shadow-xl shadow-slate-200/50 sm:block"
                >

                  <div className="flex items-center gap-2">

                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-50">
                      <TrendingUp
                        size={16}
                        className="text-emerald-600"
                      />
                    </div>

                    <div>
                      <p className="text-xs text-slate-400">
                        Match quality
                      </p>

                      <p className="text-sm font-bold text-emerald-600">
                        Excellent
                      </p>
                    </div>

                  </div>

                </motion.div>

                {/* Main preview */}
                <div className="rounded-3xl border border-slate-200 bg-white p-3 shadow-2xl shadow-slate-200/70">

                  <div className="rounded-2xl bg-slate-950 p-5 sm:p-6">

                    {/* Preview top bar */}
                    <div className="mb-6 flex items-center justify-between">

                      <div className="flex items-center gap-2">

                        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600">
                          <Sparkles
                            size={15}
                            className="text-white"
                          />
                        </div>

                        <span className="text-sm font-semibold text-white">
                          JobLens AI
                        </span>

                      </div>

                      <div className="flex items-center gap-1.5">

                        <div className="h-2 w-2 rounded-full bg-emerald-400" />

                        <span className="text-xs text-slate-400">
                          AI Ready
                        </span>

                      </div>

                    </div>

                    {/* Search */}
                    <div className="mb-5 rounded-xl border border-white/10 bg-white/5 p-3">

                      <div className="flex items-center gap-3">

                        <Search
                          size={17}
                          className="text-slate-500"
                        />

                        <span className="text-sm text-slate-300">
                          AI Engineer · Bangalore
                        </span>

                      </div>

                    </div>

                    {/* Stats */}
                    <div className="grid grid-cols-3 gap-3">

                      <PreviewStat
                        value="128"
                        label="Jobs"
                      />

                      <PreviewStat
                        value="82%"
                        label="Avg Match"
                      />

                      <PreviewStat
                        value="14"
                        label="Skills"
                      />

                    </div>

                    {/* Job result */}
                    <div className="mt-4 rounded-xl border border-white/10 bg-white/[0.04] p-4">

                      <div className="flex items-start justify-between gap-3">

                        <div>

                          <p className="text-sm font-semibold text-white">
                            AI Engineer
                          </p>

                          <p className="mt-1 text-xs text-slate-500">
                            Technology Company
                          </p>

                          <p className="mt-2 text-xs text-slate-500">
                            Bengaluru · Full-time
                          </p>

                        </div>

                        <div className="flex h-12 w-12 items-center justify-center rounded-full border-4 border-indigo-500/30 text-xs font-bold text-indigo-300">
                          87%
                        </div>

                      </div>

                      <div className="mt-4 flex flex-wrap gap-1.5">

                        {[
                          "Python",
                          "FastAPI",
                          "React",
                          "SQL",
                        ].map((skill) => (
                          <span
                            key={skill}
                            className="rounded-md bg-indigo-500/10 px-2 py-1 text-[10px] font-medium text-indigo-300"
                          >
                            {skill}
                          </span>
                        ))}

                      </div>

                    </div>

                  </div>

                </div>

              </motion.div>

            </div>

          </div>

        </section>

        {/* =====================================================
            STATS
        ====================================================== */}

        <section className="border-y border-slate-200 bg-white">

          <div className="mx-auto grid max-w-7xl grid-cols-1 divide-y divide-slate-200 px-5 sm:grid-cols-3 sm:divide-x sm:divide-y-0 sm:px-6 lg:px-8">

            {stats.map((stat, index) => {

              const Icon = stat.icon;

              return (
                <motion.div
                  key={stat.label}
                  initial={{
                    opacity: 0,
                    y: 20,
                  }}
                  whileInView={{
                    opacity: 1,
                    y: 0,
                  }}
                  viewport={{
                    once: true,
                  }}
                  transition={{
                    duration: 0.5,
                    delay: index * 0.1,
                  }}
                  className="flex items-center gap-4 px-6 py-7 sm:justify-center"
                >

                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                    <Icon size={20} />
                  </div>

                  <div>
                    <p className="text-2xl font-bold text-slate-900">
                      {stat.value}
                    </p>

                    <p className="text-sm font-medium text-slate-700">
                      {stat.label}
                    </p>

                    <p className="mt-0.5 text-xs text-slate-400">
                      {stat.description}
                    </p>
                  </div>

                </motion.div>
              );
            })}

          </div>

        </section>

        {/* =====================================================
            FEATURES
        ====================================================== */}

        <section className="bg-slate-50 py-24">

          <div className="mx-auto max-w-7xl px-5 sm:px-6 lg:px-8">

            <motion.div
              initial={{
                opacity: 0,
                y: 20,
              }}
              whileInView={{
                opacity: 1,
                y: 0,
              }}
              viewport={{
                once: true,
              }}
                className="mx-auto max-w-2xl text-center"
            >

              <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-indigo-50 px-3 py-1.5 text-xs font-semibold uppercase tracking-wider text-indigo-600">
                <Zap size={13} />
                Built for smarter job search
              </div>

              <h2 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                Your resume becomes your
                <span className="text-indigo-600">
                  {" "}job-search engine.
                </span>
              </h2>

              <p className="mt-4 text-slate-500">
                Instead of searching hundreds of jobs manually,
                let JobLens understand what makes you a good fit.
              </p>

            </motion.div>

            <div className="mt-14 grid gap-6 md:grid-cols-3">

              {features.map((feature, index) => {

                const Icon = feature.icon;

                return (
                  <motion.div
                    key={feature.title}
                    initial={{
                      opacity: 0,
                      y: 30,
                    }}
                    whileInView={{
                      opacity: 1,
                      y: 0,
                    }}
                    viewport={{
                      once: true,
                    }}
                    transition={{
                      duration: 0.5,
                      delay: index * 0.12,
                    }}
                    whileHover={{
                      y: -7,
                    }}
                    className="group rounded-2xl border border-slate-200 bg-white p-7 shadow-sm transition-shadow hover:border-indigo-200 hover:shadow-xl hover:shadow-indigo-100/40"
                  >

                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600 transition group-hover:bg-indigo-600 group-hover:text-white">
                      <Icon size={22} />
                    </div>

                    <h3 className="mt-6 text-lg font-bold text-slate-900">
                      {feature.title}
                    </h3>

                    <p className="mt-3 text-sm leading-6 text-slate-500">
                      {feature.description}
                    </p>

                    <div className="mt-6 flex items-center gap-1 text-sm font-semibold text-indigo-600 opacity-0 transition group-hover:opacity-100">
                      Learn more
                      <ArrowRight size={15} />
                    </div>

                  </motion.div>
                );

              })}

            </div>

          </div>

        </section>

        {/* =====================================================
            HOW IT WORKS
        ====================================================== */}

        <section className="bg-white py-24">

          <div className="mx-auto max-w-7xl px-5 sm:px-6 lg:px-8">

            <div className="grid gap-14 lg:grid-cols-[0.8fr_1.2fr] lg:items-center">

              {/* Left */}
              <motion.div
                initial={{
                  opacity: 0,
                  x: -25,
                }}
                whileInView={{
                  opacity: 1,
                  x: 0,
                }}
                viewport={{
                  once: true,
                }}
              >

                <p className="text-sm font-semibold uppercase tracking-wider text-indigo-600">
                  Simple workflow
                </p>

                <h2 className="mt-3 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                  From resume to
                  <span className="text-indigo-600">
                    {" "}better opportunities.
                  </span>
                </h2>

                <p className="mt-5 max-w-lg leading-7 text-slate-500">
                  JobLens handles the difficult part of job
                  discovery so you can focus on preparing and
                  applying.
                </p>

                <button
                  onClick={() => navigate("/resume")}
                  className="mt-8 flex items-center gap-2 rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
                >
                  Start with your resume
                  <ArrowRight size={16} />
                </button>

              </motion.div>

              {/* Right */}
              <div className="space-y-4">

                {steps.map((step, index) => {

                  const Icon = step.icon;

                  return (
                    <motion.div
                      key={step.number}
                      initial={{
                        opacity: 0,
                        x: 25,
                      }}
                      whileInView={{
                        opacity: 1,
                        x: 0,
                      }}
                      viewport={{
                        once: true,
                      }}
                      transition={{
                        duration: 0.5,
                        delay: index * 0.12,
                      }}
                      className="group flex gap-5 rounded-2xl border border-slate-200 bg-slate-50 p-5 transition hover:border-indigo-200 hover:bg-indigo-50/40"
                    >

                      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-white text-indigo-600 shadow-sm ring-1 ring-slate-200 group-hover:bg-indigo-600 group-hover:text-white group-hover:ring-indigo-600">
                        <Icon size={20} />
                      </div>

                      <div className="flex-1">

                        <div className="flex items-center gap-3">

                          <span className="text-xs font-bold tracking-widest text-indigo-500">
                            {step.number}
                          </span>

                          <h3 className="font-bold text-slate-900">
                            {step.title}
                          </h3>

                        </div>

                        <p className="mt-2 text-sm leading-6 text-slate-500">
                          {step.description}
                        </p>

                      </div>

                    </motion.div>
                  );

                })}

              </div>

            </div>

          </div>

        </section>

        {/* =====================================================
            CTA
        ====================================================== */}

        <section className="px-5 pb-20 sm:px-6 lg:px-8">

          <motion.div
            initial={{
              opacity: 0,
              y: 30,
            }}
            whileInView={{
              opacity: 1,
              y: 0,
            }}
            viewport={{
              once: true,
            }}
            className="mx-auto max-w-7xl overflow-hidden rounded-3xl bg-slate-950 px-7 py-14 text-center shadow-2xl shadow-slate-300/30 sm:px-12"
          >

            <div className="mx-auto max-w-2xl">

              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-600 shadow-lg shadow-indigo-600/30">
                <Sparkles
                  size={21}
                  className="text-white"
                />
              </div>

              <h2 className="mt-6 text-3xl font-bold text-white sm:text-4xl">
                Ready to find your next opportunity?
              </h2>

              <p className="mt-4 leading-7 text-slate-400">
                Upload your resume and let JobLens AI discover
                opportunities tailored to your profile.
              </p>

              <button
                onClick={() => navigate("/resume")}
                className="mt-8 inline-flex items-center gap-2 rounded-xl bg-white px-6 py-3.5 text-sm font-semibold text-slate-950 transition hover:-translate-y-1 hover:bg-slate-100"
              >
                Upload Resume
                <ArrowRight size={17} />
              </button>

            </div>

          </motion.div>

        </section>

      </main>

    </div>
  );
}


/* =========================================================
   PREVIEW STAT
========================================================= */

function PreviewStat({ value, label }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/[0.04] p-3">
      <p className="text-lg font-bold text-white">
        {value}
      </p>

      <p className="mt-0.5 text-[10px] text-slate-500">
        {label}
      </p>
    </div>
  );
}

export default Dashboard;