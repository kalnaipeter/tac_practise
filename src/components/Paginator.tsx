import "./Paginator.css";

interface PaginatorProps {
  currentPage: number;
  totalPages: number;
  rowsPerPage: number;
  rowsPerPageOptions: number[];
  onPageChange: (page: number) => void;
  onRowsPerPageChange: (rows: number) => void;
}

export default function Paginator({
  currentPage,
  totalPages,
  rowsPerPage,
  rowsPerPageOptions,
  onPageChange,
  onRowsPerPageChange,
}: PaginatorProps) {
  return (
    <div className="paginator">
      <label className="paginator__rows-label">
        Rows per page:
        <select
          value={rowsPerPage}
          onChange={(e) => onRowsPerPageChange(Number(e.target.value))}
        >
          {rowsPerPageOptions.map((opt) => (
            <option key={opt} value={opt}>
              {opt}
            </option>
          ))}
        </select>
      </label>
      <span className="paginator__info">
        Page {currentPage} of {totalPages}
      </span>
      <div className="paginator__nav">
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          Prev
        </button>
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
}
