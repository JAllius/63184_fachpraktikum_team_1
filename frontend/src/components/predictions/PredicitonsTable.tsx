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
  predictions: Prediction[];
  askDelete: (id: string) => void;
  askUpdate: (id: string) => void;
};

const PredictionsTable = ({ predictions, askDelete, askUpdate }: Props) => {
  return (
    <div>
      <Table>
        <TableCaption>List of Predictions</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>
              <SortableHeader field="name" label="Name" />
            </TableHead>
            <TableHead>id</TableHead>
            <TableHead>
              <SortableHeader field="created_at" label="Created" />
            </TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {predictions.map((pr) => (
            <TableRow key={pr.id}>
              <TableCell className="font-medium">
                <Link to={`${pr.id}`} aria-label="View prediction">
                  {pr.name}
                </Link>
              </TableCell>
              <TableCell className="text-muted-foreground">{pr.id}</TableCell>
              <TableCell>{pr.created_at}</TableCell>
              <TableCell>
                <RowActions
                  id={pr.id}
                  parent="Dataset Version"
                  onDelete={() => askDelete(pr.id)}
                  onUpdate={() => askUpdate(pr.id)}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell colSpan={3}>Total</TableCell>
            <TableCell className="text-right">{predictions.length}</TableCell>
          </TableRow>
        </TableFooter>
      </Table>
    </div>
  );
};

export default PredictionsTable;
