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
import type { DatasetVersion } from "@/lib/actions/dataset_versions";

type Props = {
  datasetVersions: DatasetVersion[];
  askDelete: (id: string) => void;
  askUpdate: (id: string) => void;
};

const DatasetVersionsTable = ({
  datasetVersions,
  askDelete,
  askUpdate,
}: Props) => {
  return (
    <div>
      <Table>
        <TableCaption>List of Dataset Versions</TableCaption>
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
          {datasetVersions.map((dsv) => (
            <TableRow key={dsv.id}>
              <TableCell className="font-medium">
                <Link to={`${dsv.id}`} aria-label="View dataset">
                  {dsv.name}
                </Link>
              </TableCell>
              <TableCell className="text-muted-foreground">{dsv.id}</TableCell>
              <TableCell>{dsv.created_at}</TableCell>
              <TableCell>
                <RowActions
                  id={dsv.id}
                  parent="Dataset Version"
                  onDelete={() => askDelete(dsv.id)}
                  onUpdate={() => askUpdate(dsv.id)}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell colSpan={3}>Total</TableCell>
            <TableCell className="text-right">
              {datasetVersions.length}
            </TableCell>
          </TableRow>
        </TableFooter>
      </Table>
    </div>
  );
};

export default DatasetVersionsTable;
