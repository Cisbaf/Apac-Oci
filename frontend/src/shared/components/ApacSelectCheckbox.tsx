import { IconButton } from "@mui/material";
import CheckBoxIcon from "@mui/icons-material/CheckBox";
import CheckBoxOutlineBlankIcon from "@mui/icons-material/CheckBoxOutlineBlank";
import { useAutorizeMultiplesApac } from "../context/AutorizeMultiplesApac";


export function ApacSelectCheckbox({ id }: { id: number }) {
  const { isSelected, toggleOne } = useAutorizeMultiplesApac();
  const checked = isSelected(id);

  return (
    <IconButton
      color={checked ? "primary" : "default"}
      onClick={() => toggleOne(id)}
      size="small"
    >
      {checked ? <CheckBoxIcon /> : <CheckBoxOutlineBlankIcon />}
    </IconButton>
  );
}
