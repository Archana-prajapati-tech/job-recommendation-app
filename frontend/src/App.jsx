import { useState } from "react";
import "./App.css";

function App() {
  const [skills, setSkills] = useState("");
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchJobs = async () => {
    if (!skills.trim()) {
      setError("Please enter skills");
      return;
    }

    setLoading(true);
    setError("");
    setJobs([]);

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/get_jobs?skills=${skills}`
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setJobs(data);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  return (
    <div className="container">
     <h1 className="main-heading"> Smart Job Finder</h1>
<p className="sub-heading">Find jobs based on your skills instantly</p>

      <div className="search-box">
        <input
          type="text"
          placeholder="Enter skills (java, react, sql)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
        />
        <button onClick={fetchJobs}>Search</button>
      </div>

      {loading && <p className="loading">Loading jobs...</p>}
      {error && <p className="error">{error}</p>}

      <div className="jobs">
        {jobs.length > 0 ? (
          jobs.map((job) => (
            <div key={job.id} className="job-card">
              <h3>{job.title}</h3>
              <p><b>Company:</b> {job.company}</p>
              <p><b>Match Score:</b> {job.score}</p>
              <a href={job.link} target="_blank" rel="noreferrer">
                Apply Now →
              </a>
            </div>
          ))
        ) : (
          !loading && <p>No jobs found</p>
        )}
      </div>
    </div>
  );
}

export default App;