import { useState } from "react";
import type { Country } from "../types/Country";
import { getCountries } from "../services/countryService";
import Actions from "./Actions";
import "./CountryTable.css";

export default function CountryTable() {
  const [countries] = useState<Country[]>(getCountries);

  const formatNumber = (n: number) => n.toLocaleString();

  const handleShow = (name: string) => alert(`Show: ${name}`);
  const handleEdit = (name: string) => alert(`Edit: ${name}`);
  const handleDelete = (name: string) => alert(`Delete: ${name}`);

  return (
    <div className="country-table-wrapper">
      <h1>Countries of the World</h1>
      <table className="country-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Capital</th>
            <th>Population</th>
            <th>Area (km²)</th>
            <th>Continent</th>
            <th>Language</th>
            <th>Currency</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {countries.map((country) => (
            <tr key={country.name}>
              <td>{country.name}</td>
              <td>{country.capital}</td>
              <td className="num">{formatNumber(country.population)}</td>
              <td className="num">{formatNumber(country.area)}</td>
              <td>{country.continent}</td>
              <td>{country.language}</td>
              <td>{country.currency}</td>
              <td>
                <Actions
                  countryName={country.name}
                  onShow={handleShow}
                  onEdit={handleEdit}
                  onDelete={handleDelete}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
