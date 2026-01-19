import { useParams, useSearchParams } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";
import {
  get_ml_problem,
  type MLProblem,
} from "../../../lib/actions/mlProblems/mlProblem.action";
import {
  delete_model,
  get_models,
  update_model,
  type Model,
  type ModelListResponse,
} from "../../../lib/actions/models/model.action";
import type { DeleteTarget, UpdateTarget } from "@/components/models";
import ModelsTable from "@/components/models/ModelsTable";
import Train from "@/components/ml/train/Train";
import Predict from "@/components/ml/predict/Predict";
import MLProblemDetails from "@/components/ml_problem_details/MLProblemDetails";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import ModelDelete from "@/components/models/ModelDelete";
import ModelsFilterbar from "@/components/models/ModelsFilterbar";
import ModelUpdate from "@/components/models/ModelUpdate";
import { Pagination, PageSize } from "@/components/table";
import {
  get_dataset_version,
  type DatasetVersion,
} from "@/lib/actions/dataset_versions";
import type { Profile } from "../dataset_versions/DatasetVersionDetailPage";
import Loading from "@/components/loading/Loading";
import NotFound from "@/components/errors/not_found/NotFound";
import { Fox } from "@/components/watermark/Fox";
import { toast } from "sonner";
import type { ModelUpdateInput } from "@/components/models/model.schema";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:42000";

export type FeatureStrategy = {
  include: [string, string][];
  exclude: [string, string][];
};

const MLProblemDetailPage = () => {
  const params = useParams<{
    datasetId: string;
    datasetVersionId: string;
    problemId: string;
  }>();
  if (!params.datasetId) {
    throw new Error("datasetId param missing");
  }
  if (!params.problemId) {
    throw new Error("problemId param missing");
  }
  if (!params.datasetVersionId) {
    throw new Error("datasetVersionId param missing");
  }
  const datasetId = params.datasetId;
  const datasetVersionId = params.datasetVersionId;
  const problemId = params.problemId;

  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const [mlProblem, setMLProblem] = useState<MLProblem | null>(null);
  const [datasetVersion, setDatasetVersion] = useState<DatasetVersion | null>(
    null,
  );
  const [totalPages, setTotalPages] = useState(0);
  const [deleteTarget, setDeleteTarget] = useState<DeleteTarget | null>(null);
  const [openDelete, setOpenDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [updateTarget, setUpdateTarget] = useState<UpdateTarget | null>(null);
  const [openUpdate, setOpenUpdate] = useState(false);
  const [tabValue, setTabValue] = useState("models");
  const [featureStrategy, setFeatureStrategy] = useState<FeatureStrategy>({
    include: [],
    exclude: [],
  });

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

  useEffect(() => {
    async function loadDatasetVersion() {
      try {
        const data: DatasetVersion =
          await get_dataset_version(datasetVersionId);
        setDatasetVersion(data);
      } catch (error) {
        console.log(error);
      }
    }
    loadDatasetVersion();
  }, [datasetVersionId]);

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

  useEffect(() => {
    if (!mlProblem || !datasetVersion) return;
    if (mlProblem.feature_strategy === "auto") {
      const profile: Profile = datasetVersion?.profile_json
        ? JSON.parse(datasetVersion?.profile_json)
        : null;
      const exclude = Object.entries(profile.exclude_suggestions);
      setFeatureStrategy({
        include: [],
        exclude: exclude,
      });
    } else {
      const feature_strategy = mlProblem?.feature_strategy
        ? JSON.parse(mlProblem?.feature_strategy)
        : { include: [], exclude: [] };
      const include: [string, string][] = Object.entries(
        feature_strategy?.include,
      );
      const exclude: [string, string][] = Object.entries(
        feature_strategy?.exclude,
      );
      setFeatureStrategy({
        include: include,
        exclude: exclude,
      });
    }
  }, [mlProblem, datasetVersion]);

  useEffect(() => {
    const eventSource = new EventSource(`${API_URL}/events/stream`);

    const refreshOnTrain = (e: MessageEvent) => {
      const payload = JSON.parse(e.data);
      if (payload.job?.type === "train") {
        if (payload.job?.status === "completed")
          toast.success("Training finished successfully");
      } else if (payload.job?.status === "failed") {
        toast.error("Training failed");
      }
      loadModels();
    };

    eventSource.addEventListener("job.completed", refreshOnTrain);
    eventSource.addEventListener("job.failed", refreshOnTrain);

    return () => {
      eventSource.removeEventListener("job.completed", refreshOnTrain);
      eventSource.removeEventListener("job.failed", refreshOnTrain);
      eventSource.close();
    };
  });

  const prodModel = models.find((model) => model.status === "production");
  const prodModelName = prodModel?.name;
  const prodModelId = prodModel?.id;

  const askDelete = (id: string) => {
    setDeleteTarget({ id });
    setOpenDelete(true);
  };

  const cancelDelete = () => {
    setOpenDelete(false);
    setDeleteTarget(null);
  };

  const onDelete = async (model_id: string) => {
    if (!model_id) return;

    const res = await delete_model(model_id);
    if (!res.ok) {
      toast.error(res.error);
      return;
    }
    toast.success("Model deleted");
    await loadModels();
    cancelDelete();
    setDeleting(false);
  };

  const askUpdate = (id: string, name: string) => {
    setUpdateTarget({ id, name });
    setOpenUpdate(true);
  };

  const cancelUpdate = () => {
    setOpenUpdate(false);
    setUpdateTarget(null);
  };

  const onUpdate = async (model_id: string, data: ModelUpdateInput) => {
    if (!model_id || !data) return;

    const res = await update_model(model_id, data);
    if (!res.ok) {
      toast.error(res.error);
      return;
    }
    toast.success("ML Problem updated");
    await loadModels();
    cancelUpdate();
  };

  if (loading) {
    return <Loading />;
  }

  if (!mlProblem) return <NotFound name="ML Problem" />;

  return (
    <div className="w-full pl-4 pt-8">
      <div className="mx-auto w-full px-6">
        <h1>ML problem details: {mlProblem?.name ?? "Unknown ML Problem"}</h1>
        {tabValue === "models" && (
          <p className="mt-1 mb-4 text-sm text-muted-foreground">
            Manage all models of {mlProblem?.name ?? "Unknown ML Problem"}.
          </p>
        )}
        {tabValue === "configuration" && (
          <p className="mt-1 mb-4 text-sm text-muted-foreground">
            Manage the configuration of{" "}
            {mlProblem?.name ?? "Unknown ML Problem"}.
          </p>
        )}
        <Tabs className="w-full" value={tabValue} onValueChange={setTabValue}>
          <TabsList className="w-full items-center justify-start gap-2">
            <TabsTrigger value="models">Models</TabsTrigger>
            <TabsTrigger value="configuration">Configuration</TabsTrigger>
          </TabsList>
          <TabsContent value="models">
            {models.length > 0 ? (
              <div>
                <div className="flex justify-between">
                  <div className="relative">
                    <ModelsFilterbar />
                  </div>
                  <div className="flex gap-2">
                    <Train
                      problemId={problemId}
                      task={mlProblem.task}
                      onCreate={loadModels}
                    />
                    <Predict problemId={problemId} />
                  </div>
                </div>
                <ModelsTable
                  models={models}
                  askDelete={askDelete}
                  askUpdate={askUpdate}
                  task={mlProblem.task}
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
                  <ModelDelete
                    target={deleteTarget}
                    open={openDelete}
                    onConfirm={onDelete}
                    onCancel={cancelDelete}
                    deleting={deleting}
                  />
                )}
                {updateTarget && (
                  <ModelUpdate
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
                    <ModelsFilterbar />
                  </div>
                  <div className="flex gap-2">
                    <Train
                      problemId={problemId}
                      task={mlProblem.task}
                      onCreate={loadModels}
                    />
                    <Predict problemId={problemId} />
                  </div>
                </div>
                <div>
                  <p className="text-base font-semibold">No Models yet</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Train a model to activate this Tab.
                  </p>
                  <div className="mt-5">
                    <Train
                      problemId={problemId}
                      task={mlProblem.task}
                      onCreate={loadModels}
                    />
                  </div>
                </div>
              </div>
            )}
          </TabsContent>
          <TabsContent value="configuration">
            <div>
              <MLProblemDetails
                datasetId={datasetId}
                datasetVersionId={datasetVersionId}
                datasetVersionName={datasetVersion?.name}
                mlProblem={mlProblem}
                featureStrategy={featureStrategy}
                prodModelName={prodModelName}
                prodModelId={prodModelId}
              />
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default MLProblemDetailPage;
