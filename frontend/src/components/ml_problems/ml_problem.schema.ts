import { z } from "zod";

export const MLProblemSchema = z.object({
  // name: z.string().trim().min(1, "ML problem name is required"),
  name: z.string().trim().optional(),
  dataset_version_id: z
    .string()
    .trim()
    .min(1, "Dataset version id is required"),
  task: z.string().trim().min(1, "Task definition is required"),
  target: z.string().trim().min(1, "Target column is required"),
});

export type MLProblemInput = z.infer<typeof MLProblemSchema>;
