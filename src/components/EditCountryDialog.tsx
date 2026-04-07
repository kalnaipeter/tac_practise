import { useRef, useEffect, useState } from "react";
import type { Country } from "../types/Country";
import "./EditCountryDialog.css";

interface Props {
  country: Country;
  onSave: (updated: Country) => void;
  onCancel: () => void;
}

export default function EditCountryDialog({ country, onSave, onCancel }: Props) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const [draft, setDraft] = useState<Country>({ ...country });

  useEffect(() => {
    dialogRef.current?.showModal();
    const dialog = dialogRef.current;
    const handleCancel = () => onCancel();
    dialog?.addEventListener("cancel", handleCancel);
    return () => dialog?.removeEventListener("cancel", handleCancel);
  }, [onCancel]);

  const handleChange = (field: keyof Country, value: string) => {
    setDraft((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    onSave({
      ...draft,
      population: Number(draft.population),
      area: Number(draft.area),
      countryCode: country.countryCode,
    });
  };

  return (
    <dialog ref={dialogRef} className="edit-dialog">
      <h2 className="edit-dialog-title">Edit — {country.name}</h2>
      <form className="edit-dialog-form">
        <label className="edit-dialog-label" htmlFor="edit-name">Name</label>
        <input
          id="edit-name"
          className="edit-dialog-input"
          type="text"
          value={draft.name}
          onChange={(e) => handleChange("name", e.target.value)}
        />

        <label className="edit-dialog-label" htmlFor="edit-capital">Capital</label>
        <input
          id="edit-capital"
          className="edit-dialog-input"
          type="text"
          value={draft.capital}
          onChange={(e) => handleChange("capital", e.target.value)}
        />

        <label className="edit-dialog-label" htmlFor="edit-population">Population</label>
        <input
          id="edit-population"
          className="edit-dialog-input"
          type="number"
          value={draft.population}
          onChange={(e) => handleChange("population", e.target.value)}
        />

        <label className="edit-dialog-label" htmlFor="edit-area">Area (km²)</label>
        <input
          id="edit-area"
          className="edit-dialog-input"
          type="number"
          value={draft.area}
          onChange={(e) => handleChange("area", e.target.value)}
        />

        <label className="edit-dialog-label" htmlFor="edit-continent">Continent</label>
        <input
          id="edit-continent"
          className="edit-dialog-input"
          type="text"
          value={draft.continent}
          onChange={(e) => handleChange("continent", e.target.value)}
        />

        <label className="edit-dialog-label" htmlFor="edit-language">Language</label>
        <input
          id="edit-language"
          className="edit-dialog-input"
          type="text"
          value={draft.language}
          onChange={(e) => handleChange("language", e.target.value)}
        />

        <label className="edit-dialog-label" htmlFor="edit-currency">Currency</label>
        <input
          id="edit-currency"
          className="edit-dialog-input"
          type="text"
          value={draft.currency}
          onChange={(e) => handleChange("currency", e.target.value)}
        />
      </form>
      <div className="edit-dialog-footer">
        <button type="button" className="edit-btn-cancel" onClick={onCancel}>Cancel</button>
        <button type="button" className="edit-btn-save" onClick={handleSave}>Save</button>
      </div>
    </dialog>
  );
}
