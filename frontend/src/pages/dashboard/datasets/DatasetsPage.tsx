import { useEffect, useState } from "react";
import {
  get_datasets,
  type Dataset,
  type DatasetListResponse,
} from "../../../lib/actions/datasets/dataset.action";
import { useSearchParams } from "react-router-dom";
import {
  DatasetDelete,
  DatasetsFilterbar,
  DatasetsTable,
  type DeleteTarget,
} from "@/components/datasets";
import { Pagination } from "@/components/table";

const DatasetsPage = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [seachParams] = useSearchParams();
  const [deleteTarget, setDeleteTarget] = useState<DeleteTarget>();
  const [openDelete, setOpenDelete] = useState(false);

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
        setTotalPages(data.total_pages);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    }
    loadDatasets();
  }, [q, id, name]);

  const askDelete = (id: string, name: string) => {
    setDeleteTarget({ id, name });
    setOpenDelete(true);
  };

  if (loading) {
    return (
      <div className="min-w-full flex items-center justify-center">
        Loading...
      </div>
    );
  }

  return (
    <div className="w-full pl-4">
      <div className="mx-auto w-full px-6">
        <h1>Datasets</h1>
        <p className="mt-1 mb-4 text-sm text-muted-foreground">
          Manage uploaded datasets.
        </p>
        <DatasetsFilterbar />
        <DatasetsTable datasets={datasets} askDelete={askDelete} />
        {/* <Pagination totalPages={totalPages} /> */}
        {totalPages > 1 && (
          <div className="mt-2 flex justify-center">
            <Pagination totalPages={totalPages} />
          </div>
        )}
        {deleteTarget && (
          <DatasetDelete
            target={deleteTarget}
            open={openDelete}
            onOpenChange={setOpenDelete}
          />
        )}
      </div>
    </div>
  );
};

export default DatasetsPage;
