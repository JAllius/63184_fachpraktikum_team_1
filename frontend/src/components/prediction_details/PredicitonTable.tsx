import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Link } from "react-router-dom";
import { RowActions, SortableHeader } from "../table";
import type { Prediction } from "@/lib/actions/predictions";

type Props = {
  columnNames: string[];
  rows: Record<string, unknown>[];
};

const PredictionTable = ({ columnNames, rows }: Props) => {
  const colSpan = columnNames.length - 1;
  const total = rows.length;

  // helper function for stability
  function renderCell(value: unknown): React.ReactNode {
    if (value === null || value === undefined) return "—";
    if (typeof value === "number") return value.toString();
    if (typeof value === "boolean") return value ? "true" : "false";
    if (typeof value === "string") return value;
    // fallback in case everything else fails
    return JSON.stringify(value);
  }

  return (
    <div>
      <Table>
        <TableCaption>Prediction</TableCaption>
        <TableHeader>
          <TableRow>
            {columnNames.map((name) => (
              <TableHead>{name}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((row, i) => (
            <TableRow key={i}>
              {columnNames.map((col) => (
                <TableCell>{renderCell(row[col])}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell colSpan={colSpan}>Total</TableCell>
            <TableCell className="text-right">{total}</TableCell>
          </TableRow>
        </TableFooter>
      </Table>
    </div>
  );
};

export default PredictionTable;
