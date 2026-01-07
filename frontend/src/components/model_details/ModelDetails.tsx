import { ChevronDown, ChevronUp, FileText } from "lucide-react";
import { Link } from "react-router-dom";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../ui/card";
import StatCard from "../ui/stat-card";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import { useState } from "react";
import ColumnBadges from "../ui/column-badges";

type Props = {
  status: string;
  datasetId: string;
  datasetVersionId: string;
  mlProblemId: string;
  mlProblemName?: string;
  created_at: string;
  metadata: {
    model_name?: string;
    task: string; // Regression
    target: string;
    preset: string;
    version: string;
    framework: string;
    algorithm: string;
    train_mode: string;
    random_seed: number;
    metrics: {
      accuracy: number;
      precision: number;
      recall: number;
      f1: number;
    };
    semantic_types: Record<string, string[]>;
    cross_validation?: { mean: number; std: number };
  };
};

const ModelDetails = ({
  status,
  datasetId,
  datasetVersionId,
  mlProblemId,
  mlProblemName,
  created_at,
  metadata,
}: Props) => {
  const [openTechnical, setOpenTechnical] = useState(false);

  const semanticTypes = metadata.semantic_types;

  const groupedSemanticTypes = Object.fromEntries(
    Object.entries(semanticTypes)
      .filter(([, cols]) => cols.length > 0)
      .map(([type, cols]) => [type, cols.map((c) => [c, c])])
  ) as Record<string, [string, string][]>;

  return (
    <div>
      <section>
        <h3 className="mt-8 mb-4 text-sm font-medium text-muted-foreground">
          Metrics
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            label="Accuracy"
            value={metadata.metrics.accuracy.toFixed(3)}
            tooltip="Percentage of correct predictions overall."
          />
          <StatCard
            label="Precision"
            value={metadata.metrics.precision.toFixed(3)}
            tooltip="Percentage of positive predictions that are correct."
          />
          <StatCard
            label="Recall"
            value={metadata.metrics.recall.toFixed(3)}
            tooltip="Percentage of actual positives that are correctly identified."
          />
          {metadata?.cross_validation ? (
            <StatCard
              label="F1 score"
              value={metadata.metrics.f1.toFixed(3)}
              secondaryValue={`CV ${metadata?.cross_validation?.mean.toFixed(
                3
              )}±${metadata?.cross_validation?.std.toFixed(3)}`}
              tooltip={
                "Percentage-based balance between precision and recall.\nCV shows average and variation across folds."
              }
            />
          ) : (
            <StatCard
              label="F1 score"
              value={metadata.metrics.f1.toFixed(3)}
              tooltip="Percentage-based balance between precision and recall."
            />
          )}
        </div>
      </section>
      <section>
        <h3 className="mt-8 mb-4 text-sm font-medium text-muted-foreground">
          Model Details
        </h3>
        <Card className="w-full h-full flex flex-col text-foreground">
          <CardHeader>
            <CardTitle>
              <div className="flex items-center gap-2">
                {metadata?.model_name ?? "Unknown Model"}
                {status === "production" ? (
                  <Badge variant={"default"}>{status}</Badge>
                ) : (
                  <Badge variant={"secondary"}>{status}</Badge>
                )}
                {status !== "production" && (
                  <Button className="h-5 px-2 text-xs" variant={"default"}>
                    Set to production
                  </Button>
                )}
              </div>
            </CardTitle>
          </CardHeader>
          <CardDescription />
          <CardContent className="flex flex-1 text-sm">
            <div className="w-1/2">
              <div>
                <span className="text-muted-foreground/80">Task: </span>
                <span className="capitalize">{metadata.task}</span>
              </div>
              <div>
                <span className="text-muted-foreground/80">Target: </span>
                <span>{metadata.target}</span>
              </div>
              <div>
                <span className="text-muted-foreground/80">ML Problem: </span>
                <Link
                  to={`../datasets/${datasetId}/${datasetVersionId}/${mlProblemId}`}
                  aria-label="View ML problem"
                  className="inline-flex items-center gap-1 group"
                >
                  <span>{mlProblemName ?? "Unknown ML Problem"}</span>
                  <FileText className="w-3 h-3 group-hover:text-sky-400 group-hover:scale-105 active:scale-95" />
                </Link>
              </div>
              <div>
                <span className="text-muted-foreground/80">Created: </span>
                <span className="capitalize">{created_at}</span>
              </div>
            </div>
            <div className="w-1/2">
              {/*
              Evaluation: evaluation_strategy
              */}
              <div>
                <span className="text-muted-foreground/80">Algorithm: </span>
                <span>{metadata.preset}</span>
                <span className="ml-1 rounded-md bg-muted px-1 text-muted-foreground h-5 text-xs">
                  v{metadata.version}
                </span>
              </div>
              <div>
                <span className="text-muted-foreground/80">Train mode: </span>
                <span>{metadata.train_mode}</span>
              </div>
              <div>
                <span className="text-muted-foreground/80">Preset: </span>
                <span>{metadata.algorithm}</span>
                <span className="text-muted-foreground/80"> • </span>
                <span>{metadata.framework}</span>
              </div>
              <div>
                <span className="text-muted-foreground/80">
                  Evaluation strategy:{" "}
                </span>
                <span>
                  {metadata.cross_validation ? "Cross Validation" : "Holdout"}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
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

export default ModelDetails;
