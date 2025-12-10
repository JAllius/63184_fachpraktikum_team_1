const API_URL = import.meta.env.VITE_API_URL || "http://localhost:42000";

export type DatasetVersion = {
  id: string;
  created_at: string;
};

export async function get_dataset_versions(
  dataset_id: string
): Promise<DatasetVersion[]> {
  const res = await fetch(`${API_URL}/dataset/${dataset_id}/versions`);
  if (!res.ok) {
    throw new Error(`Failed to fetch dataset_versions: ${res.status}`);
  }
  const data = await res.json();
  console.log(`dataset_versions for ${dataset_id}:`, data);
  return data;
}

export type MLProblem = {
  id: string;
  created_at: string;
};

export async function get_ml_problems(
  dataset_version_id: string
): Promise<MLProblem[]> {
  const res = await fetch(`${API_URL}/dataset/${dataset_version_id}/problems`);
  if (!res.ok) {
    throw new Error(`Failed to fetch ml_problems: ${res.status}`);
  }
  const data = await res.json();
  console.log(`ml problems for ${dataset_version_id}:`, data);
  return data;
}
