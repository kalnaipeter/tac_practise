import { useState } from "react";
import type { Country } from "../types/Country";
import { getCountries } from "../services/countryService";
import Actions from "./Actions";
import Paginator from "./Paginator";
import "./CountryTable.css";

const ROWS_OPTIONS = [5, 10, 25];

export default function CountryTable() {
  const [countries] = useState<Country[]>(getCountries);
  const [rowsPerPage, setRowsPerPage] = useState<number>(5);
  const [currentPage, setCurrentPage] = useState<number>(1);

  const totalPages = Math.max(1, Math.ceil(countries.length / rowsPerPage));
  const paginatedCountries = countries.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );

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
          {paginatedCountries.map((country) => (
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
      <Paginator
        currentPage={currentPage}
        totalPages={totalPages}
        rowsPerPage={rowsPerPage}
        rowsPerPageOptions={ROWS_OPTIONS}
        onPageChange={setCurrentPage}
        onRowsPerPageChange={(rows) => {
          setRowsPerPage(rows);
          setCurrentPage(1);
        }}
      />
    </div>
  );
}
