import React from "react";
import ReactDOM from "react-dom";

const App = () => {
  return <h1>Hello from {{project_name}}!</h1>;
};

ReactDOM.render(<App />, document.getElementById("root"));