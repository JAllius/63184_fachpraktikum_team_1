import { Link, useParams, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import {
  get_ml_problems,
  type MLProblem,
  type MLProblemListResponse,
} from "../../../lib/actions/mlProblem.action";
import {
  get_dataset_version,
  type DatasetVersion,
} from "../../../lib/actions/datasetVersion.action";

const DatasetVersionIdPage = () => {
  const params = useParams<{ datasetId: string; datasetVersionId: string }>();
  if (!params.datasetVersionId) {
    throw new Error("datasetVersionId param missing");
  }
  const datasetVersionId = params.datasetVersionId;

  const [mlProblems, setMlProblems] = useState<MLProblem[]>([]);
  const [loading, setLoading] = useState(true);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [seachParams, setSearchParams] = useSearchParams();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [datasetVersion, setDatasetVersion] = useState<DatasetVersion | null>(
    null
  );

  const q = seachParams.get("q") || "";
  const id = seachParams.get("id") || "";
  const task = seachParams.get("task") || "";
  const target = seachParams.get("target") || "";
  // const name = seachParams.get("name") || "";

  useEffect(() => {
    async function loadDatasetVersion() {
      try {
        const data: DatasetVersion = await get_dataset_version(
          datasetVersionId
        );
        setDatasetVersion(data);
      } catch (error) {
        console.log(error);
      }
    }
    loadDatasetVersion();
  }, [datasetVersionId]);

  useEffect(() => {
    async function loadMlProblems() {
      try {
        const data: MLProblemListResponse = await get_ml_problems(
          datasetVersionId,
          {
            q: q || undefined,
            id: id || undefined,
            task: id || undefined,
            target: id || undefined,
            // name: name || undefined,
          }
        );
        setMlProblems(data.items);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    }
    loadMlProblems();
  }, [datasetVersionId, q, id, task, target]); // name

  if (loading) {
    return (
      <div className="min-w-full flex items-center justify-center">
        Loading . . .
      </div>
    );
  }

  return (
    <div className="min-w-full flex flex-col items-center justify-center">
      <h1>ML Problems of: {datasetVersionId}</h1>{" "}
      {/* datasetVersion?.name ?? */}
      <ul>
        {mlProblems.map((mlp) => (
          <li key={mlp.id} className="flex">
            <div className="border rounded px-2 py-2 ">
              {/* <span className="font-semibold">{dsv.name}</span>, */}
              {mlp.id}, {mlp.task}, {mlp.target}, {mlp.created_at}
            </div>
            <Link
              to={`${mlp.id}`}
              className="px-3 py-1 rounded-md flex items-center justify-center text-blue-500 hover:bg-blue-500 hover:text-white hover:scale-105 active:scale-95 transition-all duration-150"
            >
              View
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DatasetVersionIdPage;
