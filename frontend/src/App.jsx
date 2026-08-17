import { useEffect, useState } from "react";
import "./App.css";

const API = "https://skillgraph-api-k78k.onrender.com";

function App() {
  const [developers, setDevelopers] = useState([]);
  const [selected, setSelected] = useState("");
  const [developer, setDeveloper] = useState(null);
  const [connections, setConnections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/developers`)
      .then((res) => res.json())
      .then(setDevelopers)
      .catch(() => setError("Unable to connect to SkillGraph"));
  }, []);

  const loadDeveloper = async (name) => {
    setSelected(name);
    setDeveloper(null);
    setConnections([]);
    setError("");
    setLoading(true);

    try {
      const [devRes, connRes] = await Promise.all([
        fetch(`${API}/developer/${name}`),
        fetch(`${API}/developer/${name}/connections`)
      ]);

      if (!devRes.ok || !connRes.ok) {
        throw new Error();
      }

      const devData = await devRes.json();
      const connData = await connRes.json();

      setDeveloper(devData);
      setConnections(connData);
    } catch {
      setError("Something went wrong while loading the developer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <div>
          <h1>SkillGraph</h1>
          <p>Explore developer skills, projects and technology connections.</p>
        </div>
        <span className="badge">GRAPH EXPLORER</span>
      </header>

      <main>
        <section className="selector">
          <label>Select a developer</label>

          <select
            value={selected}
            onChange={(e) => loadDeveloper(e.target.value)}
          >
            <option value="">Choose a developer...</option>

            {developers.map((dev) => (
              <option key={dev.name} value={dev.name}>
                {dev.name} — {dev.role}
              </option>
            ))}
          </select>
        </section>

        {error && <div className="error">{error}</div>}

        {loading && (
          <div className="loading">
            Loading graph connections...
          </div>
        )}

        {!loading && developer && (
          <>
            <section className="profile">
              <div className="avatar">
                {developer.name.charAt(0)}
              </div>

              <div>
                <h2>{developer.name}</h2>
                <p>{developer.role}</p>
              </div>
            </section>

            <section className="grid">
              <div className="card">
                <h3>Skills</h3>

                <div className="tags">
                  {developer.skills.map((skill) => (
                    <span key={skill}>{skill}</span>
                  ))}
                </div>
              </div>

              <div className="card">
                <h3>Projects</h3>

                {developer.projects.map((project) => (
                  <div className="project" key={project.name}>
                    <strong>{project.name}</strong>
                    <p>{project.description}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="card connections">
              <h3>Technology Connections</h3>
              <p className="sub">
                Developer → Project → Technology
              </p>

              {connections.map((connection) => (
                <div className="connection" key={connection.project}>
                  <strong>{connection.project}</strong>

                  <span>→</span>

                  <div className="tags">
                    {connection.technologies.map((tech) => (
                      <span key={tech}>{tech}</span>
                    ))}
                  </div>
                </div>
              ))}
            </section>
          </>
        )}

        {!loading && !developer && !error && (
          <div className="empty">
            <div className="empty-icon">◎</div>
            <h2>Explore the developer graph</h2>
            <p>
              Select a developer above to discover connected skills,
              projects and technologies.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;