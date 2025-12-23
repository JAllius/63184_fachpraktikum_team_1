import { z } from "zod";

export const DatasetVersionSchema = z.object({
  // name: z.string().trim().min(1, "Dataset version name is required"),
  dataset_id: z.string().trim().min(1, "Dataset id is required"),
  file: z.instanceof(File).optional(),
  file_id: z.string().optional(),
});

export type DatasetVersionInput = z.infer<typeof DatasetVersionSchema>;
