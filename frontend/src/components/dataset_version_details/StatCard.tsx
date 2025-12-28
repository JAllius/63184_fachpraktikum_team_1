import { cn } from "@/lib/utils";

type Props = {
  label: string;
  value: number | string;
  hint?: string;
  className?: string;
};

const StatCard = ({ label, value, hint, className }: Props) => {
  return (
    <div className={cn("rounded-lg border bg-card p-4", className)}>
      <div className="text-xs text-muted-foreground">{label}</div>
      <div className="mt-1 text-2xl font-semibold">{value}</div>
      {hint && <div className="mt-1 text-xs text-muted-foreground">{hint}</div>}
    </div>
  );
};

export default StatCard;
