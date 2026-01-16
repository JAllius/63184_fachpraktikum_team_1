import { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Checkbox } from "../ui/checkbox";
import { Label } from "../ui/label";
import { Tabs, TabsList, TabsTrigger } from "../ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ReferenceLine,
  Scatter,
  ScatterChart,
  XAxis,
  YAxis,
} from "recharts";

import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";

import type { ExplainabilitySummaryClassification } from "./Explainability";

type Props = { summary: ExplainabilitySummaryClassification };

const chartConfig = {
  value: { label: "Influence", color: "hsl(var(--chart-1))" },
  impact: { label: "Impact", color: "hsl(var(--chart-2))" },
} satisfies ChartConfig;

export default function ExplainabilityClassification({ summary }: Props) {
  const [grouped, setGrouped] = useState(true);

  function pctLabel(q: number) {
    return `${Math.round(q * 100)}%`;
  }

  const classLabels = summary.metadata.label_classes ?? [];
  const classKey = String(Math.max(0, Math.min(classLabels.length - 1, 0)));

  const [activeClassKey, setActiveClassKey] = useState(
    classLabels.length ? "0" : classKey
  );

  const meanAbsParent =
    summary.global.mean_abs_parent_per_class[activeClassKey] ?? [];
  const meanAbsFeature =
    summary.global.mean_abs_per_class[activeClassKey] ?? [];
  const perFeature = summary.distributions[activeClassKey]?.per_feature ?? [];

  // parent -> fid (only from available distributions)
  const fidByParent: Record<string, number> = {};
  for (const item of perFeature) {
    const f = summary.features.find((x) => x.fid === item.fid);
    if (f && fidByParent[f.parent] === undefined)
      fidByParent[f.parent] = item.fid;
  }

  const selectableParents = meanAbsParent
    .map((p) => p.parent)
    .filter((p) => fidByParent[p] !== undefined);

  const [selectedParent, setSelectedParent] = useState<string>(
    selectableParents[0] ?? ""
  );

  const activeParent = selectableParents.includes(selectedParent)
    ? selectedParent
    : selectableParents[0] ?? "";

  const fid = activeParent ? fidByParent[activeParent] : undefined;
  const dist = fid != null ? perFeature.find((x) => x.fid === fid) : undefined;

  const barData = useMemo(() => {
    if (grouped) {
      return meanAbsParent.map((r) => ({ label: r.parent, value: r.value }));
    }
    return meanAbsFeature.map((r) => {
      const f = summary.features.find((x) => x.fid === r.fid);
      return { label: f?.name ?? `feature ${r.fid}`, value: r.value };
    });
  }, [grouped, meanAbsParent, meanAbsFeature, summary.features]);

  const barHeight = Math.min(520, Math.max(220, barData.length * 22));

  const quantiles = summary.metadata.quantiles ?? [];
  const scatterData = useMemo(() => {
    if (!dist) return [];
    return dist.shap_quantiles
      .map((impact, i) => {
        const typical = dist.X_quantiles[i];
        return {
          typical: typeof typical === "number" ? typical : null,
          impact,
          q: quantiles[i] != null ? pctLabel(quantiles[i]) : `Q${i + 1}`,
        };
      })
      .filter((p) => p.typical != null) as Array<{
      typical: number;
      impact: number;
      q: string;
    }>;
  }, [dist, quantiles]);

  const xDomain = useMemo(() => {
    if (scatterData.length === 0) return undefined;
    const xs = scatterData.map((d) => d.typical);
    const min = Math.min(...xs);
    const max = Math.max(...xs);
    const pad = (max - min) * 0.08 || 1;
    return [min - pad, max + pad] as [number, number];
  }, [scatterData]);

  return (
    <div className="grid gap-4">
      {/* class selector */}
      {classLabels.length > 1 && (
        <Tabs value={activeClassKey} onValueChange={setActiveClassKey}>
          <TabsList className="w-fit">
            {classLabels.map((label, i) => (
              <TabsTrigger key={label + i} value={String(i)}>
                {label}
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      )}

      {/* Top drivers */}
      <Card>
        <CardHeader className="flex flex-row items-start justify-between gap-4">
          <div>
            <CardTitle>Top drivers</CardTitle>
            <p className="text-sm text-muted-foreground">
              Bigger bars mean this factor matters more for this outcome.
            </p>
          </div>

          <div className="flex items-center gap-2 pt-1">
            <Checkbox
              checked={grouped}
              onCheckedChange={(v) => setGrouped(Boolean(v))}
            />
            <Label className="text-sm text-muted-foreground">
              Group by column
            </Label>
          </div>
        </CardHeader>

        <CardContent>
          <ChartContainer
            config={chartConfig}
            style={{ height: barHeight }}
            className="w-full"
          >
            <BarChart
              data={barData}
              layout="vertical"
              margin={{ left: 8, right: 16, top: 6, bottom: 6 }}
              barCategoryGap={6}
            >
              <CartesianGrid horizontal={false} />
              <XAxis
                type="number"
                tickLine={false}
                axisLine={false}
                tickMargin={6}
              />
              <YAxis
                type="category"
                dataKey="label"
                tickLine={false}
                axisLine={false}
                width={grouped ? 160 : 260}
              />
              <ChartTooltip content={<ChartTooltipContent />} />
              <Bar
                dataKey="value"
                radius={6}
                fill="var(--color-value)"
                isAnimationActive={false}
              />
            </BarChart>
          </ChartContainer>

          <div className="mt-2 text-xs text-muted-foreground">
            Influence (mean absolute impact)
          </div>
        </CardContent>
      </Card>

      {/* How a factor changes outcomes */}
      <Card>
        <CardHeader className="flex flex-row items-start justify-between gap-3">
          <div>
            <CardTitle>How a factor changes outcomes</CardTitle>
            <p className="text-sm text-muted-foreground">
              Typical value vs. impact on this class.
            </p>
          </div>

          <div className="w-[260px]">
            <Select value={activeParent} onValueChange={setSelectedParent}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {selectableParents.map((p) => (
                  <SelectItem key={p} value={p}>
                    {p}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardHeader>

        <CardContent>
          <ChartContainer config={chartConfig} className="h-[220px] w-full">
            <ScatterChart margin={{ left: 8, right: 16, top: 10, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <ReferenceLine y={0} strokeDasharray="4 4" />

              <XAxis
                type="number"
                dataKey="typical"
                tickLine={false}
                axisLine={false}
                tickMargin={6}
                domain={xDomain}
              />
              <YAxis
                type="number"
                dataKey="impact"
                tickLine={false}
                axisLine={false}
                tickMargin={6}
              />

              <ChartTooltip
                content={
                  <ChartTooltipContent
                    labelFormatter={(_, payload) => {
                      const r = payload?.[0]?.payload;
                      return r?.q ? `Percentile: ${r.q}` : "Point";
                    }}
                    formatter={(value, name, item) => {
                      const r = item?.payload ?? {};
                      if (name === "typical")
                        return [Number(value).toFixed(3), "Typical value"];
                      if (name === "impact")
                        return [Number(value).toFixed(4), "Impact"];
                      if (r?.q) return [r.q, "Percentile"];
                      return [String(value), String(name)];
                    }}
                  />
                }
              />

              <Scatter
                data={scatterData}
                fill="var(--color-impact)"
                isAnimationActive={false}
              />
            </ScatterChart>
          </ChartContainer>

          <div className="mt-2 text-xs text-muted-foreground">
            X: typical value (from quantiles) • Y: impact (SHAP)
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
