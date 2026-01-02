const API_URL = import.meta.env.VITE_API_URL || "http://localhost:42000";

export type Prediction = {
  id: string;
  name?: string;
  outputs_json: string;
  created_at: string;
};

export type PredictionListResponse = {
  items: Prediction[];
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

export type PredictionQueryParams = {
  page?: number;
  size?: number;
  sort?: string;
  dir?: "asc" | "desc";
  q?: string;
  id?: string;
  // name?: string;
};

export async function get_predictions(
  model_id: string,
  params: PredictionQueryParams = {}
): Promise<PredictionListResponse> {
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
    ? `${API_URL}/modelPredictions/${model_id}?${queryString}`
    : `${API_URL}/modelPredictions/${model_id}`;

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch predictions: ${res.status}`);
  }
  const data = await res.json();
  console.log(`predictions of ${model_id}:`, data);
  return data;
}

export async function get_prediction(
  prediction_id: string
): Promise<Prediction> {
  const res = await fetch(`${API_URL}/prediction/${prediction_id}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch prediction: ${res.status}`);
  }
  const data = await res.json();
  console.log("prediction:", data);
  return data;
}
