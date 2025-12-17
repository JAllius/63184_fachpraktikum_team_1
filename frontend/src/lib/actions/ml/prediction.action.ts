import {
  PredictFormSchema,
  type PredictFormInput,
} from "@/components/ml/predict/predictForm.schema";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:42000";

type PredictResponse = { ok: true } | { ok: false; error: string };

export async function post_predict(req: unknown): Promise<PredictResponse> {
  const parsed = PredictFormSchema.safeParse(req);
  if (!parsed.success) {
    return {
      ok: false,
      error: "Invalid predict parameters.",
    };
  }

  const data: PredictFormInput = parsed.data;

  const qs = new URLSearchParams();

  if (data.input_json) qs.set("input_json", data.input_json);
  if (data.input_uri) qs.set("input_uri", data.input_uri);
  if (data.problem_id) qs.set("problem_id", data.problem_id);
  if (data.model_id) qs.set("model_id", data.model_id);

  const queryString = qs.toString();

  const url = `${API_URL}/predict?${queryString}`;

  try {
    // const res = await fetch(url, {
    //   method: "POST",
    // });
    const res = await fetch(url, { method: "POST" });
    if (!res.ok) {
      return {
        ok: false,
        error: `Prediction request failed (status ${res.status}).`,
      };
    }
    return { ok: true };
  } catch {
    return { ok: false, error: "Network error while starting prediction." };
  }
}
