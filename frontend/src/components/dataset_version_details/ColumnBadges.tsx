import { Badge } from "../ui/badge";

type Props = {
  items: [string, string][];
};

const ColumnBadges = ({ items }: Props) => {
  if (items.length === 0) {
    return <div className="mt-auto text-sm text-muted-foreground">None</div>;
  }
  return (
    <div className="mt-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-6 gap-y-1">
      {items.map(([id, v]) => (
        <Badge
          className="flex items-center justify-center"
          key={id}
          variant={"secondary"}
        >
          {v}
        </Badge>
      ))}
    </div>
  );
};

export default ColumnBadges;
