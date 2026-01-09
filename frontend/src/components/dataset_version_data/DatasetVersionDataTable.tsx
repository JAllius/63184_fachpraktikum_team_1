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
import { get_dataset_version_csv } from "@/lib/actions/dataset_versions/datasetVersion.action";
import { useEffect, useState } from "react";
import Loading from "../loading/Loading";
import NotFound from "../errors/not_found/NotFound";

type Props = {
  uri: string;
};

const DatasetVersionDataTable = ({ uri }: Props) => {
  const [datasetVersionCSV, setDatasetVersionCSV] = useState<{
    column_names: string[];
    rows: Record<string, unknown>[];
  }>({ column_names: [], rows: [] });
  const [csvLoading, setCsvLoading] = useState(true);

  useEffect(() => {
    async function loadCSV() {
      if (!uri) return;
      try {
        const data: {
          column_names: string[];
          rows: Record<string, unknown>[];
        } = await get_dataset_version_csv(uri);
        setDatasetVersionCSV(data);
        setCsvLoading(false);
        console.log(data);
      } catch (error) {
        console.log(error);
      } finally {
        setCsvLoading(false);
      }
    }
    loadCSV();
  }, [uri]);

  const columnNames: string[] = datasetVersionCSV.column_names;
  const rows: Record<string, unknown>[] = datasetVersionCSV.rows;
  const colSpan = columnNames.length - 1;
  const total = rows.length;

  // helper function for stability
  function renderCell(value: unknown): React.ReactNode {
    if (value === null || value === undefined) return "—";
    if (typeof value === "number") return value;
    if (typeof value === "boolean") return value ? "true" : "false";
    if (typeof value === "string") return value;
    // fallback in case everything else fails
    return JSON.stringify(value);
  }

  return (
    <div className="w-full h-full min-h-0 overflow-auto">
      {csvLoading ? (
        <div className="h-full flex items-center justify-center">
          <Loading />
        </div>
      ) : rows.length > 0 ? (
        <Table>
          <TableCaption>Dataset Version Data</TableCaption>
          <TableHeader>
            <TableRow>
              {columnNames.map((name) => (
                <TableHead key={name}>{name}</TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map((row, i) => (
              <TableRow key={i}>
                {columnNames.map((col) => (
                  <TableCell key={col}>{renderCell(row[col])}</TableCell>
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
      ) : (
        <div className="h-full flex items-center justify-center">
          <NotFound name="Dataset Version CSV" />
        </div>
      )}
    </div>
  );
};

export default DatasetVersionDataTable;
