import "./Actions.css";

interface ActionsProps {
  countryName: string;
  onShow: (name: string) => void;
  onEdit: (name: string) => void;
  onDelete: (name: string) => void;
}

export default function Actions({ countryName, onShow, onEdit, onDelete }: ActionsProps) {
  return (
    <div className="actions">
      <button className="action-btn show" onClick={() => onShow(countryName)}>Show</button>
      <button className="action-btn edit" onClick={() => onEdit(countryName)}>Edit</button>
      <button className="action-btn delete" onClick={() => onDelete(countryName)}>Delete</button>
    </div>
  );
}
