import { useParams, useSearchParams } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";
import {
  get_dataset_versions,
  type DatasetVersion,
  type DatasetVersionListResponse,
} from "../../../lib/actions/dataset_versions/datasetVersion.action";
import {
  get_dataset,
  type Dataset,
} from "../../../lib/actions/datasets/dataset.action";
import {
  DatasetVersionCreate,
  DatasetVersionDelete,
  DatasetVersionsFilterbar,
  DatasetVersionsTable,
  DatasetVersionUpdate,
  type DeleteTarget,
  type UpdateTarget,
} from "@/components/dataset_versions";
import { PageSize, Pagination } from "@/components/table";
// import { Edit } from "lucide-react";

const DatasetIdPage = () => {
  const params = useParams<{ datasetId: string }>();
  if (!params.datasetId) {
    throw new Error("datasetId param missing");
  }
  const datasetId = params.datasetId;

  const [datasetVersions, setDatasetVersions] = useState<DatasetVersion[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const [dataset, setDataset] = useState<Dataset | null>(null);
  const [totalPages, setTotalPages] = useState(0);
  const [deleteTarget, setDeleteTarget] = useState<DeleteTarget | null>(null);
  const [openDelete, setOpenDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [updateTarget, setUpdateTarget] = useState<UpdateTarget | null>(null);
  const [openUpdate, setOpenUpdate] = useState(false);

  const page = Number(searchParams.get("page") ?? 1);
  const size = Number(searchParams.get("size") ?? 20);
  const sort = searchParams.get("sort") ?? "created_at";
  const dir = ((searchParams.get("dir") as "asc") || "desc") ?? "desc";
  const q = searchParams.get("q") || "";
  const id = searchParams.get("id") || "";
  // const name = searchParams.get("name") || "";

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

  const loadDatasetVersions = useCallback(async () => {
    try {
      const data: DatasetVersionListResponse = await get_dataset_versions(
        datasetId,
        {
          page,
          size,
          sort,
          dir,
          q: q || undefined,
          id: id || undefined,
          // name: name || undefined,
        }
      );
      setDatasetVersions(data.items);
      setTotalPages(data.total_pages);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [datasetId, page, size, sort, dir, q, id]); // name

  useEffect(() => {
    loadDatasetVersions();
  }, [loadDatasetVersions]);

  const askDelete = (id: string, name?: string) => {
    setDeleteTarget({ id, name });
    setOpenDelete(true);
  };

  const cancelDelete = () => {
    setOpenDelete(false);
    setDeleteTarget(null);
  };

  const onDelete = async () => {
    if (!deleteTarget) return;
    setDeleting(true);
    try {
      console.log("Deleting");
      await loadDatasetVersions();
    } catch (error) {
      console.log(error);
    } finally {
      console.log("Done");
      cancelDelete();
      setDeleting(false);
    }
  };

  const askUpdate = (id: string, name?: string) => {
    setUpdateTarget({ id, name });
    setOpenUpdate(true);
  };

  const cancelUpdate = () => {
    setOpenUpdate(false);
    setUpdateTarget(null);
  };

  const onUpdate = async () => {
    if (!updateTarget) return;
    try {
      console.log("Updating");
      await loadDatasetVersions();
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
        <div className="flex flex-inline items-center gap-2">
          <h1>Dataset details: {dataset?.name}</h1>
        </div>

        <p className="mt-1 mb-4 text-sm text-muted-foreground">
          Manage all dataset versions of {dataset?.name}.
        </p>
        <div className="flex justify-between">
          <div className="relative">
            <DatasetVersionsFilterbar />
          </div>
          <DatasetVersionCreate
            onCreate={loadDatasetVersions}
            datasetId={datasetId}
          />
        </div>
        <DatasetVersionsTable
          datasetVersions={datasetVersions}
          askDelete={askDelete}
          askUpdate={askUpdate}
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
          <DatasetVersionDelete
            target={deleteTarget}
            open={openDelete}
            onConfirm={onDelete}
            onCancel={cancelDelete}
            deleting={deleting}
          />
        )}
        {updateTarget && (
          <DatasetVersionUpdate
            target={updateTarget}
            open={openUpdate}
            onConfirm={onUpdate}
            onCancel={cancelUpdate}
          />
        )}
      </div>
    </div>
  );
};

export default DatasetIdPage;
