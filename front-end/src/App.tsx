import { useState } from "react";
import "./App.css";
import { nflTeams } from "../utils.ts";

function App() {
  const [teams, setTeams] = useState({ awayTeam: "", homeTeam: "" });
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

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
    fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(teams),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
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
      <div>
        <button
          onClick={handleSubmit}
          className="mt-8 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Predict
        </button>
      </div>
    </div>
  );
}

export default App;
