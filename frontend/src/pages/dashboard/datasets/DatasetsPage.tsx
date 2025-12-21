import { useCallback, useEffect, useState } from "react";
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
  DatasetUpdate,
  type DeleteTarget,
  type UpdateTarget,
} from "@/components/datasets";
import { PageSize, Pagination } from "@/components/table";

const DatasetsPage = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
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
  const name = searchParams.get("name") || "";

  const loadDatasets = useCallback(async () => {
    try {
      const data: DatasetListResponse = await get_datasets({
        page,
        size,
        sort,
        dir,
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
  }, [page, size, sort, dir, q, id, name]);

  useEffect(() => {
    loadDatasets();
  }, [loadDatasets]);

  const askDelete = (id: string, name: string) => {
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
      await loadDatasets();
    } catch (error) {
      console.log(error);
    } finally {
      console.log("Done");
      cancelDelete();
      setDeleting(false);
    }
  };

  const askUpdate = (id: string, name: string) => {
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
      await loadDatasets();
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
        <h1>Datasets</h1>
        <p className="mt-1 mb-4 text-sm text-muted-foreground">
          Manage all datasets.
        </p>
        <DatasetsFilterbar onCreate={loadDatasets} />
        <DatasetsTable
          datasets={datasets}
          askDelete={askDelete}
          askUpdate={askUpdate}
        />
        {/* <Pagination totalPages={totalPages} /> */}
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
          <DatasetDelete
            target={deleteTarget}
            open={openDelete}
            onConfirm={onDelete}
            onCancel={cancelDelete}
            deleting={deleting}
          />
        )}
        {updateTarget && (
          <DatasetUpdate
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

export default DatasetsPage;
