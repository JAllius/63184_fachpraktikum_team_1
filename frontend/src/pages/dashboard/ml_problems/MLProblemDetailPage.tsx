import { useParams, useSearchParams } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";
import {
  get_ml_problem,
  type MLProblem,
} from "../../../lib/actions/mlProblems/mlProblem.action";
import {
  get_models,
  type Model,
  type ModelListResponse,
} from "../../../lib/actions/models/model.action";
import type { DeleteTarget, UpdateTarget } from "@/components/models";
import ModelsTable from "@/components/models/ModelsTable";
import Train from "@/components/ml/train/Train";
import Predict from "@/components/ml/predict/Predict";

const MLProblemDetailPage = () => {
  const params = useParams<{
    datasetId: string;
    datasetVersionId: string;
    problemId: string;
  }>();
  if (!params.problemId) {
    throw new Error("problemId param missing");
  }
  const problemId = params.problemId;

  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [mlProblem, setMLProblem] = useState<MLProblem | null>(null);
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
  const name = searchParams.get("name") || "";
  const algorithm = searchParams.get("algorithm") || "";
  const train_mode = searchParams.get("train_mode") || "";
  const evaluation_strategy = searchParams.get("evaluation_strategy") || "";
  const status = searchParams.get("status") || "";

  useEffect(() => {
    async function loadMLProblem() {
      try {
        const data: MLProblem = await get_ml_problem(problemId);
        setMLProblem(data);
      } catch (error) {
        console.log(error);
      }
    }
    loadMLProblem();
  }, [problemId]);

  const loadModels = useCallback(async () => {
    try {
      const data: ModelListResponse = await get_models(problemId, {
        page,
        size,
        sort,
        dir,
        q: q || undefined,
        id: id || undefined,
        name: name || undefined,
        algorithm: algorithm || undefined,
        train_mode: train_mode || undefined,
        evaluation_strategy: evaluation_strategy || undefined,
        status: status || undefined,
      });
      setModels(data.items);
      setTotalPages(data.total_pages);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [
    problemId,
    page,
    size,
    sort,
    dir,
    q,
    id,
    name,
    algorithm,
    train_mode,
    evaluation_strategy,
    status,
  ]);

  useEffect(() => {
    loadModels();
  }, [loadModels]);

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
      await loadModels();
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
      await loadModels();
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
  console.log(mlProblem);
  if (!mlProblem) return;

  return (
    <div className="w-full pl-4 pt-8">
      <div className="mx-auto w-full px-6">
        <h1>Models of {mlProblem?.name}</h1>
        <p className="mt-1 mb-4 text-sm text-muted-foreground">
          Manage all models of {mlProblem?.name}.
        </p>
        <div className="flex justify-between">
          {/* <div className="relative">
            <DatasetVersionsFilterbar />
          </div> */}
          <Train problemId={problemId} />
          <Predict problemId={problemId} />
        </div>
        <ModelsTable
          models={models}
          askDelete={askDelete}
          askUpdate={askUpdate}
          task={mlProblem.task}
        />
      </div>
    </div>
  );
};

export default MLProblemDetailPage;
