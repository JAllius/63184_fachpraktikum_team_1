import type { MLProblem } from "@/lib/actions/mlProblems/mlProblem.action";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../ui/card";
import { Button } from "../ui/button";
import { Link } from "react-router-dom";
import { ChevronDown, ChevronUp, FileText } from "lucide-react";
import type { FeatureStrategy } from "@/pages/dashboard/ml_problems/MLProblemDetailPage";
import ColumnBadges from "../ui/column-badges";
import { useState } from "react";

type Props = {
  datasetId: string;
  datasetVersionId: string;
  datasetVersionName?: string;
  mlProblem: MLProblem;
  featureStrategy: FeatureStrategy;
  prodModelName?: string;
  prodModelId?: string;
};

const MLProblemDetails = ({
  datasetId,
  datasetVersionId,
  datasetVersionName,
  mlProblem,
  featureStrategy,
  prodModelName,
  prodModelId,
}: Props) => {
  const [openTechnical, setOpenTechnical] = useState(false);

  const semanticTypesJSON = JSON.parse(mlProblem.semantic_types);
  const semanticTypes: [string, string][] = Object.entries(semanticTypesJSON);
  const groupedSemanticTypes = semanticTypes.reduce((acc, [col, type]) => {
    if (col === mlProblem?.target) return acc; // skip target column

    (acc[type] ??= []).push([col, col]);
    return acc;
  }, {} as Record<string, [string, string][]>);

  return (
    <div>
      <section>
        <h3 className="mt-8 mb-4 text-sm font-medium text-muted-foreground">
          ML Problem Summary
        </h3>
        <Card className="w-full h-full flex flex-col text-foreground">
          <CardHeader>
            <CardTitle>{mlProblem.name ?? "Unknown ML Problem"}</CardTitle>
          </CardHeader>
          <CardDescription />
          <CardContent className="flex flex-1 flex-col text-sm">
            <div>
              <span className="text-muted-foreground/80">Task: </span>
              <span className="capitalize">{mlProblem.task}</span>
            </div>
            <div>
              <span className="text-muted-foreground/80">Target: </span>
              <span>{mlProblem.target}</span>
            </div>
            <div>
              <span className="text-muted-foreground/80">
                Dataset Version:{" "}
              </span>
              <Link
                to={`../datasets/${datasetId}/${datasetVersionId}`}
                aria-label="View dataset version"
                className="inline-flex items-center gap-1 group"
              >
                <span>{datasetVersionName ?? "Unknown Dataset Version"}</span>
                <FileText className="w-3 h-3 group-hover:text-sky-400 group-hover:scale-105 active:scale-95" />
              </Link>
            </div>
            <div>
              <span className="text-muted-foreground/80">Created: </span>
              <span className="capitalize">{mlProblem.created_at}</span>
            </div>
            {prodModelId && (
              <div>
                <span className="text-muted-foreground/80">
                  Production Model:{" "}
                </span>
                <Link
                  to={`${prodModelId}`}
                  aria-label="View dataset version"
                  className="inline-flex items-center gap-1 group"
                >
                  <span className="capitalize">
                    {prodModelName ?? "Unknown Model"}
                  </span>
                  <FileText className="w-3 h-3 group-hover:text-sky-400 group-hover:scale-105 active:scale-95" />
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </section>
      <section>
        <div className="mt-8 mb-4 flex items-center gap-6">
          <h3 className="text-sm font-medium text-muted-foreground">
            Feature Strategy
          </h3>
          <Button className="h-6 px-2 py-0 text-xs" variant={"default"}>
            Reset to default
          </Button>
        </div>
        <div className="flex items-center justify-between gap-6">
          <Card className="w-full h-full flex flex-col text-foreground">
            <CardHeader>
              <div className="flex items-center justify-between text-foreground">
                <CardTitle>Include</CardTitle>
                <Button className="h-6 px-2 py-0 text-xs" variant={"default"}>
                  Edit
                </Button>
              </div>
            </CardHeader>
            <CardDescription />
            <CardContent className="flex flex-1 flex-col text-sm">
              <ColumnBadges
                items={featureStrategy.include}
                className="grid-cols-2 sm:grid-cols-3 lg:grid-cols-5"
              />
            </CardContent>
          </Card>
          <Card className="w-full h-full flex flex-col text-foreground">
            <CardHeader>
              <div className="flex items-center justify-between text-foreground">
                <CardTitle>Exclude</CardTitle>
                <Button className="h-6 px-2 py-0 text-xs" variant={"default"}>
                  Edit
                </Button>
              </div>
            </CardHeader>
            <CardDescription />
            <CardContent className="flex flex-1 flex-col text-sm">
              <ColumnBadges
                items={featureStrategy.exclude}
                className="grid-cols-2 sm:grid-cols-3 lg:grid-cols-5"
              />
            </CardContent>
          </Card>
        </div>
      </section>
      <section>
        <Button
          variant={"ghost"}
          className="mt-7 mb-3.5 -ml-3 font-semibold text-lg flex items-center justify-center"
          size="sm"
          onClick={() => {
            setOpenTechnical((v) => !v);
          }}
        >
          <h3 className="text-sm font-medium text-muted-foreground">
            Technical Information
          </h3>
          {openTechnical ? <ChevronDown /> : <ChevronUp />}
        </Button>
        {openTechnical && (
          <Card className="w-full h-full flex flex-col text-foreground">
            <CardHeader>
              <CardTitle>Training features</CardTitle>
            </CardHeader>
            <CardDescription />
            <CardContent className="flex flex-1 flex-col text-sm space-y-4">
              {Object.entries(groupedSemanticTypes).map(([group, items]) => (
                <div key={group} className="space-y-2">
                  <div className="capitalize text-muted-foreground font-semibold">
                    {group} features ({items.length})
                  </div>
                  <ColumnBadges
                    items={items}
                    className="grid-cols-3 sm:grid-cols-5 lg:grid-cols-8"
                  />
                </div>
              ))}
            </CardContent>
          </Card>
        )}
      </section>
    </div>
  );
};

export default MLProblemDetails;
