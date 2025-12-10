import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { get_ml_problems, type MLProblem } from "../../../lib/api";

const DatasetVersionIdPage = () => {
  const params = useParams<{ datasetId: string; datasetVersionId: string }>();
  if (!params.datasetVersionId) {
    throw new Error("datasetVersionId param missing");
  }
  const datasetVersionId = params.datasetVersionId;

  const [mlProblems, setmlProblems] = useState<MLProblem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMLProblems() {
      try {
        const data = await get_ml_problems(datasetVersionId);
        setmlProblems(data);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    }
    loadMLProblems();
  }, [datasetVersionId]);

  if (loading) {
    return (
      <div className="min-w-full flex items-center justify-center">
        Loading . . .
      </div>
    );
  }

  return (
    <div className="min-w-full flex flex-col items-center justify-center">
      <h1>ML Problems</h1>
      <ul>
        {mlProblems.map((ds) => (
          <li key={ds.id} className="flex">
            <div className="border rounded px-2 py-2 ">
              {ds.id}, {ds.created_at}
            </div>
            <Link
              to={`${ds.id}`}
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
