import { useRef, useState } from "react";
import { Controller, useForm } from "react-hook-form";
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Trash } from "lucide-react";
import { cn } from "@/lib/utils";

type Props = {
  problemId?: string;
  modelId?: string;
};

type Mode = "new" | "existing" | "json";

const Predict = ({ problemId, modelId }: Props) => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState(true);
  const [mode, setMode] = useState<Mode>("new");
  const [hasFile, setHasFile] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const {
    register,
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
    setValue,
    unregister,
    reset,
  } = useForm<PredictFormInput>({
    resolver: zodResolver(PredictFormSchema),
    defaultValues: {
      input_csv: undefined,
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

  function clearInputFile() {
    setValue("input_csv", undefined);
    setHasFile(false);
    if (inputRef.current) inputRef.current.value = "";
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
              {/* Data File */}
              <FieldLabel>Data File</FieldLabel>
              <Tabs
                value={mode}
                onValueChange={(v) => {
                  const next = v as Mode;
                  setMode(next);
                  if (next === "new") {
                    setValue("input_json", "");
                    setValue("input_uri", "");
                  } else if (next === "existing") {
                    clearInputFile();
                    setValue("input_json", "");
                  } else {
                    clearInputFile();
                    setValue("input_uri", "");
                  }
                }}
                className="-mt-4"
              >
                <TabsList>
                  <TabsTrigger value="new">New</TabsTrigger>
                  <TabsTrigger value="existing">Existing</TabsTrigger>
                  <TabsTrigger value="json">JSON</TabsTrigger>
                </TabsList>
                <TabsContent value="new">
                  {/* Upload CSV */}
                  <Field data-invalid={!!errors.input_csv}>
                    <div className="flex gap-2 items-center">
                      <Controller
                        name="input_csv"
                        control={control}
                        render={({ field }) => (
                          <Input
                            ref={inputRef}
                            id="file"
                            type="file"
                            accept=".csv,text/csv"
                            multiple={false}
                            aria-invalid={!!errors.input_csv}
                            onChange={(e) => {
                              const f = e.target.files?.[0];
                              field.onChange(f);
                              setHasFile(!!f);
                            }}
                            className={cn(
                              "text-sm",
                              "px-3",
                              "text-muted-foreground",
                              "file:mr-1",
                              "file:px-0",
                              "file:h-9",
                              "file:pb-3",
                              "file:rounded-md",
                              "file:border-0",
                              "file:bg-transparent",
                              "file:text-sm",
                              "file:font-medium",
                              "file:text-muted-foreground"
                            )}
                          />
                        )}
                      />
                      {hasFile && (
                        <Button
                          type="button"
                          variant={"outline"}
                          onClick={clearInputFile}
                          className="h-9 w-9 shrink-0"
                        >
                          <Trash className="text-red-500" />
                        </Button>
                      )}
                    </div>
                    <FieldError
                      errors={errors.input_csv ? [errors.input_csv] : undefined}
                    />
                  </Field>
                </TabsContent>
                <TabsContent value="existing">
                  {/* Choose existing CSV */}
                  <Controller
                    name="input_uri"
                    control={control}
                    render={({ field }) => (
                      <Field data-invalid={!!errors.input_uri}>
                        <Select
                          value={field.value}
                          onValueChange={field.onChange}
                        >
                          <SelectTrigger
                            aria-invalid={!!errors.input_uri}
                            className="h-9 w-full justify-between text-left border rounded-md text-sm pl-3"
                          >
                            <SelectValue placeholder="Choose an existing file" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="aaa" disabled={true}>
                              Unavailable Feature!
                            </SelectItem>
                          </SelectContent>
                        </Select>
                        <FieldError
                          errors={
                            errors.input_uri ? [errors.input_uri] : undefined
                          }
                        />
                      </Field>
                    )}
                  />
                </TabsContent>
                <TabsContent value="json">
                  <Field data-invalid={!!errors.input_json}>
                    <Input
                      id="input_json"
                      aria-invalid={!!errors.input_json}
                      {...register("input_json")}
                    />
                    <FieldError
                      errors={
                        errors.input_json ? [errors.input_json] : undefined
                      }
                    />
                  </Field>
                </TabsContent>
              </Tabs>
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
