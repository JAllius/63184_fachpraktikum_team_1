import { Link, useParams, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import {
  get_ml_problem,
  type MLProblem,
} from "../../../lib/actions/mlProblems/mlProblem.action";
import {
  get_models,
  type Model,
  type ModelListResponse,
} from "../../../lib/actions/models/model.action";
import TrainFormDrawer from "@/components/ml/train/TrainFormDrawer";
import PredictFormDrawer from "@/components/ml/predict/PredictFormDrawer";

const MLProblemIdPage = () => {
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
  const [seachParams] = useSearchParams();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [mlProblem, setMlProblem] = useState<MLProblem | null>(null);

  const q = seachParams.get("q") || "";
  const id = seachParams.get("id") || "";
  const name = seachParams.get("name") || "";
  const algorithm = seachParams.get("algorithm") || "";
  const train_mode = seachParams.get("train_mode") || "";
  const evaluation_strategy = seachParams.get("evaluation_strategy") || "";
  const status = seachParams.get("status") || "";

  useEffect(() => {
    async function loadMlProblem() {
      try {
        const data: MLProblem = await get_ml_problem(problemId);
        setMlProblem(data);
      } catch (error) {
        console.log(error);
      }
    }
    loadMlProblem();
  }, [problemId]);

  useEffect(() => {
    async function loadModels() {
      try {
        const data: ModelListResponse = await get_models(problemId, {
          q: q || undefined,
          id: id || undefined,
          name: name || undefined,
          algorithm: algorithm || undefined,
          train_mode: train_mode || undefined,
          evaluation_strategy: evaluation_strategy || undefined,
          status: status || undefined,
        });
        setModels(data.items);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    }
    loadModels();
  }, [
    problemId,
    q,
    id,
    name,
    algorithm,
    train_mode,
    evaluation_strategy,
    status,
  ]); // name

  if (loading) {
    return (
      <div className="min-w-full flex items-center justify-center">
        Loading . . .
      </div>
    );
  }

  return (
    <div className="min-w-full flex flex-col items-center justify-center">
      <h1>Models of: {problemId}</h1> {/* mlProblem?.name ?? */}
      <ul>
        {models.map((m) => (
          <li key={m.id} className="flex">
            <div className="border rounded px-2 py-2 ">
              <span className="font-semibold">{m.name}</span>, {m.id},{" "}
              {m.algorithm}, {m.status}, {m.train_mode}, {m.evaluation_strategy}{" "}
              , {m.created_at}
            </div>
            <Link
              to={`${m.id}`}
              className="px-3 py-1 rounded-md flex items-center justify-center text-blue-500 hover:bg-blue-500 hover:text-white hover:scale-105 active:scale-95 transition-all duration-150"
            >
              View
            </Link>
          </li>
        ))}
      </ul>
      <TrainFormDrawer problemId={problemId} />
      <PredictFormDrawer problemId={problemId} />
    </div>
  );
};

export default MLProblemIdPage;
