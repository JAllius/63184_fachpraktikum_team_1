import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { PredictFormSchema, type PredictFormInput } from "./predictForm.schema";
import { toast } from "sonner";
import {
  Sheet,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetOverlay,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import {
  Field,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldSet,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { post_predict } from "@/lib/actions/ml/prediction.action";

type Props = {
  problemId?: string;
  modelId?: string;
};

const Predict = ({ problemId, modelId }: Props) => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState(true);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setValue,
    unregister,
    reset,
  } = useForm<PredictFormInput>({
    resolver: zodResolver(PredictFormSchema),
    defaultValues: {
      input_json: "",
      input_uri: "",
      problem_id: problemId ?? "",
      model_id: modelId ?? "production",
    },
  });

  function handleInputToggle(checked: boolean) {
    setInput(checked);
    if (checked) {
      setValue("input_json", "");
      unregister("input_json");
    } else {
      setValue("input_uri", "");
      unregister("input_uri");
    }
  }

  async function onSubmit(data: PredictFormInput) {
    const res = await post_predict(data);
    if (!res.ok) {
      toast.error(res.error);
      return;
    }
    toast.success("Prediction started");
    setOpen(false);
    reset({
      input_json: "",
      input_uri: "",
      problem_id: problemId ?? "",
      model_id: modelId ?? "production",
    });
  }

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button className="hover:scale-105 active:scale-95">Predict</Button>
      </SheetTrigger>
      <SheetContent
        className="flex h-full flex-col"
        onOpenAutoFocus={(e) => e.preventDefault()}
      >
        <SheetHeader>
          <SheetTitle>Predict</SheetTitle>
        </SheetHeader>

        <form
          id="predict_form"
          onSubmit={handleSubmit(onSubmit)}
          className="mt-6 space-y-6"
        >
          <FieldSet>
            <FieldGroup>
              <div className="flex gap-2">
                <span>Json</span>
                <Switch
                  checked={input}
                  onCheckedChange={handleInputToggle}
                  className="shrink-0 w-9"
                />
                <span>Uri</span>
              </div>
              {/* JSON Input */}
              {!input && (
                <Field data-invalid={!!errors.input_json}>
                  <FieldLabel htmlFor="input_json">Json Input</FieldLabel>
                  <Input
                    id="input_json"
                    aria-invalid={!!errors.input_json}
                    {...register("input_json")}
                  />
                  <FieldError
                    errors={errors.input_json ? [errors.input_json] : undefined}
                  />
                </Field>
              )}
              {/* URI Input */}
              {input && (
                <Field data-invalid={!!errors.input_uri}>
                  <FieldLabel htmlFor="input_uri">Uri Input</FieldLabel>
                  <Input
                    id="input_uri"
                    aria-invalid={!!errors.input_uri}
                    {...register("input_uri")}
                  />
                  <FieldError
                    errors={errors.input_uri ? [errors.input_uri] : undefined}
                  />
                </Field>
              )}
              {/* Problem id */}
              <Field data-invalid={!!errors.problem_id}>
                <FieldLabel htmlFor="problem_id">Problem id</FieldLabel>
                <Input
                  id="problem_id"
                  disabled={!!problemId}
                  aria-invalid={!!errors.problem_id}
                  readOnly={!!problemId}
                  defaultValue={problemId ?? ""}
                  {...register("problem_id")}
                />
                <FieldError
                  errors={errors.problem_id ? [errors.problem_id] : undefined}
                />
              </Field>
              {/* Model id */}
              <Field data-invalid={!!errors.model_id}>
                <FieldLabel htmlFor="problem_id">Model id</FieldLabel>
                <Input
                  id="model_id"
                  disabled={!!modelId}
                  aria-invalid={!!errors.model_id}
                  readOnly={!!modelId}
                  defaultValue={modelId ?? ""}
                  {...register("model_id")}
                />
                <FieldError
                  errors={errors.model_id ? [errors.model_id] : undefined}
                />
              </Field>
            </FieldGroup>
          </FieldSet>
        </form>
        <SheetFooter className="mt-auto">
          <Button
            variant="outline"
            onClick={() => setOpen(false)}
            className="w-20 hover:scale-105 active:scale-95"
          >
            Cancel
          </Button>
          <Button
            type="submit"
            form="predict_form"
            disabled={isSubmitting}
            className="w-20 hover:scale-105 active:scale-95"
          >
            {isSubmitting ? "Sending..." : "Predict"}
          </Button>
        </SheetFooter>
      </SheetContent>
      <SheetOverlay className="bg-black/30 backdrop-blur-sm" />
    </Sheet>
  );
};

export default Predict;
