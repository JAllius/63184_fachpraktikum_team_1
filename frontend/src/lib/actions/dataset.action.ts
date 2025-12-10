const API_URL = import.meta.env.VITE_API_URL || "http://localhost:42000";

export type Dataset = {
  id: string;
  created_at: string;
};

export type DatasetListResponse = {
  items: Dataset[];
  page: number;
  size: number;
  total: number;
  total_pages: number;
  sort: string;
  dir: "asc" | "desc";
  q: string | null;
  id: string | null;
  name: string | null;
};

export type DatasetQueryParams = {
  page?: number;
  size?: number;
  sort?: string;
  dir?: "asc" | "desc";
  q?: string;
  id?: string;
  name?: string;
};

export async function get_datasets(
  params: DatasetQueryParams = {}
): Promise<DatasetListResponse> {
  const search = new URLSearchParams();

  if (params.page !== undefined) search.set("page", String(params.page));
  if (params.size !== undefined) search.set("size", String(params.size));
  if (params.sort !== undefined) search.set("sort", String(params.sort));
  if (params.dir !== undefined) search.set("dir", String(params.dir));
  if (params.q !== undefined) search.set("q", String(params.q));

  const queryString = search.toString();

  const url = queryString
    ? `${API_URL}/datasets?${queryString}`
    : `${API_URL}/datasets`;

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch datasets: ${res.status}`);
  }
  const data = await res.json();
  console.log("datasets:", data);
  return data;
}
