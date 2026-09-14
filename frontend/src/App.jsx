import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Resume from "./pages/Resume";
import Jobs from "./pages/Jobs";
import Layout from "./components/Layout";
import Profile from "./pages/Profile";
import JobDetails from "./pages/JobDetails";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>

          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/resume"
            element={<Resume />}
          />

          <Route
            path="/profile"
            element={<Profile />}
          />

          <Route
            path="/jobs"
            element={<Jobs />}
          />

          <Route
            path="/jobs/:jobId"
            element={<JobDetails />}
          />

          

        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;