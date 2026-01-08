import {
  DatasetVersionSchema,
  type DatasetVersionInput,
} from "@/components/dataset_versions";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:42000";

export type DatasetVersion = {
  id: string;
  name?: string;
  created_at: string;
  uri: string;
  profile_json: string;
};

export type DatasetVersionListResponse = {
  items: DatasetVersion[];
  page: number;
  size: number;
  total: number;
  total_pages: number;
  sort: string;
  dir: "asc" | "desc";
  q: string | null;
  id: string | null;
  // name: string | null;
};

export type DatasetVersionQueryParams = {
  page?: number;
  size?: number;
  sort?: string;
  dir?: "asc" | "desc";
  q?: string;
  id?: string;
  // name?: string;
};

export async function get_dataset_versions(
  dataset_id: string,
  params: DatasetVersionQueryParams = {}
): Promise<DatasetVersionListResponse> {
  const search = new URLSearchParams();

  if (params.page !== undefined) search.set("page", String(params.page));
  if (params.size !== undefined) search.set("size", String(params.size));
  if (params.sort !== undefined) search.set("sort", String(params.sort));
  if (params.dir !== undefined) search.set("dir", String(params.dir));
  if (params.q !== undefined) search.set("q", String(params.q));
  if (params.id !== undefined) search.set("id", String(params.id));
  // if (params.name !== undefined) search.set("name", String(params.name));

  const queryString = search.toString();

  const url = queryString
    ? `${API_URL}/datasetVersions/${dataset_id}?${queryString}`
    : `${API_URL}/datasetVersions/${dataset_id}`;

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch dataset_versions: ${res.status}`);
  }
  const data = await res.json();
  // console.log(`dataset_versions of ${dataset_id}:`, data);
  return data;
}

export async function get_dataset_version(
  dataset_version_id: string
): Promise<DatasetVersion> {
  const res = await fetch(`${API_URL}/datasetVersion/${dataset_version_id}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch dataset_version: ${res.status}`);
  }
  const data = await res.json();
  // console.log("dataset_version:", data);
  return data;
}

type CreateDatasetVersion = { ok: true } | { ok: false; error: string };

export async function create_dataset_version(
  req: unknown
): Promise<CreateDatasetVersion> {
  const parsed = DatasetVersionSchema.safeParse(req);
  if (!parsed.success) {
    return {
      ok: false,
      error: "Invalid parameters to create a dataset version.",
    };
  }

  const data: DatasetVersionInput = parsed.data;

  // "file_id" feature currently unavailable
  if (!data.file) {
    return { ok: false, error: "Please upload a CSV file." };
  }

  const form = new FormData();
  form.append("dataset_id", data.dataset_id);
  form.append("name", data.name ?? "unknown name");
  form.append("file", data.file);

  const url = `${API_URL}/datasetVersion`;

  try {
    const res = await fetch(url, {
      method: "POST",
      body: form,
    });
    if (!res.ok) {
      return {
        ok: false,
        error: `Create dataset version request failed (status ${res.status}).`,
      };
    }
    return { ok: true };
  } catch {
    return {
      ok: false,
      error: "Network error while creating dataset version.",
    };
  }
}
