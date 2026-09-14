import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Award,
  BriefcaseBusiness,
  CheckCircle2,
  Code2,
  GraduationCap,
  MapPin,
  RefreshCw,
  Sparkles,
  UserRound,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Profile() {
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get(
        "/api/profile"
      );

      setProfile(response.data);

    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to load your profile."
      );

    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  if (loading) {
    return <ProfileLoading />;
  }

  if (error) {
    return (
      <div className="min-h-[calc(100vh-64px)] bg-slate-50 px-5 py-10">
        <div className="mx-auto max-w-xl rounded-2xl border border-red-100 bg-white p-8 text-center shadow-sm">

          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-red-50 text-red-500">
            <UserRound size={22} />
          </div>

          <h2 className="mt-5 text-lg font-bold text-slate-900">
            Profile unavailable
          </h2>

          <p className="mt-2 text-sm text-slate-500">
            {error}
          </p>

          <div className="mt-6 flex justify-center gap-3">

            <button
              onClick={fetchProfile}
              className="flex items-center gap-2 rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800"
            >
              <RefreshCw size={15} />
              Try Again
            </button>

            <button
              onClick={() => navigate("/resume")}
              className="rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
            >
              Upload Resume
            </button>

          </div>

        </div>
      </div>
    );
  }

  if (!profile) {
    return null;
  }

  const skills = profile.skills || [];
  const coreSkills = profile.core_skills || [];
  const supportingSkills = profile.supporting_skills || [];
  const roles = profile.preferred_roles || [];
  const locations = profile.preferred_locations || [];
  const workModes = profile.preferred_work_modes || [];
  const education = profile.education || [];
  const experience = profile.experience || [];
  const projects = profile.projects || [];
  const certifications = profile.certifications || [];

  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-50">

      {/* Background */}

      <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">

        <div className="absolute left-[10%] top-20 h-72 w-72 rounded-full bg-indigo-200/20 blur-[100px]" />

        <div className="absolute right-[5%] top-[40%] h-80 w-80 rounded-full bg-violet-200/20 blur-[110px]" />

      </div>


      <main className="mx-auto max-w-7xl px-5 py-8 sm:px-6 lg:px-8">

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
        >

          <div className="flex items-center gap-2 text-sm font-semibold text-indigo-600">
            <Sparkles size={16} />
            AI Profile
          </div>

          <div className="mt-2 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">

            <div>

              <h1 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                Your Professional Profile
              </h1>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
                JobLens created this profile from your resume to
                personalize job discovery and matching.
              </p>

            </div>

            <button
              onClick={() => navigate("/jobs")}
              className="flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition hover:bg-indigo-700"
            >
              <BriefcaseBusiness size={17} />
              Find Jobs
            </button>

          </div>

        </motion.div>


        {/* Profile summary */}

        <motion.section
          initial={{
            opacity: 0,
            y: 25,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            delay: 0.1,
          }}
          className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
        >

          <div className="flex flex-col gap-6 md:flex-row">

            <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
              <UserRound size={28} />
            </div>

            <div className="flex-1">

              <div className="flex flex-wrap items-center gap-3">

                <h2 className="text-xl font-bold text-slate-900">
                  Candidate Profile
                </h2>

                <span className="flex items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700">
                  <CheckCircle2 size={13} />
                  AI Analyzed
                </span>

              </div>

              <p className="mt-3 max-w-4xl text-sm leading-7 text-slate-500">
                {profile.summary ||
                  "Your resume profile has been analyzed and is ready for personalized job matching."}
              </p>

            </div>

          </div>

        </motion.section>


        {/* Main grid */}

        <div className="mt-6 grid gap-6 lg:grid-cols-3">

          {/* Skills */}

          <ProfileSection
            icon={Code2}
            title="Skills"
            delay={0.15}
            className="lg:col-span-2"
          >

            {coreSkills.length > 0 && (
              <SkillGroup
                title="Core Skills"
                skills={coreSkills}
              />
            )}

            {supportingSkills.length > 0 && (
              <SkillGroup
                title="Supporting Skills"
                skills={supportingSkills}
              />
            )}

            {coreSkills.length === 0 &&
              supportingSkills.length === 0 && (
                <SkillGroup
                  title="Detected Skills"
                  skills={skills}
                />
              )}

          </ProfileSection>


          {/* Experience level */}

          <ProfileSection
            icon={BriefcaseBusiness}
            title="Career Level"
            delay={0.2}
          >

            <div className="rounded-xl bg-indigo-50 p-5">

              <p className="text-xs font-medium uppercase tracking-wide text-indigo-500">
                Experience Level
              </p>

              <p className="mt-2 text-xl font-bold text-indigo-900">
                {profile.experience_level ||
                  "Not specified"}
              </p>

            </div>

          </ProfileSection>


          {/* Roles */}

          <ProfileSection
            icon={BriefcaseBusiness}
            title="Preferred Roles"
            delay={0.25}
          >

            <TagList
              items={roles}
              empty="No preferred roles detected."
            />

          </ProfileSection>


          {/* Locations */}

          <ProfileSection
            icon={MapPin}
            title="Preferred Locations"
            delay={0.3}
          >

            <TagList
              items={locations}
              empty="No preferred locations detected."
            />

          </ProfileSection>


          {/* Work modes */}

          <ProfileSection
            icon={Sparkles}
            title="Work Preferences"
            delay={0.35}
          >

            <TagList
              items={workModes}
              empty="No work mode preference detected."
            />

          </ProfileSection>


          {/* Education */}

          <ProfileSection
            icon={GraduationCap}
            title="Education"
            delay={0.4}
            className="lg:col-span-2"
          >

            {education.length > 0 ? (
              <div className="space-y-4">

                {education.map(
                  (item, index) => (
                    <EducationItem
                      key={index}
                      item={item}
                    />
                  )
                )}

              </div>
            ) : (
              <EmptyText text="No education information detected." />
            )}

          </ProfileSection>


          {/* Certifications */}

          <ProfileSection
            icon={Award}
            title="Certifications"
            delay={0.45}
          >

            {certifications.length > 0 ? (
              <div className="space-y-3">

                {certifications.map(
                  (item, index) => (
                    <div
                      key={index}
                      className="flex items-start gap-3 rounded-xl bg-slate-50 p-3"
                    >

                      <div className="mt-0.5 text-amber-500">
                        <Award size={17} />
                      </div>

                      <p className="text-sm font-medium text-slate-700">
                        {formatValue(item)}
                      </p>

                    </div>
                  )
                )}

              </div>
            ) : (
              <EmptyText text="No certifications detected." />
            )}

          </ProfileSection>


          {/* Experience */}

          <ProfileSection
            icon={BriefcaseBusiness}
            title="Experience"
            delay={0.5}
            className="lg:col-span-3"
          >

            {experience.length > 0 ? (
              <div className="grid gap-4 md:grid-cols-2">

                {experience.map(
                  (item, index) => (
                    <ExperienceItem
                      key={index}
                      item={item}
                    />
                  )
                )}

              </div>
            ) : (
              <EmptyText text="No professional experience detected." />
            )}

          </ProfileSection>


          {/* Projects */}

          <ProfileSection
            icon={Code2}
            title="Projects"
            delay={0.55}
            className="lg:col-span-3"
          >

            {projects.length > 0 ? (
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">

                {projects.map(
                  (item, index) => (
                    <ProjectItem
                      key={index}
                      item={item}
                    />
                  )
                )}

              </div>
            ) : (
              <EmptyText text="No projects detected." />
            )}

          </ProfileSection>

        </div>


        {/* Bottom CTA */}

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
          className="mt-8 rounded-2xl bg-slate-950 p-7 text-white sm:p-8"
        >

          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">

            <div>

              <div className="flex items-center gap-2 text-indigo-400">
                <Sparkles size={17} />
                Profile ready
              </div>

              <h2 className="mt-2 text-xl font-bold">
                Find jobs matched to your profile
              </h2>

              <p className="mt-2 text-sm text-slate-400">
                Use your AI profile to discover and rank relevant
                opportunities.
              </p>

            </div>

            <button
              onClick={() => navigate("/jobs")}
              className="flex shrink-0 items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-950 transition hover:-translate-y-0.5 hover:bg-slate-100"
            >
              Search Jobs
              <ArrowRightIcon />
            </button>

          </div>

        </motion.div>

      </main>

    </div>
  );
}


/* =========================================================
   SECTION
========================================================= */

function ProfileSection({
  icon: Icon,
  title,
  children,
  delay = 0,
  className = "",
}) {

  return (
    <motion.section
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
        delay,
      }}
      className={`rounded-2xl border border-slate-200 bg-white p-6 shadow-sm ${className}`}
    >

      <div className="mb-5 flex items-center gap-3">

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
          <Icon size={18} />
        </div>

        <h2 className="font-bold text-slate-900">
          {title}
        </h2>

      </div>

      {children}

    </motion.section>
  );
}


/* =========================================================
   SKILLS
========================================================= */

function SkillGroup({
  title,
  skills,
}) {

  if (!skills?.length) {
    return null;
  }

  return (
    <div className="mb-5 last:mb-0">

      <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400">
        {title}
      </p>

      <div className="flex flex-wrap gap-2">

        {skills.map(
          (skill, index) => (
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
                delay: index * 0.025,
              }}
              className="rounded-lg border border-indigo-100 bg-indigo-50 px-3 py-1.5 text-xs font-medium text-indigo-700"
            >
              {formatValue(skill)}
            </motion.span>
          )
        )}

      </div>

    </div>
  );
}


/* =========================================================
   TAG LIST
========================================================= */

function TagList({
  items,
  empty,
}) {

  if (!items?.length) {
    return <EmptyText text={empty} />;
  }

  return (
    <div className="flex flex-wrap gap-2">

      {items.map(
        (item, index) => (
          <span
            key={`${item}-${index}`}
            className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-700"
          >
            {formatValue(item)}
          </span>
        )
      )}

    </div>
  );
}


/* =========================================================
   EDUCATION
========================================================= */

function EducationItem({
  item,
}) {

  if (typeof item === "string") {
    return (
      <div className="rounded-xl bg-slate-50 p-4">
        <p className="text-sm font-medium text-slate-700">
          {item}
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">

      <p className="font-semibold text-slate-900">
        {item.degree ||
          item.qualification ||
          item.course ||
          "Education"}
      </p>

      {item.institution && (
        <p className="mt-1 text-sm text-slate-500">
          {item.institution}
        </p>
      )}

      {item.year && (
        <p className="mt-2 text-xs text-slate-400">
          {item.year}
        </p>
      )}

    </div>
  );
}


/* =========================================================
   EXPERIENCE
========================================================= */

function ExperienceItem({
  item,
}) {

  if (typeof item === "string") {
    return (
      <div className="rounded-xl bg-slate-50 p-4">
        <p className="text-sm leading-6 text-slate-600">
          {item}
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-slate-100 bg-slate-50 p-5">

      <h3 className="font-semibold text-slate-900">
        {item.role ||
          item.title ||
          "Experience"}
      </h3>

      {item.company && (
        <p className="mt-1 text-sm font-medium text-indigo-600">
          {item.company}
        </p>
      )}

      {item.duration && (
        <p className="mt-2 text-xs text-slate-400">
          {item.duration}
        </p>
      )}

      {item.description && (
        <p className="mt-3 text-sm leading-6 text-slate-500">
          {item.description}
        </p>
      )}

    </div>
  );
}


/* =========================================================
   PROJECT
========================================================= */

function ProjectItem({
  item,
}) {

  if (typeof item === "string") {
    return (
      <div className="rounded-xl border border-slate-100 bg-slate-50 p-5">

        <h3 className="font-semibold text-slate-900">
          {item}
        </h3>

      </div>
    );
  }

  return (
    <div className="rounded-xl border border-slate-100 bg-slate-50 p-5 transition hover:border-indigo-200 hover:bg-indigo-50/30">

      <h3 className="font-semibold text-slate-900">
        {item.name ||
          item.title ||
          "Project"}
      </h3>

      {item.description && (
        <p className="mt-2 text-sm leading-6 text-slate-500">
          {item.description}
        </p>
      )}

      {item.technologies && (
        <div className="mt-3 flex flex-wrap gap-1.5">

          {(Array.isArray(item.technologies)
            ? item.technologies
            : [item.technologies]
          ).map(
            (tech, index) => (
              <span
                key={index}
                className="rounded-md bg-white px-2 py-1 text-[10px] font-medium text-slate-500 ring-1 ring-slate-200"
              >
                {formatValue(tech)}
              </span>
            )
          )}

        </div>
      )}

    </div>
  );
}


/* =========================================================
   LOADING
========================================================= */

function ProfileLoading() {

  return (
    <div className="min-h-[calc(100vh-64px)] bg-slate-50 px-5 py-10">

      <div className="mx-auto max-w-7xl animate-pulse">

        <div className="h-4 w-24 rounded bg-slate-200" />

        <div className="mt-4 h-10 w-80 rounded bg-slate-200" />

        <div className="mt-8 h-36 rounded-2xl bg-white" />

        <div className="mt-6 grid gap-6 lg:grid-cols-3">

          {[1, 2, 3, 4, 5, 6].map(
            (item) => (
              <div
                key={item}
                className="h-48 rounded-2xl bg-white"
              />
            )
          )}

        </div>

      </div>

    </div>
  );
}


/* =========================================================
   EMPTY
========================================================= */

function EmptyText({
  text,
}) {

  return (
    <p className="text-sm text-slate-400">
      {text}
    </p>
  );
}


/* =========================================================
   FORMAT
========================================================= */

function formatValue(value) {

  if (
    value === null ||
    value === undefined
  ) {
    return "";
  }

  if (typeof value === "string") {
    return value;
  }

  if (typeof value === "number") {
    return String(value);
  }

  if (typeof value === "object") {

    return (
      value.name ||
      value.title ||
      value.degree ||
      value.role ||
      value.value ||
      JSON.stringify(value)
    );
  }

  return String(value);
}


/* =========================================================
   ARROW
========================================================= */

function ArrowRightIcon() {

  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
    >
      <path d="M5 12h14" />
      <path d="m13 6 6 6-6 6" />
    </svg>
  );
}


export default Profile;