import { ChevronDown, ChevronUp } from "lucide-react";
import { useSearchParams } from "react-router-dom";

type SortableHeaderProps = {
  field: string;
  label: string;
};

const SortableHeader = ({ field, label }: SortableHeaderProps) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const sort = searchParams.get("sort");
  const dir = searchParams.get("dir");

  const toggleSort = (field: string) => {
    const params = new URLSearchParams(searchParams);

    if (sort !== field) {
      // activate new column -> desc
      params.set("sort", field);
      params.set("dir", "desc");
    } else if (dir === "desc") {
      // desc -> asc
      params.set("dir", "asc");
    } else {
      // asc -> remove sorting
      params.delete("sort");
      params.delete("dir");
    }
    // reset page on sorting
    params.delete("page");
    setSearchParams(params, { replace: true });
  };

  const isActive = sort === field;

  return (
    <button
      onClick={() => toggleSort(field)}
      className="flex items-center gap-1 hover:text-foreground"
    >
      <span>{label}</span>
      {isActive ? (
        dir === "desc" ? (
          <ChevronDown className="h-4 w-4 text-sky-400" />
        ) : (
          <ChevronUp className="h-4 w-4 text-sky-400" />
        )
      ) : (
        <ChevronDown className="h-4 w-4 text-muted-foreground" />
      )}
    </button>
  );
};

export default SortableHeader;
