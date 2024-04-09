import react, { useState } from "react";
import "./App.css";
import { nflTeams, years } from "../utils.ts";

// @ts-ignore;
import football from "./assets/football.png";
import React from "react";

function App() {
  const [teams, setTeams] = useState({
    awayTeam: "Bears",
    awayYear: "2023",
    homeTeam: "Bengals",
    homeYear: "2023",
  });
  const [result, setResult] = useState([]);
  const [error, setError] = useState("");
  const [resultTeams, setResultTeams] = useState({
    awayTeam: "",
    homeTeam: "",
  });

  // calculate scores using existing structure of result
  let awayScore, homeScore;
  if (result && resultTeams.homeTeam === result[0]) {
    awayScore = Math.min(result[1] as number, result[2] as number);
    homeScore = Math.max(result[1] as number, result[2] as number);
  } else {
    awayScore = Math.max(result[1] as number, result[2] as number);
    homeScore = Math.min(result[1] as number, result[2] as number);
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
    fetch(`/api/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(teams),
    })
      .then((response) => response.json())
      .then((data) => {
        setResult(data.predictions);
        setResultTeams({ awayTeam: teams.awayTeam, homeTeam: teams.homeTeam });
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className="flex flex-col items-center">
      <div className="mb-8">
        <img src={football} alt="football" className="w-32 h-32" />
      </div>
      <h1 className="mb-8">NFL Game Predictor</h1>
      <div className="flex max-w-sm gap-8 justify-center flex-col md:flex-row">
        <div className="flex flex-row gap-2">
          <select
            id="awayYearDropdown"
            name="awayYear"
            onChange={handleTeamChange}
            defaultValue="2023"
          >
            {years.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
          <select
            id="awayTeamsDropdown"
            name="awayTeam"
            onChange={handleTeamChange}
            defaultValue="Bears"
          >
            {nflTeams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>
        at
        <div className="flex flex-row gap-2">
          <select
            id="homeYearDropdown"
            name="homeYear"
            onChange={handleTeamChange}
            defaultValue="2023"
          >
            {years.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
          <select
            id="homeTeamsDropdown"
            name="homeTeam"
            onChange={handleTeamChange}
            defaultValue="Bengals"
          >
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
      {result.length > 1 && (
        <div className="flex flex-col items-center justify-center gap-4">
          <div className="mt-8 text-left text-2xl">
            <div className="">
              <strong>{resultTeams.awayTeam}:</strong> {awayScore}
            </div>
            <div>
              <strong>{resultTeams.homeTeam}:</strong> {homeScore}
            </div>
          </div>
          <div className="text-4xl font-bold text-center">{result[0]} win!</div>
        </div>
      )}
    </div>
  );
}

export default App;
