import { ListItem, ListItemText } from "@mui/material";

interface IParameterReadOnlyProps {
  name: string;
  value: any;
}

export default function ParameterReadOnly({
  name,
  value,
}: IParameterReadOnlyProps) {
  return (
    <ListItem
      divider={true}
    >
      <ListItemText
        primary={name}
        secondary={value}
        primaryTypographyProps={{
          color: "secondary",
        }}
        secondaryTypographyProps={{
          fontSize: 20,
        }}
      />
    </ListItem>
  );
}
