import { useState } from "react";
import "./ThemeToggle.css";

type Theme = "light" | "dark";

function getInitialTheme(): Theme {
  const current = document.documentElement.dataset.theme;
  return current === "dark" ? "dark" : "light";
}

export default function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(getInitialTheme);

  const toggle = () => {
    const next: Theme = theme === "light" ? "dark" : "light";
    setTheme(next);
    document.documentElement.dataset.theme = next;
    localStorage.setItem("theme", next);
  };

  return (
    <button className="theme-toggle" onClick={toggle} aria-label={`Switch to ${theme === "light" ? "dark" : "light"} mode`}>
      {theme === "light" ? "🌙" : "☀️"}
    </button>
  );
}
