import React, { Component } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

import "../css/Example.css";

const data = [
  {
    name: "r/LearnCode",
    Regular: 4000,
    Toxic: 2400,
    amt: 2400,
  },
  {
    name: "r/Valorant",
    Regular: 3000,
    Toxic: 1398,
    amt: 2210,
  },
  {
    name: "r/LeagueOfLegends",
    Regular: 4000,
    Toxic: 8750,
    amt: 2290,
  },
  {
    name: "r/Conservative",
    Regular: 2780,
    Toxic: 3908,
    amt: 2000,
  },
  {
    name: "r/Politics",
    Regular: 1890,
    Toxic: 4800,
    amt: 2181,
  },
  {
    name: "r/Shitposting",
    Regular: 2390,
    Toxic: 3800,
    amt: 2500,
  },
  {
    name: "r/memes",
    Regular: 3490,
    Toxic: 4300,
    amt: 2100,
  },
];

class Example extends Component {
  render() {
    return (
      <>
        <h1>
          Nombre de posts et leur proportion à être toxique entre 2022 et 2023
        </h1>
        <div className="center-div">
          <BarChart
            width={1000}
            height={600}
            data={data}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Toxic" stackId="a" fill="#8884d8" />
            <Bar dataKey="Regular" stackId="a" fill="#82ca9d" />
          </BarChart>
        </div>
      </>
    );
  }
}

export default Example;
