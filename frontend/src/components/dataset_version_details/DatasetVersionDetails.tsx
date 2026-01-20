import type { Profile } from "@/pages/dashboard/dataset_versions/DatasetVersionDetailPage";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../ui/card";
import StatCard from "../ui/stat-card";
import ColumnBadges from "../ui/column-badges";
import { Button } from "../ui/button";
import ColumnsDetailsTable from "./column_details/ColumnsDetailsTable";
import Filterbar from "./column_details/Filterbar";
import { AlertTriangle } from "lucide-react";
import { Field, FieldError, FieldLabel } from "../ui/field";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { Input } from "../ui/input";
import { Controller, useForm } from "react-hook-form";

type Props = {
  profile: Profile;
};

const DatasetVersionDetails = ({ profile }: Props) => {
  const [tabValue, setTabValue] = useState("summary");
  const [editing, setEditing] = useState(false);
  const [columnsFilter, setColumnsFilter] = useState("");
  const nCols = profile.summary?.n_cols ?? 0;
  const nRows = profile.summary?.n_rows ?? 0;
  const missingPct = profile.summary?.missing_pct ?? 0;
  const missingValues = (missingPct * 100).toFixed(2).toString() + "%";
  const idCandidates = Object.entries(profile?.id_candidates) ?? [];
  const excludeSuggestions = Object.entries(profile?.exclude_suggestions) ?? [];
  // const leakageColumns = Object.entries(profile?.leakage_columns) ?? [];
  const warnings: string[] = Object.entries(profile.columns)
    .filter(([, meta]) => meta?.warning)
    .map(([col]) => col);

  const columnNames = Object.entries(profile.columns).map(([name]) => ({
    name: name,
  }));

  const filteredColumns = columnNames.filter((v) =>
    v.name.toLowerCase().includes(columnsFilter.toLowerCase()),
  );

  const {
    register,
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<string[]>({
    defaultValues: {
      columns: "",
    },
  });

  return (
    <div>
      <Tabs className="w-full" value={tabValue} onValueChange={setTabValue}>
        <TabsList className="w-full items-center justify-start gap-2">
          <TabsTrigger value="summary">Summary</TabsTrigger>
          <TabsTrigger value="columns">Columns</TabsTrigger>
        </TabsList>
        <TabsContent value="summary">
          <section>
            <h3 className="mt-8 mb-4 text-sm font-medium text-muted-foreground">
              Dataset Version Summary
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
              <StatCard label="Columns" value={nCols} />
              <StatCard label="Rows" value={nRows} />
              <StatCard label="Missing values" value={missingValues} />
            </div>
          </section>
          <section>
            <h3 className="mt-8 mb-4 text-sm font-medium text-muted-foreground">
              Column Analysis
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 items-stretch">
              <Card className="w-full h-full flex flex-col">
                <CardHeader>
                  <div className="flex items-center justify-between text-foreground">
                    <CardTitle>Suggested Exclusions</CardTitle>
                    {!editing ? (
                      <Button
                        className="h-6 px-2 py-0 text-xs"
                        variant={"default"}
                        onClick={() => setEditing(true)}
                      >
                        Edit
                      </Button>
                    ) : (
                      <div className="flex items-center gap-2">
                        <Button
                          className="h-6 min-w-[52px] px-2 py-0 text-xs"
                          variant={"default"}
                          onClick={() => {}}
                        >
                          Save
                        </Button>
                        <Button
                          className="h-6 min-w-[52px] px-2 py-0 text-xs"
                          variant={"secondary"}
                          onClick={() => setEditing(false)}
                        >
                          Cancel
                        </Button>
                      </div>
                    )}
                  </div>
                  <CardDescription className="font-normal italic text-xs">
                    Columns that are excluded by default when creating ML
                    problems.
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex flex-1 flex-col text-sm">
                  {!editing ? (
                    <ColumnBadges items={excludeSuggestions} />
                  ) : (
                    <form id="update-exclusions" onSubmit={() => {}}>
                      <Controller
                        name="columns"
                        control={control}
                        render={({ field }) => (
                          <Field data-invalid={!!errors.columns}>
                            <FieldLabel />
                            <Select
                              value={field.value}
                              onValueChange={() => {}}
                            >
                              <SelectTrigger
                                aria-invalid={!!errors.columns}
                                className="h-9 w-full justify-between text-left border rounded-md text-sm pl-3"
                              >
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <div className="sticky top-0 z-10 pb-1 border-b bg-popover">
                                  <Input
                                    placeholder="Filter columns"
                                    value={columnsFilter}
                                    onChange={(e) =>
                                      setColumnsFilter(e.target.value)
                                    }
                                    onKeyDown={(e) => e.stopPropagation()}
                                  />
                                </div>
                                {filteredColumns.map((c) => (
                                  <SelectItem key={c.name} value={c.name}>
                                    {c.name}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                            <FieldError
                              errors={
                                errors.columns ? [errors.columns] : undefined
                              }
                            />
                          </Field>
                        )}
                      />
                    </form>
                  )}
                </CardContent>
              </Card>
              <Card className="w-full h-full flex flex-col">
                <CardHeader>
                  <div className="flex items-center justify-between text-foreground">
                    <CardTitle>Identifier Columns</CardTitle>
                    <div className="h-6" />
                  </div>
                  <CardDescription className="font-normal italic text-xs">
                    Columns likely to act as unique identifiers and should
                    usually be excluded.
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex flex-1 flex-col text-sm">
                  <ColumnBadges items={idCandidates} />
                </CardContent>
              </Card>
              <Card className="w-full h-full flex flex-col">
                <CardHeader>
                  <div className="flex items-center justify-between text-foreground">
                    <CardTitle className="inline-flex items-center gap-2">
                      Warnings <AlertTriangle className="h-5 w-5" />
                    </CardTitle>
                    <div className="h-6" />
                  </div>
                  <CardDescription className="font-normal italic text-xs">
                    Columns that contain many distinct values and may require
                    special handling when used in a model.
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex flex-1 flex-col text-sm">
                  <ColumnBadges items={warnings} />
                </CardContent>
              </Card>
              {/* <Card className="w-full h-full flex flex-col">
                <CardHeader>
                  <div className="flex items-center justify-between text-foreground">
                    <CardTitle>Potential Data Leakage (manual)</CardTitle>
                    <Button
                      className="h-6 px-2 py-0 text-xs"
                      variant={"default"}
                    >
                      Edit
                    </Button>
                  </div>
                  <CardDescription className="font-normal italic text-xs">
                    Columns that may leak future information into the model.
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex flex-1 flex-col text-sm">
                  <ColumnBadges items={leakageColumns} />
                </CardContent>
              </Card> */}
            </div>
          </section>
        </TabsContent>
        <TabsContent value="columns">
          <Filterbar />
          <ColumnsDetailsTable columns={Object.entries(profile?.columns)} />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DatasetVersionDetails;
