import React, { Component } from "react";
import "../css/Landing.css";
import logo from "../resources/logo.png";
class Landing extends Component {
  render() {
    return (
      <section className="App-header">
        <div>
          <img src={logo} alt="Logo"></img>
          <div>
            <h1>Toxicity Identifier</h1>
            <p>
              Nous avons réalisé un programme capable d'identifier du contenu
              toxique sur Reddit. Voici une visualisation des données que nous
              avons pu en retirer.
            </p>
          </div>
        </div>
      </section>
    );
  }
}

export default Landing;
