import { useState } from "react";
import "./App.css";
import { nflTeams } from "../utils.ts";

function App() {
  const [teams, setTeams] = useState({ awayTeam: "", homeTeam: "" });

  const handleTeamChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = event.target;
    setTeams((prevTeams) => ({
      ...prevTeams,
      [name]: value,
    }));
  };

  return (
    <>
      <h1 className="mb-24">NFL Game Predictor</h1>
      <div className="flex flex-row">
        <div>
          <select
            id="homeTeamsDropdown"
            name="home"
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
            name="home"
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
    </>
  );
}

export default App;
