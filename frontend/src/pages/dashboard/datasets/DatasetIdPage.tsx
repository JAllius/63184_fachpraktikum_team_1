import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { get_dataset_versions, type DatasetVersion } from "../../../lib/api";

const DatasetIdPage = () => {
  const params = useParams<{ datasetId: string }>();
  if (!params.datasetId) {
    throw new Error("datasetId param missing");
  }
  const datasetId = params.datasetId;

  const [datasetVersions, setDatasetVersions] = useState<DatasetVersion[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDatasetVersions() {
      try {
        const data = await get_dataset_versions(datasetId);
        setDatasetVersions(data);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    }
    loadDatasetVersions();
  }, [datasetId]);

  if (loading) {
    return (
      <div className="min-w-full flex items-center justify-center">
        Loading . . .
      </div>
    );
  }

  return (
    <div className="min-w-full flex flex-col items-center justify-center">
      <h1>Dataset Versions</h1>
      <ul>
        {datasetVersions.map((ds) => (
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

export default DatasetIdPage;
