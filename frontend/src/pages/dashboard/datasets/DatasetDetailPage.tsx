import { Link, useParams, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import {
  get_dataset_versions,
  type DatasetVersion,
  type DatasetVersionListResponse,
} from "../../../lib/actions/dataset_versions/datasetVersion.action";
import {
  get_dataset,
  type Dataset,
} from "../../../lib/actions/datasets/dataset.action";

const DatasetIdPage = () => {
  const params = useParams<{ datasetId: string }>();
  if (!params.datasetId) {
    throw new Error("datasetId param missing");
  }
  const datasetId = params.datasetId;

  const [datasetVersions, setDatasetVersions] = useState<DatasetVersion[]>([]);
  const [loading, setLoading] = useState(true);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [seachParams, setSearchParams] = useSearchParams();
  const [dataset, setDataset] = useState<Dataset | null>(null);

  const q = seachParams.get("q") || "";
  const id = seachParams.get("id") || "";
  // const name = seachParams.get("name") || "";

  useEffect(() => {
    async function loadDataset() {
      try {
        const data: Dataset = await get_dataset(datasetId);
        setDataset(data);
      } catch (error) {
        console.log(error);
      }
    }
    loadDataset();
  }, [datasetId]);

  useEffect(() => {
    async function loadDatasetVersions() {
      try {
        const data: DatasetVersionListResponse = await get_dataset_versions(
          datasetId,
          {
            q: q || undefined,
            id: id || undefined,
            // name: name || undefined,
          }
        );
        setDatasetVersions(data.items);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    }
    loadDatasetVersions();
  }, [datasetId, q, id]); // name

  if (loading) {
    return (
      <div className="min-w-full flex items-center justify-center">
        Loading . . .
      </div>
    );
  }

  return (
    <div className="min-w-full flex flex-col items-center justify-center">
      <h1>Versions of: {dataset?.name ?? datasetId}</h1>
      <ul>
        {datasetVersions.map((dsv) => (
          <li key={dsv.id} className="flex">
            <div className="border rounded px-2 py-2 ">
              {/* <span className="font-semibold">{dsv.name}</span>, */}
              {dsv.id}, {dsv.created_at}
            </div>
            <Link
              to={`${dsv.id}`}
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
