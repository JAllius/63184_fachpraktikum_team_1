const API_URL = import.meta.env.VITE_API_URL || "http://localhost:42000";

export type Model = {
  id: string;
  name: string;
  algorithm: string;
  train_mode: string;
  evaluation_strategy: string;
  status: "staging" | "production" | "archived";
  metrics_json: string;
  metadata_json: string;
  created_at: string;
};

export type ModelListResponse = {
  items: Model[];
  page: number;
  size: number;
  total: number;
  total_pages: number;
  sort: string;
  dir: "asc" | "desc";
  q: string | null;
  id: string | null;
  name: string | null;
  algorithm: string | null;
  train_mode: string | null;
  evaluation_strategy: string | null;
  status: string | null;
};

export type ModelQueryParams = {
  page?: number;
  size?: number;
  sort?: string;
  dir?: "asc" | "desc";
  q?: string;
  id?: string;
  name?: string;
  algorithm?: string;
  train_mode?: string;
  evaluation_strategy?: string;
  status?: string | null;
};

export async function get_models(
  problem_id: string,
  params: ModelQueryParams = {}
): Promise<ModelListResponse> {
  const search = new URLSearchParams();

  if (params.page !== undefined) search.set("page", String(params.page));
  if (params.size !== undefined) search.set("size", String(params.size));
  if (params.sort !== undefined) search.set("sort", String(params.sort));
  if (params.dir !== undefined) search.set("dir", String(params.dir));
  if (params.q !== undefined) search.set("q", String(params.q));
  if (params.id !== undefined) search.set("id", String(params.id));
  if (params.name !== undefined) search.set("name", String(params.name));
  if (params.algorithm !== undefined)
    search.set("algorithm", String(params.algorithm));
  if (params.train_mode !== undefined)
    search.set("train_mode", String(params.train_mode));
  if (params.evaluation_strategy !== undefined)
    search.set("evaluation_strategy", String(params.evaluation_strategy));
  if (params.status !== undefined) search.set("status", String(params.status));

  const queryString = search.toString();

  const url = queryString
    ? `${API_URL}/problemModels/${problem_id}?${queryString}`
    : `${API_URL}/problemModels/${problem_id}`;

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch models: ${res.status}`);
  }
  const data = await res.json();
  console.log(`models of ${problem_id}:`, data);
  return data;
}

export async function get_model(model_id: string): Promise<Model> {
  const res = await fetch(`${API_URL}/model/${model_id}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch model: ${res.status}`);
  }
  const data = await res.json();
  console.log("model:", data);
  return data;
}
