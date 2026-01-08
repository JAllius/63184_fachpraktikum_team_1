import { MLProblemSchema, type MLProblemInput } from "@/components/ml_problems";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:42000";

export type MLProblem = {
  id: string;
  name?: string;
  task: string;
  target: string;
  feature_strategy: string;
  semantic_types: string;
  created_at: string;
};

export type MLProblemListResponse = {
  items: MLProblem[];
  page: number;
  size: number;
  total: number;
  total_pages: number;
  sort: string;
  dir: "asc" | "desc";
  q: string | null;
  id: string | null;
  task: string | null;
  target: string | null;
  // name: string | null;
};

export type MLProblemQueryParams = {
  page?: number;
  size?: number;
  sort?: string;
  dir?: "asc" | "desc";
  q?: string;
  id?: string;
  task?: string;
  target?: string;
  // name?: string;
};

export async function get_ml_problems(
  dataset_version_id: string,
  params: MLProblemQueryParams = {}
): Promise<MLProblemListResponse> {
  const search = new URLSearchParams();

  if (params.page !== undefined) search.set("page", String(params.page));
  if (params.size !== undefined) search.set("size", String(params.size));
  if (params.sort !== undefined) search.set("sort", String(params.sort));
  if (params.dir !== undefined) search.set("dir", String(params.dir));
  if (params.q !== undefined) search.set("q", String(params.q));
  if (params.id !== undefined) search.set("id", String(params.id));
  if (params.task !== undefined) search.set("task", String(params.task));
  if (params.target !== undefined) search.set("target", String(params.target));
  // if (params.name !== undefined) search.set("name", String(params.name));

  const queryString = search.toString();

  const url = queryString
    ? `${API_URL}/datasetVersionProblems/${dataset_version_id}?${queryString}`
    : `${API_URL}/datasetVersionProblems/${dataset_version_id}`;

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch ml_problems: ${res.status}`);
  }
  const data = await res.json();
  // console.log(`ml_problems of ${dataset_version_id}:`, data);
  return data;
}

export async function get_ml_problem(problem_id: string): Promise<MLProblem> {
  const res = await fetch(`${API_URL}/problem/${problem_id}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch ml_problem: ${res.status}`);
  }
  const data = await res.json();
  // console.log("ml_problem:", data);
  return data;
}

type CreateMLProblem = { ok: true } | { ok: false; error: string };

export async function create_ml_problem(
  req: unknown
): Promise<CreateMLProblem> {
  const parsed = MLProblemSchema.safeParse(req);
  if (!parsed.success) {
    return {
      ok: false,
      error: "Invalid parameters to create an ML problem.",
    };
  }

  const data: MLProblemInput = parsed.data;

  const qs = new URLSearchParams({
    name: data.name ?? "unknown name",
    dataset_version_id: data.dataset_version_id,
    task: data.task,
    target: data.target,
  });

  const url = `${API_URL}/problem?${qs}`;

  try {
    const res = await fetch(url, {
      method: "POST",
    });
    if (!res.ok) {
      return {
        ok: false,
        error: `Create ML problem request failed (status ${res.status}).`,
      };
    }
    return { ok: true };
  } catch {
    return { ok: false, error: "Network error while creating ML Problem." };
  }
}
