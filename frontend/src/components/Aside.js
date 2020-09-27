import React from "react";
import "./Aside.css";

export default function Aside() {
  return (
    <aside className="sidenav">
      <img src="http://www.gravatar.com/avatar" alt="Name" />
      <div className="sidenav__title">Dashboard</div>
      <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
      </ul>
    </aside>
  );
}
