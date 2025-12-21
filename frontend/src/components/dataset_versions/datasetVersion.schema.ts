import { z } from "zod";

export const DatasetVersionSchema = z.object({
  name: z.string().trim().min(1, "Dataset name is required"),
});

export type DatasetVersionInput = z.infer<typeof DatasetVersionSchema>;
