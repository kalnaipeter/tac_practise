import { useEffect } from "react";
import type { Country } from "../types/Country";
import "./CountryDialog.css";

const COUNTRY_ISO: Record<string, string> = {
  Hungary: "hu",
  Germany: "de",
  Japan: "jp",
  Brazil: "br",
  Australia: "au",
  Canada: "ca",
  Egypt: "eg",
  "South Korea": "kr",
};

interface CountryDialogProps {
  country: Country | null;
  onClose: () => void;
}

export default function CountryDialog({ country, onClose }: CountryDialogProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  if (!country) return null;

  const isoCode = COUNTRY_ISO[country.name];

  return (
    <div className="dialog-backdrop" onClick={onClose}>
      <div className="dialog-box" onClick={(e) => e.stopPropagation()}>
        <button className="dialog-close" onClick={onClose}>×</button>
        <h2 className="dialog-title">{country.name}</h2>
        <dl className="dialog-info">
          <dt>Capital</dt>
          <dd>{country.capital}</dd>
          <dt>Population</dt>
          <dd>{country.population.toLocaleString()}</dd>
          <dt>Area</dt>
          <dd>{country.area.toLocaleString()} km²</dd>
          <dt>Continent</dt>
          <dd>{country.continent}</dd>
          <dt>Language</dt>
          <dd>{country.language}</dd>
          <dt>Currency</dt>
          <dd>{country.currency}</dd>
        </dl>
        {isoCode && (
          <div className="dialog-flag">
            <img
              src={`https://flagcdn.com/w160/${isoCode}.png`}
              alt={`Flag of ${country.name}`}
            />
          </div>
        )}
      </div>
    </div>
  );
}
