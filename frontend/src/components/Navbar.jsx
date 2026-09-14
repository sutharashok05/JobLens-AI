import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  BriefcaseBusiness,
  FileText,
  LayoutDashboard,
  Menu,
  Search,
  UserRound,
  X,
  Sparkles,
} from "lucide-react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";

function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const links = [
    {
      name: "Dashboard",
      path: "/",
      icon: LayoutDashboard,
    },
    {
      name: "Resume",
      path: "/resume",
      icon: FileText,
    },
    {
      name: "Profile",
      path: "/profile",
      icon: UserRound,
    },
    {
      name: "Find Jobs",
      path: "/jobs",
      icon: Search,
    },
  ];

  const closeMobile = () => setMobileOpen(false);

  const isJobsPage = location.pathname.startsWith("/jobs");

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/90 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 sm:px-6 lg:px-8">

        {/* Logo */}
        <button
          type="button"
          onClick={() => {
            closeMobile();
            navigate("/");
          }}
          className="group flex items-center gap-2.5"
        >
          <motion.div
            whileHover={{ rotate: -4, scale: 1.04 }}
            whileTap={{ scale: 0.96 }}
            className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-600 via-violet-600 to-cyan-500 text-white shadow-md shadow-indigo-500/20"
          >
            <BriefcaseBusiness size={18} />
          </motion.div>

          <div className="text-left">
            <div className="text-[15px] font-bold tracking-tight text-slate-950">
              JobLens <span className="text-indigo-600">AI</span>
            </div>
            <div className="hidden text-[9px] font-medium uppercase tracking-[0.18em] text-slate-400 sm:block">
              Intelligent Job Discovery
            </div>
          </div>
        </button>

        {/* Desktop Navigation */}
        <nav className="hidden items-center gap-1 md:flex">
          {links.map((link) => {
            const Icon = link.icon;

            return (
              <NavLink
                key={link.path}
                to={link.path}
                className={({ isActive }) =>
                  `relative flex items-center gap-2 rounded-lg px-3.5 py-2 text-sm font-medium transition ${
                    isActive
                      ? "bg-indigo-50 text-indigo-700"
                      : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon size={16} />
                    {link.name}

                    {isActive && (
                      <motion.span
                        layoutId="navbar-active"
                        className="absolute inset-x-3 -bottom-[1px] h-0.5 rounded-full bg-indigo-600"
                      />
                    )}
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* Desktop CTA */}
        <div className="hidden md:block">
          <motion.button
            type="button"
            whileHover={{ y: -1 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => navigate("/jobs")}
            className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold shadow-sm transition ${
              isJobsPage
                ? "bg-slate-950 text-white"
                : "bg-indigo-600 text-white shadow-indigo-600/20 hover:bg-indigo-700"
            }`}
          >
            <Search size={16} />
            Find Jobs
          </motion.button>
        </div>

        {/* Mobile Menu Button */}
        <button
          type="button"
          aria-label={mobileOpen ? "Close navigation" : "Open navigation"}
          aria-expanded={mobileOpen}
          onClick={() => setMobileOpen((value) => !value)}
          className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 transition hover:bg-slate-50 md:hidden"
        >
          {mobileOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Mobile Navigation */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden border-t border-slate-100 bg-white md:hidden"
          >
            <motion.nav
              initial={{ y: -8 }}
              animate={{ y: 0 }}
              exit={{ y: -8 }}
              className="mx-auto max-w-7xl px-5 py-4 sm:px-6"
            >
              <div className="space-y-1">
                {links.map((link) => {
                  const Icon = link.icon;

                  return (
                    <NavLink
                      key={link.path}
                      to={link.path}
                      onClick={closeMobile}
                      className={({ isActive }) =>
                        `flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                          isActive
                            ? "bg-indigo-50 text-indigo-700"
                            : "text-slate-600 hover:bg-slate-50 hover:text-slate-950"
                        }`
                      }
                    >
                      <Icon size={18} />
                      {link.name}
                    </NavLink>
                  );
                })}
              </div>

              <div className="mt-4 border-t border-slate-100 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    closeMobile();
                    navigate("/jobs");
                  }}
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/15 transition hover:bg-indigo-700"
                >
                  <Sparkles size={16} />
                  Find Jobs with AI
                </button>
              </div>
            </motion.nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}

export default Navbar;
