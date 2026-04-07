import { useRef, useEffect } from "react";
import type { Country } from "../types/Country";
import "./ShowCountryDialog.css";

interface Props {
  country: Country;
  onClose: () => void;
}

export default function ShowCountryDialog({ country, onClose }: Props) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    dialogRef.current?.showModal();
    const dialog = dialogRef.current;
    const handleCancel = () => onClose();
    dialog?.addEventListener("cancel", handleCancel);
    return () => dialog?.removeEventListener("cancel", handleCancel);
  }, [onClose]);

  const formatNumber = (n: number) => n.toLocaleString();

  return (
    <dialog ref={dialogRef} className="show-dialog">
      <h2 className="show-dialog-title">{country.name}</h2>
      <dl className="show-dialog-details">
        <dt>Capital</dt>
        <dd>{country.capital}</dd>
        <dt>Population</dt>
        <dd>{formatNumber(country.population)}</dd>
        <dt>Area (km²)</dt>
        <dd>{formatNumber(country.area)}</dd>
        <dt>Continent</dt>
        <dd>{country.continent}</dd>
        <dt>Language</dt>
        <dd>{country.language}</dd>
        <dt>Currency</dt>
        <dd>{country.currency}</dd>
      </dl>
      <div className="show-dialog-flag">
        <img
          src={`https://flagcdn.com/w320/${country.countryCode}.png`}
          alt={`Flag of ${country.name}`}
          className="show-dialog-flag-img"
        />
      </div>
      <div className="show-dialog-footer">
        <button type="button" className="show-btn-close" onClick={onClose}>Close</button>
      </div>
    </dialog>
  );
}
