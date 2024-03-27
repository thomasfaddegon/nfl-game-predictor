import { useState } from "react";
import "./App.css";
import { nflTeams } from "../utils.ts";

function App() {
  const [teams, setTeams] = useState({ awayTeam: "", homeTeam: "" });
  const [result, setResult] = useState([]);
  const [error, setError] = useState("");

  let awayScore, homeScore;
  if (result && teams.homeTeam === result[0]) {
    awayScore = Math.min(...result);
    homeScore = Math.max(...result);
  } else {
    awayScore = Math.max(...result);
    homeScore = Math.min(...result);
  }

  const handleTeamChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = event.target;
    setTeams((prevTeams) => ({
      ...prevTeams,
      [name]: value,
    }));
  };

  const errorCheck = () => {
    if (
      !teams.awayTeam ||
      !teams.homeTeam ||
      teams.awayTeam === "Select a Team" ||
      teams.homeTeam === "Select a Team"
    ) {
      setError("Please select two teams");
      return true;
    }
    if (teams.awayTeam === teams.homeTeam) {
      setError("Please select different teams");
      return true;
    }
    setError("");
    return false;
  };

  const handleSubmit = () => {
    if (errorCheck()) return;
    console.log("teams:", teams);
    console.log("fetching results");
    fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(teams),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        setResult(data.predictions);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className="flex flex-col items-center">
      <h1 className="mb-8">NFL Game Predictor</h1>
      <div className="flex max-w-sm gap-8 justify-between flex-row">
        <div>
          <select
            id="homeTeamsDropdown"
            name="homeTeam"
            onChange={handleTeamChange}
          >
            <option>Select a Team</option>
            {nflTeams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>

        <div>
          <select
            id="homeTeamsDropdown"
            name="awayTeam"
            onChange={handleTeamChange}
          >
            <option>Select a Team</option>
            {nflTeams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>
      </div>
      {error && <p className="text-red-500">{error}</p>}
      <div className="flex flex-col gap-5">
        <button
          onClick={handleSubmit}
          className="mt-8 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Predict
        </button>
      </div>
      {result && (
        <h3 className="mt-8">
          <div>
            {teams.awayTeam}: {awayScore}
          </div>
          <div>
            {teams.homeTeam}: {homeScore}
          </div>
          {result[0]} wins!
        </h3>
      )}
    </div>
  );
}

export default App;
