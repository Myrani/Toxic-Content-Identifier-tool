import React, { Component } from "react";
import "../css/ScoreTable.css";

class ScoreTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      scores: [
        { name: "u/ProfessionalTroller", score: 90 },
        { name: "u/Toxikkkk", score: 85 },
        { name: "u/EmmanuelMacron", score: 95 },
      ],
    };
  }

  componentDidMount() {
    this.setState({
      scores: this.state.scores.sort((a, b) => b.score - a.score),
    });
  }

  render() {
    return (
      <>
        <h1>Utilisateurs Reddit les plus toxiques :</h1>
        <div className="center-div">
          <table class="styled-table">
            <thead>
              <tr>
                <th>Nom</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {this.state.scores.map((item, index) => (
                <tr key={index}>
                  <td>{item.name}</td>
                  <td>{item.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>
    );
  }
}

export default ScoreTable;
