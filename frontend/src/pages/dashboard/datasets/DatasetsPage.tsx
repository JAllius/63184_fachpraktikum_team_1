import { useEffect, useState } from "react";
import {
  get_datasets,
  type Dataset,
  type DatasetListResponse,
} from "../../../lib/actions/dataset.action";
import { Link, useSearchParams } from "react-router-dom";

const DatasetsPage = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [seachParams, setSearchParams] = useSearchParams();

  const q = seachParams.get("q") || "";
  const id = seachParams.get("id") || "";
  const name = seachParams.get("name") || "";

  useEffect(() => {
    async function loadDatasets() {
      try {
        const data: DatasetListResponse = await get_datasets({
          q: q || undefined,
          id: id || undefined,
          name: name || undefined,
        });
        setDatasets(data.items);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    }
    loadDatasets();
  }, [q, name, id]);

  if (loading) {
    return (
      <div className="min-w-full flex items-center justify-center">
        Loading . . .
      </div>
    );
  }

  return (
    <div className="min-w-full flex flex-col items-center justify-center">
      <h1>Datasets</h1>
      <ul>
        {datasets.map((ds) => (
          <li key={ds.id} className="flex">
            <div className="border rounded px-2 py-2 ">
              <span className="font-semibold">{ds.name}</span>,{ds.id},{" "}
              {ds.created_at}
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

export default DatasetsPage;
