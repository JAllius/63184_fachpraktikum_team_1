import { cn } from "@/lib/utils";
import { Badge } from "./badge";

type Props = {
  items: [string, string][];
  className?: string;
};

const ColumnBadges = ({ items, className }: Props) => {
  if (items.length === 0) {
    return <div className="mt-auto text-sm text-muted-foreground">None</div>;
  }
  return (
    <div
      className={cn(
        "mt-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-6 gap-y-1 overflow-hidden",
        className
      )}
    >
      {items.map(([id, v]) => (
        <Badge
          className="flex items-center justify-center w-full min-w-0"
          key={id}
          variant={"secondary"}
        >
          <span className="truncate">{v}</span>
        </Badge>
      ))}
    </div>
  );
};

export default ColumnBadges;
