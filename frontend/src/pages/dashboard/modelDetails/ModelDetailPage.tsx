import { useParams, useSearchParams } from "react-router-dom";
import PredictFormDrawer from "@/components/ml/predict/PredictFormDrawer";
import {
  PredictionsTable,
  type DeleteTarget,
  type UpdateTarget,
} from "@/components/predictions";
import type { Model } from "@/lib/actions/models/model.action";
import {
  type Prediction,
  type PredictionListResponse,
  get_predictions,
} from "@/lib/actions/predictions";
import { useState, useCallback, useEffect } from "react";

const ModelDetailPage = () => {
  const params = useParams<{ problemId: string; modelId: string }>();
  if (!params.modelId) {
    throw new Error("modelId param missing");
  }
  const problemId = params.problemId;
  const modelId = params.modelId;

  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [model, setModel] = useState<Model | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [totalPages, setTotalPages] = useState(0);
  const [deleteTarget, setDeleteTarget] = useState<DeleteTarget | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [openDelete, setOpenDelete] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [deleting, setDeleting] = useState(false);
  const [updateTarget, setUpdateTarget] = useState<UpdateTarget | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [openUpdate, setOpenUpdate] = useState(false);

  const page = Number(searchParams.get("page") ?? 1);
  const size = Number(searchParams.get("size") ?? 20);
  const sort = searchParams.get("sort") ?? "created_at";
  const dir = ((searchParams.get("dir") as "asc") || "desc") ?? "desc";
  const q = searchParams.get("q") || "";
  const id = searchParams.get("id") || "";
  // const name = searchParams.get("name") || "";

  // useEffect(() => {
  //   async function loadModel() {
  //     try {
  //       const data: Model = await get_model(modelId);
  //       setDataset(data);
  //     } catch (error) {
  //       console.log(error);
  //     }
  //   }
  //   loadModel();
  // }, [modelId]);

  const loadPredictions = useCallback(async () => {
    try {
      const data: PredictionListResponse = await get_predictions(modelId, {
        page,
        size,
        sort,
        dir,
        q: q || undefined,
        id: id || undefined,
        // name: name || undefined,
      });
      setPredictions(data.items);
      setTotalPages(data.total_pages);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [modelId, page, size, sort, dir, q, id]); // name

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

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const onDelete = async () => {
    if (!deleteTarget) return;
    setDeleting(true);
    try {
      console.log("Deleting");
      await loadPredictions();
    } catch (error) {
      console.log(error);
    } finally {
      console.log("Done");
      cancelDelete();
      setDeleting(false);
    }
  };

  const askUpdate = (id: string) => {
    setUpdateTarget({ id });
    setOpenUpdate(true);
  };

  const cancelUpdate = () => {
    setOpenUpdate(false);
    setUpdateTarget(null);
  };

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const onUpdate = async () => {
    if (!updateTarget) return;
    try {
      console.log("Updating");
      await loadPredictions();
    } catch (error) {
      console.log(error);
    } finally {
      console.log("Done");
      cancelUpdate();
    }
  };

  if (loading) {
    return (
      <div className="min-w-full flex items-center justify-center">
        Loading...
      </div>
    );
  }

  return (
    <div className="w-full pl-4 pt-8">
      <div className="mx-auto w-full px-6">
        <h1>Details of {model?.name}</h1>
        <p className="mt-1 mb-4 text-sm text-muted-foreground">
          Manage {model?.name}.
        </p>
        <div className="flex justify-between">
          <div className="relative">{/* <PredictionsFilterbar /> */}</div>
          <PredictFormDrawer problemId={problemId} modelId={modelId} />
        </div>
        <PredictionsTable
          predictions={predictions}
          askDelete={askDelete}
          askUpdate={askUpdate}
        />
      </div>
    </div>
  );
};

export default ModelDetailPage;
