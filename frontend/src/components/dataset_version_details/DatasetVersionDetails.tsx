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
import StatCard from "./StatCard";
import ColumnBadges from "./ColumnBadges";
import { Button } from "../ui/button";

type Props = {
  profile: Profile;
};

const DatasetVersionDetails = ({ profile }: Props) => {
  const [tabValue, setTabValue] = useState("summary");
  const nCols = profile.summary?.n_cols ?? 0;
  const nRows = profile.summary?.n_rows ?? 0;
  const missingPct = profile.summary?.missing_pct ?? 0;
  const missingValues = (missingPct * 100).toFixed(2).toString() + "%";
  const idCandidates = Object.entries(profile?.id_candidates) ?? [];
  const excludeSuggestions = Object.entries(profile?.exclude_suggestions) ?? [];
  const leakageColumns = Object.entries(profile?.leakage_columns) ?? [];

  return (
    <div>
      <Tabs className="w-full" value={tabValue} onValueChange={setTabValue}>
        <TabsList className="w-full items-center justify-start gap-2">
          <TabsTrigger value="summary">Summary</TabsTrigger>
          <TabsTrigger value="columns">Columns</TabsTrigger>
        </TabsList>
        <TabsContent value="summary">
          <h3 className="mt-8 mb-4 text-sm font-medium text-muted-foreground">
            Dataset Summary
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            <StatCard label="Columns" value={nCols} />
            <StatCard label="Rows" value={nRows} />
            <StatCard label="Missing values" value={missingValues} />
          </div>
          <h3 className="mt-8 mb-4 text-sm font-medium text-muted-foreground">
            Column analysis
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 items-stretch">
            <Card className="w-full h-full flex flex-col">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Suggested Exclusions</CardTitle>
                  <Button className="h-6 px-2 py-0 text-xs" variant={"default"}>
                    Edit
                  </Button>
                </div>
                <CardDescription className="font-normal italic text-xs">
                  Columns that are excluded by default when creating ML
                  problems.
                </CardDescription>
              </CardHeader>
              <CardContent className="flex flex-1 flex-col text-sm">
                <ColumnBadges items={excludeSuggestions} />
              </CardContent>
            </Card>
            <Card className="w-full h-full flex flex-col">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Identifier Columns</CardTitle>
                  <div className="h-6" />
                </div>
                <CardDescription className="font-normal italic text-xs">
                  Columns likely to act as unique identifiers and should usually
                  be excluded.
                </CardDescription>
              </CardHeader>
              <CardContent className="flex flex-1 flex-col text-sm">
                <ColumnBadges items={idCandidates} />
              </CardContent>
            </Card>
            <Card className="w-full h-full flex flex-col">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Potential Data Leakage (manual)</CardTitle>
                  <Button className="h-6 px-2 py-0 text-xs" variant={"default"}>
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
            </Card>
          </div>
        </TabsContent>
        <TabsContent value="columns">
          <div className="flex flex-col gap-2">
            {Object.entries(profile?.columns).map((r) => (
              <div>{JSON.stringify(r)}</div>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DatasetVersionDetails;
