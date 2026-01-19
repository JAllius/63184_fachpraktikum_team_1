import { useSearchParams } from "react-router-dom";
import Predict from "@/components/ml/predict/Predict";
import {
  PredictionDelete,
  type DeleteTarget,
  type UpdateTarget,
} from "@/components/predictions";
import {
  get_predictions_all,
  type PredictionAllListResponse,
  type PredictionJoined,
} from "@/lib/actions/predictions/prediction.action";
import { useState, useCallback, useEffect } from "react";
import { PageSize, Pagination } from "@/components/table";
import Loading from "@/components/loading/Loading";
import { Fox } from "@/components/watermark/Fox";
import { toast } from "sonner";
import {
  delete_prediction,
  update_prediction,
} from "@/lib/actions/predictions/prediction.action";
import type { PredictionUpdateInput } from "@/components/predictions/prediction.schema";
import PredictionUpdate from "@/components/predictions/PredictionUpdate";
import PredictionsJoinedFilterbar from "@/components/predictions/joined_table/PredictionsJoinedFilterbar";
import PredictionsJoinedTable from "@/components/predictions/joined_table/PredictionsJoinedTable";

const PredictionsPage = () => {
  const [predictions, setPredictions] = useState<PredictionJoined[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const [totalPages, setTotalPages] = useState(0);

  const [deleteTarget, setDeleteTarget] = useState<DeleteTarget | null>(null);
  const [openDelete, setOpenDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const [updateTarget, setUpdateTarget] = useState<UpdateTarget | null>(null);
  const [openUpdate, setOpenUpdate] = useState(false);

  const page = Number(searchParams.get("page") ?? 1);
  const size = Number(searchParams.get("size") ?? 20);
  const sort = searchParams.get("sort") ?? "created_at";
  const dir = ((searchParams.get("dir") as "asc") || "desc") ?? "desc";

  const q = searchParams.get("q") || "";
  const dataset_name = searchParams.get("dataset_name") || "";
  const dataset_version_name = searchParams.get("dataset_version_name") || "";
  const problem_name = searchParams.get("problem_name") || "";
  const model_name = searchParams.get("model_name") || "";

  const loadPredictions = useCallback(async () => {
    try {
      const data: PredictionAllListResponse = await get_predictions_all({
        page,
        size,
        sort,
        dir,
        q: q || undefined,
        dataset_name: dataset_name || undefined,
        dataset_version_name: dataset_version_name || undefined,
        problem_name: problem_name || undefined,
        model_name: model_name || undefined,
      });

      setPredictions(data.items);
      setTotalPages(data.total_pages);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [
    page,
    size,
    sort,
    dir,
    q,
    dataset_name,
    dataset_version_name,
    problem_name,
    model_name,
  ]);

  useEffect(() => {
    loadPredictions();
  }, [loadPredictions]);

  const askDelete = (id: string) => {
    setDeleteTarget({ id });
    setOpenDelete(true);
  };

  const cancelDelete = () => {
    setOpenDelete(false);
    setDeleteTarget(null);
  };

  const onDelete = async (prediction_id: string) => {
    if (!prediction_id) return;

    const res = await delete_prediction(prediction_id);
    if (!res.ok) {
      toast.error(res.error);
      return;
    }
    toast.success("Prediction deleted");
    await loadPredictions();
    cancelDelete();
    setDeleting(false);
  };

  const askUpdate = (id: string) => {
    setUpdateTarget({ id });
    setOpenUpdate(true);
  };

  const cancelUpdate = () => {
    setOpenUpdate(false);
    setUpdateTarget(null);
  };

  const onUpdate = async (
    prediction_id: string,
    data: PredictionUpdateInput
  ) => {
    if (!prediction_id || !data) return;

    const res = await update_prediction(prediction_id, data);
    if (!res.ok) {
      toast.error(res.error);
      return;
    }
    toast.success("Prediction updated");
    await loadPredictions();
    cancelUpdate();
  };

  if (loading) return <Loading />;

  return (
    <div className="w-full pl-4 pt-8">
      <div className="mx-auto w-full px-6">
        <h1>Predictions</h1>
        <p className="mt-1 mb-4 text-sm text-muted-foreground">
          Browse and manage predictions across all datasets.
        </p>

        {predictions.length > 0 ? (
          <div>
            <div className="flex justify-between">
              <div className="relative">
                <PredictionsJoinedFilterbar />
              </div>
              <Predict />
            </div>
            <PredictionsJoinedTable
              predictions={predictions}
              askDelete={askDelete}
              askUpdate={askUpdate}
            />

            <div className="mt-2 grid grid-cols-3 items-center">
              <div />
              {totalPages > 1 ? (
                <div className="flex justify-center">
                  <Pagination totalPages={totalPages} />
                </div>
              ) : (
                <div />
              )}
              <div className="flex justify-end">
                <PageSize size={size} />
              </div>
            </div>

            {deleteTarget && (
              <PredictionDelete
                target={deleteTarget}
                open={openDelete}
                onConfirm={onDelete}
                onCancel={cancelDelete}
                deleting={deleting}
              />
            )}

            {updateTarget && (
              <PredictionUpdate
                target={updateTarget}
                open={openUpdate}
                onConfirm={onUpdate}
                onCancel={cancelUpdate}
              />
            )}
          </div>
        ) : (
          <div className="relative min-h-[80vh] bg-background">
            <div className="flex items-center">
              <Fox
                aria-hidden
                size="80%"
                className="pointer-events-none absolute inset-0 z-0 opacity-[0.12] m-auto"
                style={{ color: "hsl(var(--sidebar-foreground))" }}
                nodeFill="hsl(var(--sidebar-foreground))"
              />
            </div>
            <div className="flex justify-between">
              <div className="relative">
                <PredictionsJoinedFilterbar />
              </div>
              <Predict />
            </div>
            <div>
              <p className="text-base font-semibold">No predictions found</p>
              <div className="mt-5">
                <Predict />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictionsPage;
