import { z } from "zod";

export const ModelSchema = z.object({
  name: z.string().trim().min(1, "Model name is required"),
});

export type ModelInput = z.infer<typeof ModelSchema>;
