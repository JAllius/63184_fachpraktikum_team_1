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
import { SortableHeader } from "@/components/table";
import PredictionActions from "./PredictionActions";
import type { PredictionJoined } from "@/lib/actions/predictions/prediction.action";

type Props = {
  predictions: PredictionJoined[];
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
              <SortableHeader field="dataset_name" label="Dataset" />
            </TableHead>
            <TableHead>
              <SortableHeader
                field="dataset_version_name"
                label="Dataset Version"
              />
            </TableHead>
            <TableHead>
              <SortableHeader field="problem_name" label="ML Problem" />
            </TableHead>
            <TableHead>
              <SortableHeader field="model_name" label="Model" />
            </TableHead>
            <TableHead>
              <SortableHeader field="name" label="Prediction name" />
            </TableHead>
            <TableHead>
              <SortableHeader field="created_at" label="Created" />
            </TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          {predictions.map((pr) => {
            const viewUrl = `/dashboard/datasets/${pr.dataset_id}/${pr.dataset_version_id}/${pr.problem_id}/${pr.model_id}/${pr.id}`;

            return (
              <TableRow key={pr.id}>
                <TableCell className="text-muted-foreground">
                  {pr.dataset_name}
                </TableCell>
                <TableCell className="text-muted-foreground">
                  {pr.dataset_version_name}
                </TableCell>
                <TableCell className="text-muted-foreground">
                  {pr.problem_name}
                </TableCell>
                <TableCell className="text-muted-foreground">
                  {pr.model_name}
                </TableCell>
                <TableCell className="font-medium">
                  <Link to={viewUrl} aria-label="View prediction">
                    {pr.name}
                  </Link>
                </TableCell>
                <TableCell>{pr.created_at}</TableCell>
                <TableCell>
                  <PredictionActions
                    datasetId={pr.dataset_id}
                    datasetVersionId={pr.dataset_version_id}
                    problemId={pr.problem_id}
                    modelId={pr.model_id}
                    predictionId={pr.id}
                    parent="Prediction"
                    onDelete={() => askDelete(pr.id)}
                    onUpdate={() => askUpdate(pr.id)}
                  />
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>

        <TableFooter>
          <TableRow>
            <TableCell colSpan={6}>Total</TableCell>
            <TableCell className="text-right">{predictions.length}</TableCell>
          </TableRow>
        </TableFooter>
      </Table>
    </div>
  );
};

export default PredictionsTable;
