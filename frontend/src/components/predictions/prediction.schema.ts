import { z } from "zod";

export const PredictionSchema = z.object({
  // name: z.string().trim().min(1, "Dataset version name is required"),
});

export type PredictionInput = z.infer<typeof PredictionSchema>;
